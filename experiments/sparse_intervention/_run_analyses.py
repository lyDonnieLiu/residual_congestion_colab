"""
Analysis for "Two Failure Modes of Zero Ablation" paper
Runs analyses 1-4 and generates figures.

Analysis 1: MDI statistics per method x circuit
Analysis 2: Zero APS vs rank variance scatter
Analysis 3: MDI vs cross-method Kendall tau
Analysis 4: Impact demo -- what each method concludes about top-5 layers
"""

import json, numpy as np, matplotlib, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import rankdata

DATA_PATH = 'F:/codex/Lim/experiments/sparse_intervention/results/all_results.json'
ANALYSIS_PATH = 'F:/codex/Lim/experiments/sparse_intervention/results/analysis_for_paper.json'
FIG_DIR = 'F:/codex/Lim/Papers/zero_ablation_failure_modes/figures/'
os.makedirs(FIG_DIR, exist_ok=True)

with open(DATA_PATH) as f:
    raw = json.load(f)

with open(ANALYSIS_PATH) as f:
    analysis = json.load(f)

circuits = ['ioi', 'greater_than', 'docstring']
methods = ['zero_ablation', 'mean_ablation', 'resample_ablation',
           'gaussian_noise', 'activation_patching', 'activation_steering']
method_labels = ['Zero Ablation', 'Mean Ablation', 'Resample Ablation',
                 'Gaussian Noise', 'Activation Patching', 'Activation Steering']

# ============================================================
# Analysis 1: MDI (Measurement Discrimination Index) per method x circuit
# ============================================================
print("=" * 60)
print("ANALYSIS 1: Measurement Discrimination Index (MDI)")
print("=" * 60)

mdi_rows = []
for circuit in circuits:
    cd = raw[circuit]
    layers = sorted(cd.keys(), key=int)
    for mi, m in enumerate(methods):
        if m not in cd[layers[0]]:
            continue
        drops = np.array([cd[l][m]['behavioral_drop'] for l in layers])
        aps_vals = np.array([cd[l][m]['aps'] for l in layers])

        dyn_range = np.max(drops) - np.min(drops)
        unique_vals = len(set([round(d, 4) for d in drops]))
        granularity = (unique_vals - 1) / (len(layers) - 1) if len(layers) > 1 else 1.0
        mdi = dyn_range * granularity
        aps_mean = np.mean(aps_vals)

        mdi_rows.append({
            'circuit': circuit, 'method': method_labels[mi], 'method_key': m,
            'unique_values': unique_vals, 'mdi': mdi,
            'dynamic_range': dyn_range, 'aps_mean': aps_mean
        })

        print(f"  {circuit:15s} | {method_labels[mi]:22s} | "
              f"unique={unique_vals:2d}/{len(layers):2d} | "
              f"range={dyn_range:.4f} | MDI={mdi:.4f} | APS_mean={aps_mean:.3f}")

# MDI ranking
print("\n  --- MDI Summary ---")
for circuit in circuits:
    circ_rows = [r for r in mdi_rows if r['circuit'] == circuit]
    sorted_rows = sorted(circ_rows, key=lambda x: x['mdi'], reverse=True)
    print(f"\n  {circuit}:")
    for r in sorted_rows:
        print(f"    {r['method']:22s} MDI={r['mdi']:.4f} range={r['dynamic_range']:.4f}")

# ============================================================
# Analysis 2: Zero ablation APS vs rank variance
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS 2: Zero APS vs Rank Distribution")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

for ci, circuit in enumerate(circuits):
    cd = raw[circuit]
    layers = sorted(cd.keys(), key=int)

    # Per-layer ranks for all methods
    layer_ranks = {}
    active_methods = [m for m in methods if m in cd[layers[0]]]
    for m in active_methods:
        ranks = []
        for li, l in enumerate(layers):
            drops = [cd[l][mm]['behavioral_drop'] for mm in active_methods]
            all_ranks = rankdata(drops)
            m_idx = active_methods.index(m)
            ranks.append(all_ranks[m_idx])
        layer_ranks[m] = np.array(ranks)

    zero_aps = np.array([cd[l]['zero_ablation']['aps'] for l in layers])
    zero_rank = layer_ranks['zero_ablation']

    rank_var = np.var(zero_rank)

    ax = axes[ci]
    scatter = ax.scatter(zero_aps, zero_rank, c=range(len(layers)),
                         cmap='viridis', s=50, alpha=0.8, edgecolors='k', linewidth=0.5)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Layer Index')

    ax.set_xlabel('Zero Ablation APS')
    ax.set_ylabel('Zero Ablation Rank\n(higher = more important)')
    ax.set_title(f'{circuit.upper()}    (rank var={rank_var:.2f})')

    corr = np.corrcoef(zero_aps, zero_rank)[0,1]
    ax.text(0.05, 0.95, f'r = {corr:.3f}', transform=ax.transAxes,
            va='top', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    for li, l in enumerate(layers[:5]):
        ax.annotate(f'L{l}', (zero_aps[li], zero_rank[li]),
                    textcoords="offset points", xytext=(5,5), fontsize=7)

    print(f"  {circuit}: zero rank var={rank_var:.3f}, APS-range=[{zero_aps.min():.3f}, {zero_aps.max():.3f}], "
          f"rank-range=[{zero_rank.min():.0f}, {zero_rank.max():.0f}]")

plt.tight_layout()
plt.savefig(f'{FIG_DIR}aps_vs_rank_scatter.pdf', dpi=150, bbox_inches='tight')
plt.savefig(f'{FIG_DIR}aps_vs_rank_scatter.png', dpi=150, bbox_inches='tight')
print(f"\n  Saved: {FIG_DIR}aps_vs_rank_scatter.pdf")

# ============================================================
# Analysis 3: MDI vs cross-method Kendall tau
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS 3: MDI vs Cross-Method Agreement")
print("=" * 60)

method_tau = {}
for circuit in circuits:
    cdata = analysis[circuit]
    tau_pairs = cdata.get('kendall_tau', {}).get('pairs', [])
    for pair in tau_pairs:
        m1, m2 = pair['method1'], pair['method2']
        tau = pair['tau']
        method_tau.setdefault(m1, []).append(tau)
        method_tau.setdefault(m2, []).append(tau)

avg_tau = {m: np.mean(vals) for m, vals in method_tau.items()}
key_to_label = dict(zip(methods, method_labels))

mdi_vals = []
tau_vals = []
for m in methods:
    if m not in avg_tau or not any(r['method_key'] == m for r in mdi_rows):
        continue
    avg_mdi = np.mean([r['mdi'] for r in mdi_rows if r['method_key'] == m])
    mdi_vals.append(avg_mdi)
    tau_vals.append(avg_tau[m])
    print(f"  {key_to_label[m]:22s} | avg MDI={avg_mdi:.4f} | avg tau={avg_tau[m]:+.3f}")

fig2, ax2 = plt.subplots(figsize=(5, 4))
ax2.scatter(mdi_vals, tau_vals, s=100, alpha=0.8, edgecolors='k')
for i, m in enumerate(methods):
    if m in avg_tau:
        ax2.annotate(key_to_label[m].replace(' ', '\n'),
                     (mdi_vals[i], tau_vals[i]),
                     textcoords="offset points", xytext=(8,5), fontsize=8)
corr_mdi_tau = np.corrcoef(mdi_vals, tau_vals)[0,1]
ax2.set_xlabel('Average MDI (across circuits)')
ax2.set_ylabel('Average Kendall tau\n(vs all other methods)')
ax2.set_title(f'MDI vs Method Agreement   r = {corr_mdi_tau:.3f}')
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f'{FIG_DIR}mdi_vs_tau.pdf', dpi=150, bbox_inches='tight')
plt.savefig(f'{FIG_DIR}mdi_vs_tau.png', dpi=150, bbox_inches='tight')
print(f"\n  Saved: {FIG_DIR}mdi_vs_tau.pdf")

# ============================================================
# Analysis 4: Impact demo -- top-5 layers by each method
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS 4: Impact Demo -- Top-5 Layers by Each Method")
print("=" * 60)

for circuit in circuits:
    cd = raw[circuit]
    layers = sorted(cd.keys(), key=int)
    print(f"\n  --- {circuit.upper()} ---")

    for mi, m in enumerate(methods):
        if m not in cd[layers[0]]:
            continue
        drops = [(l, cd[l][m]['behavioral_drop']) for l in layers]
        drops_sorted = sorted(drops, key=lambda x: x[1], reverse=True)
        top5 = [d[0] for d in drops_sorted[:5]]
        top5_str = ', '.join([f'L{l}' for l in top5])
        aps_at_top5 = [f'{cd[l][m]["aps"]:.2f}' for l in top5]
        print(f"    {method_labels[mi]:22s} top-5: {top5_str}")
        print(f"    {'':22s} APS @ top-5: [{', '.join(aps_at_top5)}]")

    zero_top5 = set([l for l, _ in sorted(
        [(l, cd[l]['zero_ablation']['behavioral_drop']) for l in layers],
        key=lambda x: x[1], reverse=True)][:5])
    mean_top5 = set([l for l, _ in sorted(
        [(l, cd[l]['mean_ablation']['behavioral_drop']) for l in layers],
        key=lambda x: x[1], reverse=True)][:5])
    steer_top5 = set([l for l, _ in sorted(
        [(l, cd[l]['activation_steering']['behavioral_drop']) for l in layers],
        key=lambda x: x[1], reverse=True)][:5])

    j_zvsm = len(zero_top5 & mean_top5) / len(zero_top5 | mean_top5) if zero_top5 | mean_top5 else 0
    j_zvss = len(zero_top5 & steer_top5) / len(zero_top5 | steer_top5) if zero_top5 | steer_top5 else 0
    j_mvss = len(mean_top5 & steer_top5) / len(mean_top5 | steer_top5) if mean_top5 | steer_top5 else 0
    print(f"\n    Jaccard(zero, mean)     = {j_zvsm:.2f}")
    print(f"    Jaccard(zero, steering) = {j_zvss:.2f}")
    print(f"    Jaccard(mean, steering) = {j_mvss:.2f}")

print("\n" + "=" * 60)
print("ALL ANALYSES COMPLETE")
print("=" * 60)

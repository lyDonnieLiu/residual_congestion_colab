import json, numpy as np
from scipy.stats import rankdata

with open('results/all_results.json') as f:
    data = json.load(f)

circuits = ['ioi', 'greater_than', 'docstring']
methods = ['zero_ablation', 'mean_ablation', 'resample_ablation', 'gaussian_noise', 'activation_patching', 'activation_steering']

for circuit in circuits:
    print(f'=== {circuit.upper()} ===')
    cd = data[circuit]
    layers = sorted(cd.keys(), key=int)

    method_data = {}
    for m in methods:
        if m not in cd[layers[0]]:
            continue
        aps_list = [cd[l][m]['aps'] for l in layers]
        bdrop_list = [cd[l][m]['behavioral_drop'] for l in layers]
        method_data[m] = {'aps': np.array(aps_list), 'bdrop': np.array(bdrop_list)}

    layer_ranks = {}
    for l_idx, l in enumerate(layers):
        drops = [method_data[m]['bdrop'][l_idx] for m in methods if m in method_data]
        ranks = rankdata(drops)
        r_idx = 0
        for m in methods:
            if m in method_data:
                if m not in layer_ranks:
                    layer_ranks[m] = []
                layer_ranks[m].append(ranks[r_idx])
                r_idx += 1

    zero_aps = method_data['zero_ablation']['aps']

    # Correlation: zero APS vs rank disagreement
    for cmp in ['mean_ablation', 'activation_steering', 'resample_ablation', 'gaussian_noise']:
        if cmp not in layer_ranks:
            continue
        diffs = np.abs(np.array(layer_ranks['zero_ablation']) - np.array(layer_ranks[cmp]))
        corr = np.corrcoef(zero_aps, diffs)[0,1]
        print(f'  zero_aps vs |rank_diff(zero-{cmp})|: r = {corr:.3f}')

    # Count layers
    low = zero_aps < 0.80
    high = zero_aps >= 0.95
    print(f'  APS<0.80: {np.sum(low)} layers, APS>=0.95: {np.sum(high)} layers')

    if np.sum(low) > 0:
        for cmp in ['mean_ablation', 'activation_steering']:
            if cmp not in layer_ranks: continue
            zd = np.array(layer_ranks['zero_ablation'])[low]
            cd = np.array(layer_ranks[cmp])[low]
            print(f'    Low-APS: mean |rank_diff(zero-{cmp})| = {np.mean(np.abs(zd - cd)):.2f}')

    if np.sum(high) > 0:
        for cmp in ['mean_ablation', 'activation_steering']:
            if cmp not in layer_ranks: continue
            zd = np.array(layer_ranks['zero_ablation'])[high]
            cd = np.array(layer_ranks[cmp])[high]
            print(f'    High-APS: mean |rank_diff(zero-{cmp})| = {np.mean(np.abs(zd - cd)):.2f}')

    # Direction check: in low-APS layers does zero ALWAYS rank it higher?
    if np.sum(low) > 0:
        for cmp in ['mean_ablation', 'activation_steering']:
            if cmp not in layer_ranks: continue
            zd = np.array(layer_ranks['zero_ablation'])[low]
            cd = np.array(layer_ranks[cmp])[low]
            # How often does zero rank higher (more important) than cmp?
            higher = np.mean(zd > cd)
            print(f'    Low-APS: zero ranks higher than {cmp} in {higher*100:.0f}% of layers')

    # Detailed per-layer view for zero-mean comparison
    print('  Per-layer detail (zero vs mean):')
    for li, l in enumerate(layers):
        zr = layer_ranks['zero_ablation'][li]
        mr = layer_ranks['mean_ablation'][li]
        za = method_data['zero_ablation']['aps'][li]
        zb = method_data['zero_ablation']['bdrop'][li]
        mb = method_data['mean_ablation']['bdrop'][li]
        print(f'    L{l}: zero_rank={zr:.0f} mean_rank={mr:.0f} | APS={za:.3f} zero_drop={zb:.3f} mean_drop={mb:.3f}')

    print()

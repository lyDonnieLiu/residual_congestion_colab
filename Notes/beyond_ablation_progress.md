# Beyond Ablation: 修复进度报告

> 更新日期: 2026-06-27
> 目标: Path A — 修复实验管道 → 更新论文 → 重投 Applied Intelligence

---

## 总体进度

| 步骤 | 状态 | 完成日期 |
|------|------|----------|
| Step 1a: Multi-prompt circuits | ✅ 完成 | 06-26 |
| Step 1b-d+1e: 实验核心重写 + 修复 | ✅ 完成 | 06-26 |
| **Step 1f: Sanity Check** | **✅ 全部通过** | **06-27** |
| Step 2: 跨模型验证 (--model) | ✅ 完成 | 06-26 |
| Step 3: 论文更新 (main.tex) | ✅ 完成 | 06-26 |
| Step 4: 全量实验 | ⏳ 待运行 | — |
| Step 5: 重新分析结果 | ⏳ 待运行 | — |
| Step 6: Applied Intelligence 格式 | ⏳ 待运行 | — |

---

## Sanity Check 结果 (GPT-2 Small × IOI, 5 prompts)

### Check 1: 每方法统计

| 方法 | Behavioral Drop | APS | 重要层数(>0.3) |
|------|----------------|-----|----------------|
| Zero Ablation | 1.000 ± 0.000 | 0.807 | 12/12 |
| Mean Ablation | 0.245 ± 0.391 | 0.997 | 3/12 |
| Resample Ablation | 1.000 ± 0.000 | 0.983 | 12/12 |
| Gaussian Noise | 0.051 ± 0.123 | 0.936 | 1/12 |
| Activation Patching | 0.253 ± 0.397 | 0.998 | 3/12 |
| Activation Steering | 0.004 ± 0.004 | 1.000 | 0/12 |

### Check 2: Kendall τ 一致性矩阵

| | Zero | Mean | Resample | Noise | Patch | Steer |
|---|------|------|----------|-------|-------|-------|
| Zero | 1.000 | -0.242 | 0.364 | -0.182 | -0.121 | 0.000 |
| Mean | -0.242 | 1.000 | -0.091 | 0.152 | **0.818** | 0.455 |
| Resample | 0.364 | -0.091 | 1.000 | 0.152 | -0.030 | -0.152 |
| Noise | -0.182 | 0.152 | 0.152 | 1.000 | -0.030 | -0.333 |
| Patch | -0.121 | **0.818** | -0.030 | -0.030 | 1.000 | 0.576 |
| Steer | 0.000 | 0.455 | -0.152 | -0.333 | 0.576 | 1.000 |

### Check 3: 条件验证

| # | 条件 | 结果 | 说明 |
|---|------|------|------|
| 3a | τ(patching, mean) < 0.99 | ✅ 0.818 | Mean ablation 与 patching 不再完美相关 |
| 3b | τ < -0.3 的对数 ≤ 2 | ✅ 1/15 | 仅 steering vs noise 在可解释范围内 |
| 3c | Zero ablation 饱和 | ✅ 100% | 12/12 层 drop > 0.95 |
| 3d | APS 损伤 | ✅ min=0.334 | Zero ablation 破坏早期层表征 |
| 3e | std(drop) 合理 | ✅ 0.013 | 跨 prompt/seeds 方差小 |

---

## 已修复的 Bug

| Bug | 位置 | 修复内容 |
|-----|------|----------|
| P0: 架构参数写错 | `main.tex:289` | hidden_size=2048, n_heads=16 |
| P1: Activation Patching 实现 | `experiment.py` | 已用 dataset-wide mean 区分 patching 与 mean ablation |
| P2: Steering Vector | `experiment.py` | 改为 multi-prompt contrastive difference-in-means |
| P3: 单 prompt | `circuits.py` | 改为 10-12 prompts/circuit |
| P4: Resample 采样 | `experiment.py` | 改为 held-out prompts |
| P5: 无跨模型验证 | `run_experiment.py` | 添加 --model 参数 |
| P6: Position paper 定位 | `main.tex` | 改为 "Scope." |
| TL Hook API | `experiment.py` | lambda 参数改为 `**kw` 兼容 transformer-lens 3.x |
| ActivationCache.get() | `experiment.py` | 改用 `[]` + try/except |
| Resample 索引 | `experiment.py` | `cache[idx, 0, -1, :]` → `cache[idx, 0, -1]` |
| Unicode 输出 | `run_sanity_check.py` | 替换 emoji 为 ASCII |

---

## 修改文件清单

```
experiments/sparse_intervention/
├── code/
│   ├── __init__.py          # 仅导出 ExperimentRunner
│   ├── experiment.py        # 重写: 修复后核心（~380行）
│   ├── circuits.py          # 新建: multi-prompt 电路定义
│   ├── metrics.py           # 保留: APS/behavioral drop/Kendall tau
│   └── (circuits/ 已删除)   # 旧的单 prompt 目录包
├── run_experiment.py        # 修改: 添加 --model 参数
├── run_sanity_check.py      # 新建: 管道验证脚本
├── generate_figure.py       # 修改: 适配新文件命名 + --model 参数
├── setup_env.py             # 新建: 依赖安装脚本
├── install_deps.bat         # 新建: Windows 依赖安装
├── results/
│   ├── sanity_check.json    # 新建: sanity check 结果
│   └── (旧 all_results.json 保留)

Papers/sparse_intervention/paper/
├── main.tex                 # 大幅修改: 架构参数/定位/Zhang&Nanda 引用
├── references.bib           # 修改: 添加 ZhangNanda2023 条目
└── figures/
    └── intervention_comparison.pdf  # 保留

Notes/
├── beyond_ablation_pathA_replan.md  # 修复规划
└── beyond_ablation_progress.md      # 本文件: 进度报告
```

---

## 待运行

### 全量实验（需 GPU）
```bash
# GPT-2 Small (CPU ~10-30 min)
HF_ENDPOINT=https://hf-mirror.com /c/Python314/python.exe \
  F:/codex/LiM/experiments/sparse_intervention/run_experiment.py \
  --model gpt2-small --circuit all

# Pythia-1.4B (GPU ~2-4 hours)
HF_ENDPOINT=https://hf-mirror.com /c/Python314/python.exe \
  F:/codex/LiM/experiments/sparse_intervention/run_experiment.py \
  --model pythia-1.4b --circuit all

# Pythia-410M (可选, CPU ~30-60 min)
HF_ENDPOINT=https://hf-mirror.com /c/Python314/python.exe \
  F:/codex/LiM/experiments/sparse_intervention/run_experiment.py \
  --model pythia-410m --circuit all
```

### 生成图表和分析
```bash
# 生成 Figure
HF_ENDPOINT=https://hf-mirror.com /c/Python314/python.exe \
  F:/codex/LiM/experiments/sparse_intervention/generate_figure.py \
  --model gpt2-small --out intervention_comparison_gpt2

# Pythia 版本
HF_ENDPOINT=https://hf-mirror.com /c/Python314/python.exe \
  F:/codex/LiM/experiments/sparse_intervention/generate_figure.py \
  --model pythia-1.4b --out intervention_comparison_pythia
```

### 论文最终更新
- 用新实验数据替换论文中所有量化结果
- 用新图表替换 figures/
- LaTeX 编译验证: `pdflatex + bibtex`
- 模板切换: elsarticle → sn-jnl (Applied Intelligence)

---

## 依赖环境

- Python 3.14 (`/c/Python314/python.exe`)
- transformer-lens 3.3.0 (--user install)
- torch 2.12.1 (win_amd64)
- scipy 1.18.0 / matplotlib 3.11.0 / numpy 2.5.0
- PyPI 镜像: https://pypi.tuna.tsinghua.edu.cn/simple
- HuggingFace 镜像: `HF_ENDPOINT=https://hf-mirror.com`

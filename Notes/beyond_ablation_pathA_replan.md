# Beyond Ablation: Path A — 实验修复与重新投稿规划

> 生成日期: 2026-06-26
> 背景: Neurocomputing desk rejection
> 审稿人核心意见:
> 1. 架构参数与 Pythia-1.4B 实际配置严重不符 (hidden_size=14336→2048, n_heads=24→16)
> 2. 中心 claim 过于 sweeping，实证证据不足
> 3. 论文自我定位为 position paper 却投 research article
> 目标期刊: Applied Intelligence (中科院二区, ~5.0 IF, 3-5月审稿周期)

---

## 1. 已诊断的实验问题

### P0 (致命) — 论文中架构参数写错

**位置**: `main.tex:289`

```
论文写: "24 layers, 24 attention heads per layer, 14336 hidden dimensions"
实际:   "24 layers, 16 attention heads per layer, 2048 hidden dimensions"
```

TransformerLens 实际加载的模型是正确的，错误仅在论文文本中。但这足以让审稿人质疑所有实验数据的可信度。

### P1 — Activation Patching 实现错误

**位置**: `code/__init__.py:122-128`

只 patch 最后一个 token 位置 `act[0,-1,:]`，而非标准的 full-residual-stream swap。结果与 Mean Ablation 的 Kendall τ = 1.000，说明 patching 实验措施失效——它测量的其实是同样的事情。

### P2 — Steering Vector 需要 contrastive 训练

**位置**: `code/__init__.py:76`

```python
steer_dir = mean_corrupt - mean_clean
```

difference-in-means 方向思路本身合理（即对比两个条件下激活的差异方向），但受限于单 prompt，统计稳定性不足。需要改为 multi-prompt contrastive 训练以构造有统计效力的 steering direction。

### P3 — 每个电路仅 1 个 prompt

**位置**: `circuits/__init__.py:25-40`

论文声称 "100 templates"，但代码中每个电路只有 1 个 {clean, corrupt, answer} 三元组。无法获得 statistical reliability。

### P4 — Resample Ablation 采样错误

**位置**: `code/__init__.py:68-69`

```python
xb = xt.repeat(n_repeats, 1)  # 重复同一个 corrupt prompt 20 次
```

标准做法是从 held-out 数据集中采不同的激活值。

### P5 — 无跨模型验证

仅 Pythia-1.4B，无 GPT-2 Small 或其他规模的验证。

### P6 — 论文定位矛盾

`main.tex:86` 写 "This is a position paper"，与 research article 投稿矛盾。

---

## 2. 修复计划

### Step 1: 修复实验基础设施（代码）

#### 1a. 修复电路定义 → Multi-Prompt

**文件**: `experiments/sparse_intervention/code/circuits/__init__.py`

```python
# 改为 multi-prompt：每个电路 10 个 {clean, corrupt, answer} 三元组
IOI_PROMPTS = [
    ("When Mary and John went to the store, John gave a bottle to", "When Mary and John went to the store, Mary gave a bottle to", " Mary"),
    ("When Tom and Sarah went to the park, Sarah gave a book to", "When Tom and Sarah went to the park, Tom gave a book to", " Sarah"),
    ...  # 10-20 个模板
]
```

每个干预在全部 prompt 上运行，结果取平均 → 获得 statistical reliability。

#### 1b. 修复 Activation Patching

```python
# 标准做法：在 IO token 位置交换整个残差流
# 而非只 patch 最后一个 token
def _patch_full(act, src, pos_idx):
    act[:, pos_idx, :] = src[:, pos_idx, :].to(act.device)
    return act
```

需要确定 IO token 在序列中的位置（对 IOI 电路是第二个名字出现的位置）。

#### 1c. 修复 Steering Vector

```python
# 使用 multi-prompt 的 difference-in-means
steer_dir = mean(corrupt_acts) - mean(clean_acts)
# 在全部 prompt 上验证 steering 效果
```

#### 1d. 修复 Resample Ablation

```python
# 从 held-out prompt 集中采不同的激活值
held_out_prompts = [...]  # 留出的 prompt 集
with torch.no_grad():
    _, held_out_cache = model.run_with_cache(held_out_tokens)
# 从 held_out_cache 的 batch 维度随机采样
```

#### 1e. 重构实验脚本结构（保持简洁）

将 `code/__init__.py` 从单一文件拆分，但避免过度抽象：

```
code/
├── __init__.py         # 仅导出 ExperimentRunner
├── experiment.py       # ExperimentRunner + 6种干预方法（核心逻辑，保持扁平）
├── circuits.py         # 多 prompt 电路定义（数据，而非类层次）
└── metrics.py          # 保留现有的 metrics（APS, behavioral drop, Kendall tau）
```

**原则**: 不引入不必要的工厂模式或抽象基类。ExperimentRunner 保持一个类搞定运行逻辑，circuits.py 用 dict/list 而非 class hierarchy。实验脚本简单可读优先于"未来可扩展"。

#### 1f. Post-Fix Sanity Check

实验修复后，先不急于全量跑，做一轮轻量 sanity check 验证管道：

```python
# 在 1 个电路（IOI）上用 5 个 prompt 跑一轮全部 6 种方法
# 核心验证目标：
#   1. activation_patching 与 mean_ablation 不再 τ=1.0
#   2. 所有方法间 τ 不再大面积出现负相关（或如有负相关，给出因果解释）
#   3. zero_ablation 是否仍有测量饱和现象
#   4. 检查 std(behavioral_drop) across prompts 是否合理
```

如果 sanity check 通过，进入全量实验；如果出现异常模式，先诊断再继续。

### Step 2: 添加跨模型验证

在 `run_experiment.py` 中添加 `--model` 参数：

```python
parser.add_argument("--model", default="pythia-1.4b",
                    choices=["pythia-1.4b", "gpt2-small", "pythia-410m"])
```

三个模型覆盖不同规模：

| Model | Layers | Hidden | Heads | Params | 运行条件 |
|-------|--------|--------|-------|--------|---------|
| GPT-2 Small | 12 | 768 | 12 | 124M | CPU 可跑 |
| Pythia-410M | 24 | 1024 | 16 | 410M | CPU 可跑 |
| Pythia-1.4B | 24 | 2048 | 16 | 1.4B | 推荐 GPU |

### Step 3: 修复论文 main.tex

#### 3a. 修复架构参数

```latex
% 修改前
Pythia-1.4B (24 layers, 24 attention heads per layer, 14336 hidden dimensions)
% 修改后
Pythia-1.4B (24 layers, 16 attention heads per layer, 2048 hidden dimensions)~\cite{Biderman2023}
```

#### 3b. 删除 "position paper" 定位（main.tex:86-87）

删除 `\textbf{Positioning.}` 整段，改写为研究范围说明。

#### 3c. 新增 Related Work 对比（Conmy 2023 + Zhang 2023）

在 Related Work 中新增与基线方法的直接对比：

- **Conmy 2023 (ACDC)**: 自动化电路发现的分层剪枝方法。ACDC 与本文的 six-method 对比的异同——ACDC 是 circuit-level 的自动化分析，本文是 component-level 的干预方法比较，两者互补
- **Zhang 2023**: 需补充该工作的核心方法与本文的维度框架对比

注意引用信息要核实完整，避免学术规范问题。

#### 3d. 更新实验章节（Section 5）

- 更新 Multi-prompt 描述（替代原来的 "100 templates" claim）
- 更新 Table 1（Summary of behavioral drops）中的数值
- 更新 Table 2（Kendall τ consistency matrix）
- 新增跨模型对比表（3 models × same analysis）

#### 3d. 更新全文字面数值

涉及量化结果的地方（85% over-report、τ = -0.51 等），用新实验数据替换。

### Step 4: 重新运行实验

```bash
# 4a. Pythia-1.4B (全量)
python run_experiment.py --model pythia-1.4b --circuit all

# 4b. GPT-2 Small (跨模型验证)
python run_experiment.py --model gpt2-small --circuit all

# 4c. Pythia-410M (可选跨规模验证)
python run_experiment.py --model pythia-410m --circuit all

# 4d. 生成图表
python generate_figure.py
```

**GPU 注意事项**: GPT-2 Small (124M) 可在 CPU 2-10 分钟内完成。Pythia-1.4B 建议 GPU。如无 GPU，优先跑 GPT-2 Small 验证管道正确性。

### Step 5: 重新分析并验证结论

验证以下核心 claim 在修复后是否仍然成立：

1. **方法间不一致**: mean Kendall τ < 0.3? (修复前为 -0.10) —— 应不再出现大面积负相关
2. **如有负相关**: 给因果解释（例如 zero ablation 的测量饱和 vs 其他方法的区分性排序自然导致反向排序）
3. **Zero ablation over-report**: 是否仍然报告更多重要层?
4. **APS 揭示 silent damage**: L0-L2 的 APS 是否仍显著低?
5. **跨模型一致性**: 结论是否在不同模型上可复现?

### Step 6: 目标期刊格式调整

按 **Applied Intelligence** (Springer) 模板调整：

| 项目 | 说明 |
|------|------|
| 模板 | elsarticle → sn-jnl (Springer Nature) |
| 页数 | 通常无严格限制，建议 20-25 页 |
| 文献 | Springer Nature 标准格式 |
| 特殊要求 | Highlights + Abstract + Keywords |
| 审稿周期 | 3-5 个月 |

---

## 3. 修改文件清单

| 文件 | 修改类型 | 说明 |
|------|----------|------|
| `experiments/sparse_intervention/code/circuits/__init__.py` | **重写** | 改为 multi-prompt 数据结构 |
| `experiments/sparse_intervention/code/__init__.py` | **拆分重构** | ExperimentRunner, 修复所有干预方法 |
| `experiments/sparse_intervention/code/experiment.py` | **新建** | 从 __init__.py 拆出运行逻辑 |
| `experiments/sparse_intervention/code/circuits.py` | **新建** | 从 circuits/ 拆出的 multi-prompt 定义 |
| `experiments/sparse_intervention/code/metrics.py` | 保留 | APS, behavioral drop, Kendall tau |
| `experiments/sparse_intervention/code/analysis.py` | 微调 | 适配新数据结构 |
| `experiments/sparse_intervention/run_experiment.py` | 修改 | 添加 --model 参数 |
| `experiments/sparse_intervention/generate_figure.py` | 微调 | 输出路径和图例 |
| `Papers/sparse_intervention/paper/main.tex` | **大幅修改** | 架构参数、定位、实验数据 |
| `Papers/sparse_intervention/paper/references.bib` | 微调 | 补全缺失字段、移除非引用条目 |

---

## 4. 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 修复后实验结果与原结论不一致 | 中 | 高 | 接受新结果重新叙事；method disagreement 本身是 robust 现象 |
| 无 GPU 无法跑 Pythia-1.4B | 高 | 中 | 优先跑 GPT-2 Small (CPU) 验证管道；Pythia-1.4B 用已有结果做趋势分析 |
| Applied Intelligence 也 desk reject | 低 | 高 | 已分析 scope 匹配度 ⭐⭐⭐⭐⭐；备选 Complex & Intelligent Systems |
| 实验修复后代码容量/时间超预期 | 中 | 中 | 先重构再跑，做好单元验证 |

---

## 5. 验证方式

1. **单元验证**: 每个干预方法在单层单 prompt 上手工校验输出合理性
2. **跨方法一致性**: 修复后 mean ablation 和 patching 应该 τ < 1.0 (不再完美相关)
3. **跨模型验证**: GPT-2 Small 结果应定性一致但不定量相同
4. **LaTeX 编译**: `pdflatex + bibtex` 0 error

---

## 6. 参考文献

- Applied Intelligence 投稿指南: https://www.springer.com/journal/10489/submission-guidelines
- Pythia-1.4B 架构: https://huggingface.co/EleutherAI/pythia-1.4b
- Neurocomputing desk rejection 原文: 见审稿人邮件
- 期刊推荐原文档: `Notes/zero_ablation_journal_recommendation.md`

# Zero Ablation 双失效模式分析论文（方向 C 第二篇）

## Context

基于 `all_results.json` 的数据驱动发现。Paper 1 (Beyond Ablation) 已完成投稿准备。

**核心发现**：Zero ablation 有两个不同的失效模式——APS 只能捕获其中一个，另一个（度量饱和）更根本。

| 指标 | IOI | GT | Docstring |
|:---|:---:|:---:|:---:|
| Zero 唯一 drop 值 | 3/24 | 2/24 | 18/24 |
| Gentle 方法动态范围 | 0.0–0.97 | 0.0–0.99 | 0.0–0.96 |
| 关键层证据 | L11: APS=0.996, drop=1.0 | — | — |

## 论文结构

1. **Introduction** — 从"方法不一致到诊断失效"
2. **模式一：表征损伤** — APS 可见，L0-L4，验证 Paper 1
3. **模式二：度量饱和** — APS 不可见，L5-L23，新发现
4. **诊断：为什么 APS 修正不可能** — 定理级陈述
5. **MDT** — Measurement Discrimination Test 框架
6. **Impact Demo** — Zero vs Mean 排序的实际影响
7. **Discussion + Conclusion**

## 时间线

| 时段 | 事件 |
|:---|:---|
| 第 1-2 天 | 运行 4 个分析，生成图表 |
| 第 3-7 天 | 写初稿 |
| 第 8-10 天 | 修改定稿 |
| 第 11-14 天 | arXiv + TMLR 准备 |

## 前缀依赖

- `experiments/sparse_intervention/results/all_results.json` ✅
- `experiments/sparse_intervention/results/analysis_for_paper.json` ✅
- `/c/Python314/python.exe` ✅
- scipy / numpy / matplotlib ✅

详见：`.claude/plans/glittery-nibbling-scroll.md`

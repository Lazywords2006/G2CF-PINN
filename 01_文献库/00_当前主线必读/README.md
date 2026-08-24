# Block KyFan-PINN 当前主线文献

本目录共有 56 份 PDF、55 个唯一文件版本。当前论文最直接的 34 份全文位于 `07`–`10`；`06` 是实验可信性标准；`01`–`05` 是 TSONN / Allen–Cahn 旧路线背景，不再代表当前选题。

整个 `01_文献库` 当前共有 170 份 PDF，SHA-256 去重后为 167 个唯一版本。不要把文件数量当成互不重复的论文数量。

## 先按这个顺序读（P5 STOP 后）

1. [10_创新机制期刊证据链](10_创新机制期刊证据链/README.md)：先确认当前机制不是凭空发明，也看清哪些部件不能声称首创；
2. [07_Bloch_Grassmann_本征子空间](07_Bloch_Grassmann_本征子空间/README.md)：最接近当前“Bloch 简并谱簇”课题的论文；
3. [09_2026_增量审计](09_2026_增量审计/README.md)：2026 最新工作如何压缩裸 `anchor + Ky Fan` 的创新空间；
4. [08_SCI三区补强](08_SCI三区补强/README.md)：二维 periodic quantum、Dirac、Maxwell 和高重数 eigenspace 补强；
5. [06_FalsifyPDE_基准与可信评估](06_FalsifyPDE_基准与可信评估/README.md)：为什么必须用传统数值方法、强基线和真实误差防止假阳性。

当前不要继续围绕“低频 ROM 为什么应该有效”补论文。P5 已经证明其机制归因和
gap-scan 安全未通过。下一轮文献只需围绕三个问题定向补充：无标签失效风险、选择性
预测/risk–coverage、以及高风险参数的 certified fallback。未经过新检索核验的机制不能
因为“听起来合理”就进入论文贡献。

## 最重要的文献结论

- Grubišić 等（*Numerische Mathematik*, 2023）：内部本征值可以相交，只要整个目标簇与外部谱分开，谱投影仍是稳定对象；
- Wang & Xie（*JCP*, 2024）：无标签 trace / Ky Fan 神经子空间可行；
- Chang 等（*ACM TOG*, 2025）：参数化神经本征分析与模态交换已有高水平期刊先例；
- Pau（*Physical Review E*, 2007）和 Horger 等（*M2AN*, 2017）：Bloch 降阶、整个 eigenspace、residual/gap 选点有成熟数值依据；
- Riffaud（*JCP*, 2025）：预测不可靠时回退高精度求解器已有正式期刊先例；
- Mera / Mitscherling（*PRB*, 2022–2025）：简并能带应使用 projector 和量子几何等基不变量。

因此，当前论文不能把 Ky Fan、Grassmann、Bloch ROM、fallback 或 projector quantum metric 单独称作创新。P5 又进一步排除了“无条件低频 ROM”作为核心贡献。可验证的新贡献必须来自这些机制在“无标签二维 Bloch–Schrödinger 精确内部简并谱投影”上的问题特定闭环，并通过风险校准与公平实验自行证明。

## 历史背景

编号 `01` 至 `05` 的五组文献只为追溯早期选题保留。它们不应出现在当前论文的首要阅读顺序，也不能覆盖 P5 独立审计后的 2026-08-24 判断。

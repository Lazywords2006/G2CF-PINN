# AI 研究工作区规则

唯一研究状态来源：`00_项目总览/00_当前研究总档案.md`。

权威代码：`03_当前主线_BlockKyFanPINN/02_当前代码仓库/`。权威证据与 P5 审计以该
仓库的 `docs/P5-INDEPENDENT-AUDIT.zh-CN.md` 为准。

必须遵守：

- P5 已独立确认 `P5_PROMOTION_STOP`；
- 低频 ROM 不再是主创新；
- 当前步骤是独立风险开发集与无标签组合风险量；
- 不读取历史快照决定当前方案；
- 不重跑 P5、不改门槛、不挑 checkpoint、不打开 frozen final；
- MPS smoke 不是 CUDA/ROCm 正式论文结果；
- 待运行、理论预期和配置文件不能写成实际结果。

验证命令：

```bash
cd 03_当前主线_BlockKyFanPINN/02_当前代码仓库
uv run --python 3.12 --with-requirements requirements.txt python -m pytest -q
```

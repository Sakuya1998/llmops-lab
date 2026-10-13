# LLM 评测流水线：可执行的本地回归实验

此目录包含不依赖 GPU、外部模型 API 或第三方评测服务的确定性实验。它用合成数据验证评测流程、基线比较和发布门禁；它不是通用的语义质量评测器。

## 目录

- dataset.jsonl：合成测试样本和期望输出。
- baseline_predictions.jsonl：基线版本预先记录的输出。
- candidate_predictions.jsonl：候选版本输出。
- evaluate.py：准确率计算、基线回归比较和退出码门禁。
- ../../tests/test_evaluation.py：通过和失败路径的自动化测试。

每行 JSONL 是一个 JSON object。数据集 id 必须唯一，预测文件必须与数据集 ID 一一对应。

## 运行实验

    python pipelines/evaluation/evaluate.py
    pytest -q tests/test_evaluation.py

默认门禁要求候选准确率至少 0.75，且相对基线的准确率下降不超过 0.10。成功退出码为 0；质量门禁不通过时退出码为 1；输入文件或格式错误时退出码为 2。

生成机器可读报告：

    python pipelines/evaluation/evaluate.py --report artifacts/evaluation/report.json

脚本会创建报告目录；请勿将真实提示词、客户数据、密钥或受许可证限制的样本放入仓库。

## 验证门禁确实会失败

复制 candidate_predictions.jsonl 到临时文件，故意修改一条 output，再运行：

    python pipelines/evaluation/evaluate.py --candidate /tmp/candidate-regressed.jsonl

预期返回非零退出码。先复制文件再修改，不要破坏仓库内的通过样例。

## 局限与下一步

- 当前采用空白/大小写归一化后的精确匹配，不理解语义等价答案。
- 评测 fixture 是人工编写的合成输出，不代表任何真实模型质量。
- 后续可加入模型、提示词、推理参数、数据集版本、延迟和 token 用量元数据，并独立保存原始结果与汇总报告。
- 只有在门禁指标与实际任务相关、样本有代表性且阈值经过校准后，才应作为发布依据。

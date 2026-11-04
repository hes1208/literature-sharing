# 贡献指南 Contributing

欢迎改进写作流程、术语提醒、截图可靠性、检查工具和宿主兼容性说明。请围绕可复现的具体问题修改，避免把单篇论文的事实、公式或固定坐标写进通用 skill。

Contributions should address a reproducible editorial or tooling need. Keep paper-specific facts, equations and coordinates out of the general instructions.

## 提交要求 Requirements

- 简述问题、修改后的行为和验证方式。 / Describe the issue, resulting behavior and validation.
- 更新相关中英文说明；长篇专业规则可中文为主并附英文摘要。 / Keep user-facing bilingual documentation aligned.
- 只使用模拟、公开可再分发且已注明来源的测试材料。 / Use synthetic or explicitly redistributable fixtures.
- 不提交原论文、个人案例、生成的Word/PDF、账号信息或本地路径。 / Do not commit private materials or credentials.
- 保留“完整图表覆盖 + 简洁结果 + 逐页检查”的核心要求。 / Preserve complete evidence coverage, concise results and visual inspection.

## 本地验证 Local validation

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

脚本修改应有针对行为的模拟测试。仅修改文字时检查相对链接、JSON/YAML格式和中英文一致性。不得将机械测试通过解释为科学总结准确或跨宿主兼容性已验证。

For script changes, add behavioral tests. For documentation changes, check links, formats and bilingual consistency. A test pass is not scientific or cross-host certification.

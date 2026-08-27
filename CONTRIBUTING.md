# Contributing

感谢参与。请先阅读 `README.md` 和 `SECURITY.md`，不要提交登录状态、Cookie、调试响应、真实视频、
音频、转写结果或模型缓存。

## Development

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,agent]'
.venv/bin/pytest -q
.venv/bin/ruff check project tests
.venv/bin/mypy project
```

Windows PowerShell 使用 `.venv\Scripts\python` 替换上面的 `.venv/bin/python`。

新增行为时请同时增加脱离真实抖音账号的 fixture 测试。涉及网络、登录或媒体下载的测试必须使用
mock/fake 后端，避免在 CI 中访问真实账号。

提交信息使用简短的 Conventional Commit，例如 `feat: add markdown exporter`。

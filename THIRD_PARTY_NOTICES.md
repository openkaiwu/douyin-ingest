# Third-party notices

DouyinIngest 的代码和文档按仓库根目录的 Apache License 2.0 发布。依赖包、浏览器、媒体工具、
模型权重以及通过工具访问或生成的内容不属于本仓库的授权范围。

## Python dependencies

The packages declared in `pyproject.toml` continue to be distributed under their own licenses:

- AnyIO — MIT
- HTTPX — BSD 3-Clause
- Loguru — MIT
- Playwright — Apache License 2.0
- Pydantic — MIT
- faster-whisper — MIT (optional)
- python-docx — MIT (optional)

开发依赖（pytest、pytest-asyncio、ruff、mypy）也继续适用各自发行包中的许可证和声明。发布二进制
或锁定依赖版本时，应以对应版本的发行包元数据和许可证文件为准，并同步更新本文件。

## External runtime components

- Playwright Chromium 由用户按 Playwright 的安装流程获取，不包含在 Python wheel 中。
- FFmpeg/FFprobe 不由本项目自动安装，也不作为本仓库的发布内容；不同构建可能适用 LGPL 或 GPL，
  使用者应遵守自己安装的发行版许可证。
- faster-whisper 模型权重不是本项目代码的一部分。每个模型的模型卡、权重许可和使用限制可能不同，
  使用者必须在下载和传播前单独核对。

第三方名称和商标仅用于说明兼容性，不表示项目获得其背书或隶属关系。

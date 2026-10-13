# Python 开发环境与依赖管理

> 目标：把一次性脚本逐步变成可以安装、测试、交付和复现的 Python 项目。建议用时 60–90 分钟。

## 1. 从运维脚本到可交付服务

Shell/Python 脚本经常依赖“这台机器已经装了什么”。服务工程化则要求另一位开发者在干净环境中也能按步骤安装、运行和测试。

可复现性主要依赖：

- **明确的 Python 版本**：避免不同解释器的语法和标准库差异。
- **隔离的依赖环境**：不同项目可以使用不同版本的库。
- **声明式依赖**：依赖应记录在项目配置，而不是只存在于个人电脑。
- **自动化验证**：安装后能够运行测试和静态检查。

## 2. 虚拟环境是什么

`.venv` 是项目专属的 Python 环境。它让项目依赖与系统 Python、其他项目分离，但它不是容器，也不隔离操作系统、内核或网络。

在仓库根目录执行：

```bash
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip --version
```

Windows PowerShell 激活命令：

```powershell
.\.venv\Scripts\Activate.ps1
```

检查当前解释器：

```bash
which python
python -c "import sys; print(sys.executable)"
```

预期解释器路径指向仓库下的 `.venv`。如果没有激活环境，仍可显式使用 `.venv/bin/python`。

退出环境：

```bash
deactivate
```

不要把 `.venv/` 提交到 Git；不同机器的虚拟环境通常不可直接复用。

## 3. 为什么用 `python -m pip`

`pip` 命令可能指向另一个 Python 环境。使用 `python -m pip` 可以让 pip 由当前选中的解释器执行，减少“装上了却导入失败”的问题。

```bash
python -m pip install --upgrade pip
python -m pip list
python -m pip show fastapi
```

## 4. 项目依赖与 editable install

先检查仓库根目录的 `pyproject.toml`，确认项目名、Python 版本、运行依赖和开发依赖。不要在未检查配置前随意新增重复的依赖清单。

本仓库的起步安装方式：

```bash
python -m pip install -e ".[dev]"
```

其中：

- `-e` 表示 editable install：开发时，源代码修改通常无需重新安装即可被当前环境导入。
- `.` 表示当前目录是待安装项目。
- `[dev]` 表示安装项目配置中声明的开发依赖组/可选依赖。其具体语义由 `pyproject.toml` 决定。

Editable install 不会自动锁定所有传递依赖版本，也不等于可重复构建的锁文件。团队项目应根据使用的工具制定依赖锁定和升级策略。

## 5. 常见故障排查

### `ModuleNotFoundError`

按顺序检查：

1. 当前解释器是否来自预期的 `.venv`。
2. 是否在正确的仓库根目录。
3. 包是否声明在 `pyproject.toml`。
4. 是否执行了项目安装。
5. 导入名称是否与实际 Python 包目录一致。

### `pip install` 成功，但应用仍导入旧代码

检查是否使用了另一个虚拟环境、另一个终端或 IDE 解释器。用 `sys.executable` 和 `python -m pip show 包名` 确认环境。

### 依赖升级后测试失败

不要先删除测试或把所有版本升级到最新版。先查看依赖变更、错误堆栈和官方变更日志，再最小化升级范围并运行测试。

## 6. 动手任务

1. 创建虚拟环境并确认解释器路径。
2. 安装项目及开发依赖。
3. 运行 `python -m pip list`，找出 FastAPI、pytest、Ruff 等工具。
4. 退出并重新激活虚拟环境，确认命令仍能运行。
5. 查看 `pyproject.toml`，用自己的话解释运行依赖与开发依赖的区别。

## 7. 验收标准

- [ ] 能说明虚拟环境解决什么问题、不能解决什么问题。
- [ ] 能解释 `python -m pip` 相比直接运行 `pip` 的价值。
- [ ] 能找到项目依赖声明的位置。
- [ ] 能从干净终端按文档复现安装步骤。

## 参考资料

- [Python：虚拟环境与包](https://docs.python.org/3/library/venv.html)
- [Python Packaging User Guide](https://packaging.python.org/)
- [pip 用户指南](https://pip.pypa.io/en/stable/user_guide/)

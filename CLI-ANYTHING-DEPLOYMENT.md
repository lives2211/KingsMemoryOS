# CLI-Anything 部署完成

## 项目简介

**CLI-Anything**: 让任何软件变成 Agent 可用的 CLI 工具

> "Today's Software Serves Humans. Tomorrow's Users will be Agents."

通过一行命令，将任何软件（GIMP、Blender、LibreOffice 等）变成 Agent 可用的结构化 CLI 工具。

## 核心特性

| 特性 | 说明 |
|------|------|
| **结构化输出** | JSON + 人类可读格式 |
| **REPL 模式** | 交互式命令行 |
| **真实后端** | 调用实际软件，不是模拟 |
| **自动化生成** | 7 阶段流水线自动生成 CLI |
| **1,436+ 测试** | 100% 通过率 |

## 已部署示例

| 软件 | 领域 | 测试数 |
|------|------|--------|
| GIMP | 图像编辑 | 107 |
| Blender | 3D 建模 | 208 |
| Inkscape | 矢量图形 | 202 |
| Audacity | 音频处理 | 161 |
| LibreOffice | 办公套件 | 158 |
| OBS Studio | 直播录制 | 153 |
| Kdenlive | 视频编辑 | 155 |
| Shotcut | 视频编辑 | 154 |
| Draw.io | 图表绘制 | 138 |
| **总计** | | **1,436** |

## 部署位置

```
~/.openclaw/skills/cli-anything/
├── commands/           # 命令定义
├── HARNESS.md          # 方法论 SOP
├── README.md           # 插件文档
├── QUICKSTART.md       # 快速开始
├── PUBLISHING.md       # 发布指南
├── repl_skin.py        # 统一 REPL 界面
└── scripts/            # 辅助脚本
```

## 工作原理

### 7 阶段流水线

1. **🔍 Analyze** - 扫描源代码，映射 GUI 到 API
2. **📐 Design** - 设计命令组、状态模型、输出格式
3. **🔨 Implement** - 构建 Click CLI（REPL、JSON、undo/redo）
4. **📋 Plan Tests** - 创建 TEST.md 测试计划
5. **🧪 Write Tests** - 实现完整测试套件
6. **📝 Document** - 更新 TEST.md 结果
7. **📦 Publish** - 创建 setup.py，安装到 PATH

### 架构

```
用户命令 → CLI (Click) → 项目文件生成 → 真实软件调用 → 输出
                ↓
            REPL 模式 (交互式)
                ↓
            JSON 输出 (Agent 消费)
```

## 使用方法

### 为 OpenClaw 生成 CLI

```bash
# 分析软件并生成 CLI
/cli-anything <software-path>

# 示例：为 GIMP 生成 CLI
/cli-anything /usr/share/gimp

# 安装到 PATH
cd gimp/agent-harness && pip install -e .

# 使用
cli-anything-gimp --help
cli-anything-gimp --json project new -o poster.json
```

### REPL 模式

```bash
$ cli-anything-gimp
╔══════════════════════════════════════════╗
║       cli-anything-gimp v1.0.0          ║
║     GIMP CLI for AI Agents              ║
╚══════════════════════════════════════════╝

gimp> project new --width 1920 --height 1080
✓ Created project

gimp> layer add -n "Background" --type solid --color "#1a1a2e"
✓ Added layer

gimp> export render output.png
✓ Rendered: output.png
```

### JSON 输出（Agent 使用）

```bash
$ cli-anything-gimp --json project info
{
  "name": "poster",
  "width": 1920,
  "height": 1080,
  "layers": 3,
  "modified": true
}
```

## 为 OpenClaw 适配

### 当前状态

- ✅ 插件已复制到 `~/.openclaw/skills/cli-anything/`
- ⚠️ 需要适配 OpenClaw 插件格式
- ⚠️ 需要测试与 OpenClaw 的集成

### 下一步

1. **创建 OpenClaw SKILL.md**
   - 定义 OpenClaw 可用的命令
   - 配置参数和选项

2. **测试示例 CLI**
   - 选择已生成的示例（如 GIMP）
   - 安装并测试功能

3. **集成到 Agent 工作流**
   - 让 Agent 能够调用 CLI 工具
   - 处理 JSON 输出

## 应用场景

### 1. 让 Agent 使用专业软件

```
Agent: "创建一个 1920x1080 的海报，背景深蓝色"
→ cli-anything-gimp project new --width 1920 --height 1080
→ cli-anything-gimp layer add --type solid --color "#1a1a2e"
→ cli-anything-gimp export render poster.png
```

### 2. 自动化文档处理

```
Agent: "将这份数据生成 PDF 报告"
→ cli-anything-libreoffice document new --type writer
→ cli-anything-libreoffice writer add-table --rows 10 --cols 5
→ cli-anything-libreoffice export render report.pdf
```

### 3. 视频编辑自动化

```
Agent: "剪辑这段视频，添加转场效果"
→ cli-anything-kdenlive project new
→ cli-anything-kdenlive clip add -i input.mp4
→ cli-anything-kdenlive transition add --type dissolve
→ cli-anything-kdenlive export render output.mp4
```

## 关键设计原则

1. **使用真实软件**
   - 调用实际应用（GIMP、Blender 等）
   - 不是模拟或替代

2. **生成有效项目文件**
   - ODF、MLT XML、SVG 等
   - 原生渲染器处理

3. **双重输出模式**
   - 人类可读（表格、进度条）
   - 机器可读（JSON）

4. **零妥协依赖**
   - 真实软件是硬性要求
   - 测试失败（而非跳过）当后端缺失

## 资源链接

- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **HARNESS.md**: 方法论 SOP
- **QUICKSTART.md**: 5 分钟快速开始
- **PUBLISHING.md**: 发布指南

## 部署时间

2026-03-11

---

**CLI-Anything**: *Make any software with a codebase Agent-native.*

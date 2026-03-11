# 📁 文件存储规范

## 核心规则

**安装/下载的文件 → 尽量放 `/media/fengxueda/D/`**

## 原因
- 节省系统盘空间
- 数据更安全（独立分区）

## 要求

1. **OpenClaw 必须能完整使用** - 所有功能必须正常工作
2. 涉及路径的配置文件需要相应更新
3. 如果有依赖冲突，优先保证 OpenClaw 正常工作

## 常见场景

| 场景 | 存放位置 |
|------|----------|
| 模型文件大模型 | /media/fengxueda/D/models |
| 下载的安装包 | /media/fengxueda/D/downloads |
| 项目代码 | /media/fengxueda/D/projects |
| 数据/缓存 | /media/fengxueda/D/data |

---

> ⚠️ 前提：OpenClaw 功能不能受影响
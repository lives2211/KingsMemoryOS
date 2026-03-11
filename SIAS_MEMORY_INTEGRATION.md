# SIAS + memory-lancedb-pro 集成指南

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    记忆系统分层                          │
├─────────────────────────────────────────────────────────┤
│  Layer 1: SIAS (文件系统)                                │
│  - 快速写入 (WAL 协议)                                   │
│  - 结构化日志 (.learnings/)                              │
│  - 手动升级 (MEMORY.md)                                  │
│  - 适合: 即时学习、错误记录、用户纠正                    │
├─────────────────────────────────────────────────────────┤
│  Layer 2: memory-lancedb-pro (向量数据库)                │
│  - 自动嵌入 (Jina Embeddings)                            │
│  - 混合检索 (Vector + BM25)                              │
│  - 智能召回 (Auto-Recall)                                │
│  - 适合: 语义搜索、跨会话记忆、自动关联                  │
└─────────────────────────────────────────────────────────┘
```

## 工作流程

### 场景 1: 用户纠正
```
用户: "用 pnpm 而不是 npm"
    ↓
[SIAS] 立即写入 CORRECTIONS.md (WAL 协议)
    ↓
[memory-lancedb-pro] 自动捕获 (autoCapture)
    ↓
两者都有记录 → 冗余但互补
```

### 场景 2: 知识查询
```
用户: "我之前说过用什么包管理器？"
    ↓
[memory-lancedb-pro] 语义搜索 → 找到 "pnpm"
    ↓
[SIAS] 读取 MEMORY.md → 确认 "pnpm"
    ↓
双重验证 → 高置信度回答
```

### 场景 3: 知识升级
```
SIAS: 同一纠正出现 3 次
    ↓
升级到 MEMORY.md
    ↓
同时写入 memory-lancedb-pro (手动调用 memory_store)
    ↓
两个系统同步
```

## 配置协同

### 1. SIAS 配置 (SOUL.md)

在 SIAS 的 SOUL.md 中添加 memory-lancedb-pro 集成规则:

```markdown
### 5. MEMORY-LANCEDB-PRO 集成

**何时使用 memory_store:**
- 知识升级到 MEMORY.md 时
- Critical 优先级的学习
- 需要跨 Agent 共享的知识

**集成流程:**
1. 写入 .learnings/ (SIAS)
2. 升级到 MEMORY.md (SIAS)
3. 调用 memory_store (memory-lancedb-pro)
4. 两者同步完成

**避免重复:**
- SIAS 记录详细日志 (为什么学)
- memory-lancedb-pro 记录语义向量 (快速检索)
- 两者互补，不是竞争
```

### 2. memory-lancedb-pro 配置

已在 `openclaw.json` 中配置:
- `autoCapture: true` - 自动捕获对话
- `autoRecall: true` - 自动召回相关记忆
- `smartExtraction: true` - 智能提取关键信息

## 使用建议

### 日常使用流程

1. **即时学习** → SIAS (快速写入)
   ```
   用户纠正 → 立即写入 .learnings/CORRECTIONS.md
   ```

2. **定期整理** → SIAS + memory-lancedb-pro
   ```
   每天/每周: 回顾 .learnings/ → 升级重要知识 → 同步到向量库
   ```

3. **知识查询** → memory-lancedb-pro (语义搜索)
   ```
   需要找相关信息 → 自动语义搜索 → 返回最相关的记忆
   ```

4. **深度审计** → SIAS (结构化日志)
   ```
   需要分析错误模式 → 读取 ERRORS.md → 找出改进点
   ```

## 最佳实践

### DO (推荐)
- ✅ 用 SIAS 记录详细的上下文 (为什么学、怎么错的)
- ✅ 用 memory-lancedb-pro 做快速语义检索
- ✅ 定期将 SIAS 的重要知识同步到向量库
- ✅ 两个系统互补，不重复造轮子

### DON'T (避免)
- ❌ 只在 SIAS 记录，不利用向量检索
- ❌ 只在向量库记录，没有结构化日志
- ❌ 两个系统记录完全一样的内容
- ❌ 忽视 SIAS 的 WAL 协议 (先保存，后回复)

## 集成检查清单

### 部署检查
- [ ] SIAS 文件结构完整 (SOUL.md, MEMORY.md, .learnings/)
- [ ] memory-lancedb-pro 已启用 (openclaw.json)
- [ ] Jina API Key 已配置
- [ ] 所有 Agent 都有 SIAS 部署

### 功能检查
- [ ] SIAS WAL 协议执行正确
- [ ] memory-lancedb-pro 自动捕获工作
- [ ] memory-lancedb-pro 自动召回工作
- [ ] 两者数据不冲突

### 协同检查
- [ ] 知识能从 SIAS 同步到向量库
- [ ] 查询能同时利用两个系统
- [ ] 日志清晰区分来源

## 故障排除

### 问题: SIAS 和 memory-lancedb-pro 记录重复
**解决**: 这是正常的。SIAS 记录详细日志，向量库记录语义。两者互补。

### 问题: memory-lancedb-pro 没有捕获某些学习
**解决**: 检查 `autoCapture` 是否启用，或手动调用 `memory_store`。

### 问题: SIAS 文件写入失败
**解决**: 检查文件权限，确保 Agent 有写入 workspace 的权限。

## 总结

| 系统 | 优势 | 使用场景 |
|------|------|---------|
| **SIAS** | 结构化、详细、可控 | 错误记录、用户纠正、自我审计 |
| **memory-lancedb-pro** | 语义搜索、自动、智能 | 快速检索、跨会话关联、自动召回 |

**两者结合 = 结构化日志 + 智能检索 = 完美的记忆系统**

---

*集成配置完成时间: 2026-03-10*

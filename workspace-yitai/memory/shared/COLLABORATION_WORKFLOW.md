# COLLABORATION_WORKFLOW - 深度协作流程

## 🕐 每日时间线

### 08:00 - Dwight情报收集
```
产出：intel/DAILY-INTEL.md
动作：@Kelly @Rachel "今日Top3：X/Y/Z，需要我深挖哪个？"
等待：15分钟内必须收到具体反馈
补充：根据反馈更新情报
确认：双方确认"足够用了"
```

### 09:00 - Kelly内容创作
```
读取：intel/DAILY-INTEL.md + 昨晚反馈
产出：memory/drafts/YYYYMMDD-tweets.md
动作：@Dwight @Angela "事实准确吗？风格OK吗？"
等待：10分钟内反馈
修改：根据反馈调整
确认：Dwight确认数据，Angela确认质量
```

### 09:30 - 每日站会（文字版）
```
主持：Monica
时长：最多15分钟
格式：
  Dwight: "今日重点A/B/C，@Kelly @Rachel 需要深挖吗？"
  Kelly: "我要B的更多数据"
  Rachel: "我做A的深度分析"
  Ross: "今天修X，@Angela 下午测试"
  Angela: "昨日审计发现..."
  Pam: "简报我会突出..."
  Monica: "总结：A→Rachel深度，B→Kelly热点，其他按计划"
```

### 14:00 - Dwight下午补充
```
快速扫描新动态
追加到DAILY-INTEL.md的"Afternoon Update"
如有重大变化，@相关人
```

### 18:00 - Angela审计
```
检查今日所有产出
发现问题 → 立即@相关人
产出：agents/angela/memory/audit-YYYYMMDD.md
```

### 18:30 - Pam综合简报
```
读取所有Agent产出
编制：intel/briefings/YYYYMMDD.md
汇总要点，@用户汇报
```

---

## 🎯 关键协作节点

### 节点1：情报→内容
```
Dwight ──@──> Kelly/Rachel
         "够你们用吗？缺什么？"
         
Kelly/Rachel ──反馈──> Dwight
         "我需要X的角度" / "建议补充Y"
         
Dwight ──更新──> 最终情报
         双方确认"足够用了"
         
Kelly/Rachel ──开始创作──> 各自产出
```

### 节点2：内容→审核
```
Kelly/Rachel ──草稿──> @Dwight @Angela
         "事实准确吗？风格OK吗？"
         
Dwight ──验证──> "数据准确"
Angela ──质检──> "建议修改X"
         
Kelly/Rachel ──修改──> 终稿
         再次@确认
         
Angela ──通过──> 可以发布
```

### 节点3：质疑→解决
```
Angela发现Kelly数据问题
         ↓
Angela: "@Kelly 这条'暴涨23%'数据来源？"
         ↓
Kelly: "来自Nitter，我补充备注"
Dwight: "我去6551验证"
         ↓
5分钟内解决 → 继续
或升级Monica → 暂停等待
```

---

## ⚡ 紧急响应

### Level 1 - 群内解决（5分钟）
- 简单疑问、小修改
- 相关Agent直接对话
- Monica旁观，不介入

### Level 2 - Monica仲裁（10分钟）
- 分歧未决、需要决策
- @Monica请求判断
- Monica给出明确指令

### Level 3 - 用户决策（立即）
- 重大风险、方向争议
- Monica@用户请示
- 等待用户回复

---

## 📊 质量检查点

| 检查点 | 负责人 | 标准 |
|--------|--------|------|
| 数据来源 | Dwight | 每个数字必须有来源链接 |
| 事实准确 | Angela | 交叉验证，标记[UNVERIFIED] |
| 风格一致 | Kelly/Rachel | 符合平台调性，无emoji |
| 技术可行 | Ross | 代码有测试输出 |
| 整体协调 | Monica | 无重复，角度互补 |

---

## 🔄 每周五复盘

1. **数据统计**
   - 各Agent产出数量
   - @反馈响应时间
   - 返工次数

2. **问题回顾**
   - 本周最大的沟通障碍
   - 最成功的协作案例

3. **共识更新**
   - 更新SHARED_UNDERSTANDING.md
   - 记录新形成的默契

4. **流程优化**
   - 哪些环节可以简化
   - 哪些需要加强
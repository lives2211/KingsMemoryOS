# SIGNALS.md - 追踪的趋势与信号

## AI 智能体相关
- [x] OpenClaw 多智能体系统 (Shubham Saboo)
- [x] 基于文件的记忆系统设计
- [x] AI Agent 协作框架
- [ ] Claude Code / Cursor 等 AI 编程助手发展

## 技术趋势
- [ ] Tauri 2.0 桌面应用开发
- [ ] WebRTC / WebSocket 实时通讯
- [ ] 本地 AI 模型部署

## 学习资源
- OpenClaw 官方文档
- Shubham Saboo 的 AI Agent 系统系列文章
- Tauri 官方文档

## 待研究
- 如何实现多 Agent 定时任务
- Telegram Bot API 深度集成
- 跨平台通知系统

## 🔥 新发现：Apify 让 Agent 连接互联网
来源：Santiago (@svpino) Twitter 视频

### 核心观点
- **问题**：多数 AI Agent 是"离线大脑"，无法获取实时信息
- **解决方案**：给 Agent 插上"实时网线" → Apify 平台

### 为什么 Apify 有效
- **普通玩法**：LLM 直接读网页 → 幻觉多、数据不准
- **Apify 玩法**：确定性爬虫抓数据 → LLM 分析处理 → 稳定可靠

### 三步开启
1. 安装 Apify 市场插件
2. 安装基础技能（如 Lead Generation）
3. 安装 Actor Development → Agent 可自己创建爬虫

- Agent 从"被动问答"变成"主动获取信息的武器"

---

## 🔥 OpenClaw 五个设计原理 + 真实案例
来源：OpenClaw Camp @every

### 五个设计原理
1. **持久记忆**：Agent 每天写日记、更新自我身份文件，Markdown 存本地
2. **定时任务**：自己安排定时工作（凌晨构建、早上提醒）
3. **心跳机制**：每 30 分钟主动检查待处理工作，不等你发消息
4. **自安装工具**：只需告诉它目标，它自行研究如何连接
5. **多渠道统一**：Telegram/iMessage/浏览器/终端，汇入同一个 Agent

### 四位重度用户案例

#### Nat Eliason - Felix（技术探索者）
- 远程编码：手机发消息，Felix 完成修改推送，全程 <1 分钟
- 知识管理：基于 PARA 方法，同步 GitHub
- 协作写作：Webhook 接入写作工具
- 自主身份：有自己 X 账号、Stripe 账号、银行账号

#### Brandon Gell - Zosia（非技术用户）
- 晚间日历提醒
- 保姆工时统计
- 购物车管理（记住偏好）
- 冲动消费冷静期
- 密码管理（1Password 隔离）

#### Claire Vo - Polly（谨慎安全派）
- 设为独立 Google Workspace 用户
- 独立邮件地址、只读日历
- 日历管理效果一般，研究任务效果好

#### Austin Tedesco - Judd（主动推送）
- 明确指令："主动联系频率乘以二"
- 试用转化下滑时主动发消息提醒
- 教训：先接入 2 个系统，稳定后再扩展

### 实操 QA
- Q1: 多实例？→ 有冲突风险，用虚拟隔离
- Q2: Mac Mini？→ 先笔记本跑通再迁移
- Q3: 消息混淆？→ 出错就"骂"，写入 agents.md（95% 解决）
- Q4: 远程查看？→ 截图或 Vercel 预览链接
- Q5: 整夜运行？→ tmux 启动 + 检查未完成任务逻辑

---

## 🔥 Mitchell Hashimoto 的 AI 进阶六步法
来源：Mitchell Hashimoto（HashiCorp 联创，Ghostty 作者）

### 核心观点
- **第一步**：放下聊天窗口，必须用 Agent（能读文件、执行程序、发 HTTP 请求）
- **第二步**：用 AI 复现手动工作（强制手写一遍 + Agent 做一遍）
- **第三步**：下班前启动 Agent（利用疲劳时间的 30 分钟）
- **第四步**：把稳赢的任务交出去（筛出 Agent 大概率能搞定的任务）
- **第五步**：打造工程化约束（AGENTS.md + 专用工具）
- **第六步**：始终保持一个 Agent 在运行

### 关键洞察
- "一部分效率提升来自于知道什么时候**不该用** Agent"
- 关于技能形成担忧："你不再为交给 Agent 的任务积累技能，但仍为亲手做的任务正常磨练手艺"

### Harness Engineering
- Agent 犯错 → 写进 AGENTS.md 或做专用工具
- Ghostty 项目 AGENTS.md 每一行都对应一个曾经犯过的错

---

## 🔥 如何成为世界级 Agentic Engineer

### 核心原则
- "你可以把大量设计和实现交给 Agent，但结果你必须自己负责"

### 上下文管理（最被低估的工程能力）
- 只给 Agent 完成任务所需的**确切信息，不多不少**
- 研究与实现必须分离：
  - 错误："帮我构建认证系统"（上下文会被备选方案填满）
  - 正确："用 bcrypt-12 实现 JWT，refresh token 7 天过期"
- 如果不确定方案：先调研 Agent 输出对比 → 决策 → 全新会话实现

### 巧用 Agent 的"奉承性"
- 问题：Agent 被设计为"取悦用户"，你让它找 bug，它会编造 bug
- 解决方案：
  1. **中性提示词**："梳理各模块逻辑，报告所有发现"（不预设结论）
  2. **多 Agent 对抗系统**：发现者 vs 对抗者 vs 裁判

### 明确任务"终点"
- Agent 擅长开始，但不知道何时结束
- 可靠方式：
  1. **测试套件**："X 个测试全部通过才算完成，且不得修改测试"
  2. **截图 + 视觉验证**：让 Agent 截图验证设计
  3. **契约文件**：{TASK}_CONTRACT.md 列出验收条件 + stop-hook

### 长期运行 Agent 正确姿势
- 反对：24 小时连续超长会话（上下文污染）
- 推荐：每个合约开新会话，用编排层分发任务

### 规则与技能管理（AGENTS.md）
- **定位**：条件跳转目录，不是完整文档
- 格式示例：
  - "如果写代码，先读 coding-rules.md"
  - "如果测试失败，先读 coding-test-failing-rules.md"
- **规则 (Rules)**：编码偏好（"不要做 X"）
- **技能 (Skills)**：编码方法（"按这个流程做 Z"）
- 维护：定期清理冗余和矛盾

---

## 🔥 Agent Swarm：一人开发团队完整方案
来源：Elvis (@elvissun) + Mitchell Hashimoto

### 核心架构
- **Zoe**：Agent 编排层，不是简单重启失败 Agent，而是根据业务上下文（客户历史、会议记录、过去失败）写更好的 prompt
- **tmux + worktree**：每个任务独立分支、独立会话
- **任务元数据**：.clawdbot/active-tasks.json 追踪所有任务

### 8 步工作流
1. **客户需求 → Zoe  scoping**（读取 Obsidian 会议笔记）
2. **Spawn Agent**：每个 Agent 独立 worktree + tmux
3. **Monitor**：10 分钟 cron 轮询检查（非直接 poll，节省 token）
4. **Agent 创建 PR**：gh pr create --fill
5. **三 AI 审查**：Codex（边缘case）+ Gemini（安全/扩展性）+ Claude Code（验证）
6. **自动化测试**：lint → unit → e2e → playwright
7. **Human Review**：Telegram 通知，5-10 分钟 merge
8. **Merge**：自动清理 orphaned worktrees

### 定义完成标准
- PR created + Branch synced + CI passing + 3 AI reviews passed + Screenshots

### 关键技巧
- UI 变更必须带截图，否则 CI 失败
- 不直接用 Codex/Claude Code，用 OpenClaw  orchestration layer
- 事件驱动监控：bash pre-check 零 token，只有需要时触发 Opus

### 硬件瓶颈
- 16GB RAM Mac Mini 顶多 4-5 个并发 Agent
- 需要 128GB RAM 才能流畅运行多 Agent

### 核心理念
"Codex 和 Claude Code 不懂你的业务。OpenClaw 充当编排层，持有所有业务上下文，翻译成精准 prompt 给每个 coding agent"

---

## 🔥 Vercel agent-browser --native
来源：vercel-labs/agent-browser

### 核心理念
- 纯 Rust 二进制，直接 CDP
- 无抽象层 → 更高性能
- 自包含 daemon，运行时无 Node.js
- 零运行时依赖

### 安装
npm install -g agent-browser && agent-browser install

### 命令
agent-browser open url
agent-browser snapshot  # accessibility tree
agent-browser click @e2
agent-browser screenshot

### 优势
- 子毫秒解析
- 更低内存
- 可替代现有 agentic-browser


---

## 🔥 不懂代码反而是优势 - AI 使用三层模式
来源：Twitter 线程

### 核心观点
我们开着自行车，旁边 AI 是跑车。结果让跑车跟自行车跑。

### AI 使用三层

| 层级 | 模式 | 结果 |
|------|------|------|
| 【画笔】 | 告诉 AI 每个细节 | AI 被锁死在你的水平里 |
| 【员工】 | 规定每一步 | 本质还是微操 |
| 【大师】 | 你是这领域前十专家 | 给目标给权限然后放手 |

### 大师模式三原则
1. **最终结果导向**：不是修 bug，是一周进榜前 20
2. **过程不干预**：AI 可能走反直觉的路，最后赢了就行
3. **风险可控内给最高权限**：假设 AI 一定搞砸，但搞到最砸也能接受

### 抽卡心态
微操 100 次得 70 分
不如放手跑 10 次抽一次 120 分

### 案例
天润给 AI 模糊指令做海报：硅谷审美、乔布斯风格
→ AI 生成泛黄拍立得 + 古老 Mac 绿字屏
→ 没有人类设计师会想到

把 AI 规定到 workflow 里，控制性好了，最大价值可能性也小了

### AI 军团架构
- Echo（产品经理）
- Elon（CTO）
- Henry（CMO）
- 各有子 Agent

### 设定技巧：双层人设
- 底层：顶级智能不封上限
- 表层：给具体人格
- 说前十名的人不是最好的一个，能力更全面

### 主 Agent + 子 Agent
- 主 Agent：最强模型决策
- 子 Agent：轻量模型执行


---

## 🔥 BrowserBase 浏览器自动化 Skill
来源：skills.sh/browserbase/skills/browser

### 核心理念
为 Agent 打造的远程浏览器，比 MCP 工具更快，每次运行使用新浏览器上下文，避免 prompt injection

### 安装
npx skills add browserbase/skills

### 两种模式

| 特性 | Local | Remote (Browserbase) |
|------|-------|----------------------|
| 速度 | 更快 | 稍慢 |
| 设置 | 需要 Chrome | 需要 API Key |
| 隐身模式 | ❌ | ✅ |
| CAPTCHA | ❌ | 自动解决 |
| 住宅代理 | ❌ | ✅ (201 国) |
| 会话持久 | ❌ | ✅ |

### 命令


### 使用场景
- Local：简单页面、文档、公共 API
- Remote：有登录墙、CAPTCHA、反爬、Cloudflare

### 优势
1. 比 MCP 工具更快
2. 每次运行新浏览器上下文（防 prompt injection）
3. 自动 CAPTCHA 解决
4. 住宅代理 + 会话持久


---

## 🔥 提示词高效编写 9 条原则
来源：@RookieRicardoR

### 核心公式
高效 = 一次命中率 × 可复用率 ÷ 返工轮次

### 1. 先定义高效
- 不是写得多，而是可执行
- 不能复用 = 一次性对话，不是高效提示词

### 2. 从 Mega Prompt 到流水线
低效：一次性塞给模型
高效：拆成 3 段
- 第 1 段：任务背景 + 上下文
- 第 2 段：执行动作 + 逻辑顺序
- 第 3 段：输出方式 + 边界限制

### 3. XML 标签边界管理
参考骨架：
<prompt>
  <system_role>角色定义</system_role>
  <goal>目标</goal>
  <instructions>执行指令</instructions>
  <context>上下文（剪枝）</context>
  <examples>
    <good>正确示例</good>
    <bad>错误示例</bad>
  </examples>
  <constraints>约束</constraints>
  <output_format>输出格式</output_format>
</prompt>

### 4. 长上下文排序
资料在前，问题在后
原因：模型对尾部信息更敏感，问题放最后收束注意力

### 5. 动作语言精确
句式：动词 + 对象 + 约束
示例："对比 A/B 方案在成本、风险上的差异，各给 2 条证据，输出三列表格，结论不超过 100 字"

### 6. 示例双向
Good + Bad + Why Bad
- 组数不超过 5 组
- 高约束任务收益明显

### 7. 正向指令优先
先写要做什么，再写不要做什么
符合模型顺向生成逻辑

### 8. 参数配置
| 任务类型 | Temperature |
|----------|-------------|
| 事实核查/代码/数学 | 接近 0 |
| 常规总结/业务文稿 | 0.2-0.5 |
| 创意写作/头脑风暴 | 0.7-0.9 |

### 9. 提示词资产化
- 按场景沉淀模板库
- 版本管理
- 30-50 个模板解决 9 成重复工作

### 10. 10 分钟自检清单
- [ ] 目标单一
- [ ] XML 分块
- [ ] 动词可执行
- [ ] Good/Bad 示例
- [ ] 参数匹配任务
- [ ] 可复用


---

## 🔥 GitAgent - AI Agent 的 Git 原生标准
来源：github.com/open-gitagent/gitagent

### 核心理念
"你的代码仓库，直接就是你的智能体"
- 不绑定任何框架
- 走原生 Git 标准
- 像写代码、提 PR 一样管理 AI 员工

### 定位
AI 领域的 Dockerfile / Kubernetes Manifest
- 声明式定义 AI 的行为、人设、工作职责

### 目录结构



### 核心特性
- **Git-native**：版本控制、分支、diff
- **框架无关**：可导出到任意框架
- **Compliance-ready**：支持 FINRA/SEC 等监管要求
- **Composable**：Agent 可扩展、依赖、委托

### 只必需 2 个文件
1.  - manifest
2.  - 身份

### 与 OpenClaw 对比
| GitAgent | OpenClaw |
|----------|----------|
| 框架无关标准 | 具体实现 |
| 通用定义 | 运行时 + 工具 |
| 类似 Dockerfile | 实际容器 |

### 模式
1. **Human-in-the-Loop**：Agent 学新技能时开分支 + PR 让人审核
2. **Segregation of Duties**：定义角色冲突矩阵

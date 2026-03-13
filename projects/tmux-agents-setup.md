# OpenClaw + 多Agent协作配置指南

## 已安装的CLI工具

### 1. Codex CLI (OpenAI)
```bash
# 安装
npm install -g @openai/codex

# 配置 (已购买会员，无需API Key)
codex --version
```

### 2. Claude Code (Anthropic)
```bash
# 安装
npm install -g @anthropic-ai/claude-code

# 配置
claude --version
```

### 3. Gemini CLI (Google)
```bash
# 安装
npm install -g @google/gemini-cli

# 配置
gemini --version
```

## tmux 会话管理

### 创建专用会话
```bash
# Codex 会话
tmux new-session -d -s codex-agent -c /path/to/project

# Claude 会话
tmux new-session -d -s claude-agent -c /path/to/project

# Gemini 会话
tmux new-session -d -s gemini-agent -c /path/to/project
```

### 常用命令
```bash
# 查看所有会话
tmux ls

# attach到会话
tmux attach -t codex-agent

# 发送命令到会话
tmux send-keys -t codex-agent "codex" Enter

# 捕获日志
tmux capture-pane -t codex-agent -p
```

## OpenClaw 指令模板

### 启动 Codex 写代码
```
请在tmux会话"codex-agent"中启动Codex CLI，使用最强模型(o1-pro)，
授予Full Access权限，完成以下任务：
[任务描述]

要求：
1. 使用最大推理力度
2. 每10分钟汇报一次进度
3. 如果进程中断，自动重启
4. 完成后通知我进行Review
```

### 启动 Claude Code 审核
```
请在tmux会话"claude-agent"中启动Claude Code，
审核以下代码/PR：
[代码/PR链接]

要求：
1. 进行完整的代码审查
2. 检查潜在bug和安全问题
3. 提出改进建议
4. 生成审查报告
```

### 启动 Gemini 设计界面
```
请在tmux会话"gemini-agent"中启动Gemini CLI，
使用Gemini 2.5 Pro完成以下设计任务：
[设计需求]

要求：
1. 生成前端代码
2. 设计主题风格
3. 使用browser-use进行端到端测试
4. 提供设计文档
```

## 多Agent协作模式

### 模式1：串行流水线
```
User → OpenClaw → Claude(设计) → Gemini(前端) → Codex(后端) → OpenClaw(Review) → User
```

### 模式2：并行分工
```
                    ┌→ Claude(架构设计)
User → OpenClaw ──┼→ Gemini(前端开发)
                    └→ Codex(后端开发)
                         ↓
                    OpenClaw(整合Review)
```

### 模式3：讨论式协作
```
OpenClaw作为主持人，让三位Agent在各自tmux会话中：
1. 提出各自方案
2. 互相Review对方代码
3. 讨论并达成共识
4. OpenClaw汇总最终方案
```

## 监控脚本

### 自动进度检查
```bash
#!/bin/bash
# check_agents.sh

SESSIONS=("codex-agent" "claude-agent" "gemini-agent")

for session in "${SESSIONS[@]}"; do
    if tmux has-session -t "$session" 2>/dev/null; then
        echo "=== $session ==="
        tmux capture-pane -t "$session" -p | tail -20
    else
        echo "WARNING: $session is not running!"
    fi
done
```

### OpenClaw 定时检查
```
每10分钟执行：
1. 检查各tmux会话状态
2. 捕获最近日志
3. 总结当前进度
4. 如有异常，自动重启
```

## 实战示例

### 示例1：开发新功能
```
我："帮我实现用户认证系统，预算50美元"

OpenClaw：
1. 创建tmux会话
2. 派发给Claude："设计认证架构"
3. Claude完成后，派发给Codex："实现后端API"
4. 同时派发给Gemini："设计登录界面"
5. 两者完成后，互相Review
6. OpenClaw整合并测试
7. 交付成果
```

### 示例2：代码审查
```
我："Review这个PR"

OpenClaw：
1. 启动3个tmux会话
2. 让Claude检查架构设计
3. 让Codex检查实现细节
4. 让Gemini检查前端代码
5. 汇总三方意见
6. 生成审查报告
```

## 注意事项

1. **资源管理**：同时运行3个Agent很耗资源，确保机器够强
2. **成本控制**：监控各Agent的token消耗
3. **冲突处理**：定义好代码合并策略
4. **日志保留**：定期清理tmux日志，避免磁盘满

## 快捷指令

配置好后，后续只需说：
- "用tmux里的Codex写代码" → 自动进入codex-agent会话
- "让Claude Review一下" → 自动进入claude-agent会话
- "三位大哥讨论一下" → 启动三方协作模式

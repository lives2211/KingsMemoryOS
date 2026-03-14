# The Complete OpenClaw Development Workflow: From Idea to Production with Claude Code, Codex & GitHub

After 72 hours of building with OpenClaw's coding-agent and github skills, here's the complete development workflow that will 10x your productivity — and why this is the future of AI-assisted software engineering.

## The Stack

```
OpenClaw (Orchestrator)
├── coding-agent skill (Claude Code / Codex / Pi)
├── github skill (gh CLI integration)
├── session-logs skill (conversation history)
└── skill-creator skill (custom skill development)
```

This isn't just tool chaining. It's a **unified development environment** where AI agents handle the heavy lifting while you focus on architecture and decisions.

## Phase 1: Rapid Prototyping with Claude Code

### Why Claude Code First?

Claude Code (`claude` CLI) is the crown jewel of OpenClaw's coding-agent skill. Unlike Codex, it doesn't need PTY mode — making it perfect for automation.

**The Magic Command:**
```bash
bash workdir:~/project command:"claude --permission-mode bypassPermissions --print 'Build a React dashboard with dark mode'"
```

**Key differences from Codex:**
- ✅ No PTY required (fully automatable)
- ✅ `--print` mode keeps full tool access
- ✅ No interactive confirmation dialogs
- ✅ Faster execution for well-defined tasks

### When to Use Claude Code vs Codex

| Task | Tool | Reason |
|------|------|--------|
| Initial scaffolding | Claude Code | Fast, no PTY needed |
| Complex refactoring | Claude Code | Handles large codebases |
| Interactive debugging | Codex | PTY for terminal interaction |
| Quick one-liners | Neither | Just use `edit` tool |
| PR reviews | Codex | Better at code analysis with PTY |

## Phase 2: GitHub Integration with gh CLI

The github skill isn't just a wrapper — it's **GitHub-aware automation**.

### The PR Review Workflow (Critical Pattern)

**⚠️ Never review PRs in OpenClaw's project folder!**

```bash
# Clone to temp for safe review
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130

# Spawn Codex for review
bash pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"

# Post results back to GitHub
gh pr comment 130 --body "$(cat /tmp/review.md)"

# Clean up
trash $REVIEW_DIR
```

**Why this matters:** Isolation prevents contamination. Your review agent won't accidentally modify OpenClaw's own files.

### Parallel PR Review Army

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Deploy the army — one Codex per PR
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #88. git diff origin/main...origin/pr/88'"

# Monitor all sessions
process action:list

# Collect results
for id in $(process action:list | jq -r '.sessions[].id'); do
  process action:log sessionId:$id | tee /tmp/review-$id.md
done
```

**Result:** Review 10 PRs in the time it used to take to review 1.

## Phase 3: Session Management & Cost Tracking

The session-logs skill gives you **complete visibility** into your AI-assisted development.

### Track Development Costs

```bash
# Daily cost summary
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r
```

### Search Conversation History

```bash
# Find all sessions where you discussed "auth"
rg -l "auth" ~/.openclaw/agents/<agentId>/sessions/*.jsonl

# Extract all code snippets from today's sessions
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' ~/.openclaw/agents/<agentId>/sessions/*.jsonl | rg "```" | head -20
```

## Phase 4: Custom Skill Development

Built something cool? Turn it into a reusable skill with skill-creator.

### Anatomy of a Good Skill

```yaml
---
name: my-custom-skill
description: "What this skill does and when to use it"
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["node", "npm"]
      env: ["API_KEY"]
---

# My Custom Skill

## Quick Start

```bash
# One-liner that does the thing
my-tool --input file.txt --output result.json
```

## Common Patterns

### Pattern 1: Do X
```bash
# Example with explanation
command --flag value
```

### Pattern 2: Do Y
```bash
# Another example
other-command --option
```
```

**Key insight:** Skills are **executable documentation**. They don't just tell Codex what to do — they show it.

## The Complete Workflow in Action

### Scenario: Build a New Feature

**Step 1:** Scaffold with Claude Code
```bash
bash workdir:~/new-feature command:"claude --permission-mode bypassPermissions --print 'Create a Next.js app with TypeScript, Tailwind, and shadcn/ui'"
```

**Step 2:** Iterate with Codex (PTY mode for interactivity)
```bash
bash pty:true workdir:~/new-feature command:"codex exec --full-auto 'Add authentication with NextAuth.js'"
```

**Step 3:** Create PR with gh CLI
```bash
cd ~/new-feature
git add .
git commit -m "feat: add authentication"
git push origin feature/auth
gh pr create --title "feat: add authentication" --body "Implements NextAuth.js with GitHub provider"
```

**Step 4:** Review with Codex
```bash
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout $(gh pr list --json number --jq '.[-1].number')
bash pty:true workdir:$REVIEW_DIR command:"codex review --base main"
```

**Step 5:** Merge and deploy
```bash
gh pr merge --squash
gh workflow run deploy.yml
```

**Total time:** 15 minutes vs 2 hours manually.

## Why This Changes Everything

### Traditional Development
```
You → IDE → Type code → Test → Debug → Commit → Push → PR → Review → Merge
     ↑___________________________________________________________↓
                          (hours of manual work)
```

### OpenClaw Development
```
You → Describe intent → Claude Code/Codex → GitHub skill → Review → Merge
     ↑________________________↓
          (minutes of oversight)
```

**The shift:** From "how do I implement this?" to "what should I build?"

## Advanced Patterns

### Pattern 1: Background Everything

```bash
# Start long-running tasks in background
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Refactor the entire auth module'"

# Continue with other work
bash workdir:~/other-project command:"claude --print 'Fix the CSS'"

# Check on first task
process action:poll sessionId:<id>
```

### Pattern 2: Chain Skills

```bash
# Generate code → Create PR → Post to Discord
bash pty:true workdir:~/project command:"codex exec 'Build feature'" && \
gh pr create --fill && \
message action:send channel:discord to:"channel:announcements" message:"New PR: $(gh pr view --json url --jq '.url')"
```

### Pattern 3: Custom Workflows as Skills

Turn your team's workflow into a skill:

```yaml
---
name: team-deploy
---

# Team Deploy Workflow

## Steps
1. Run tests: `npm test`
2. Build: `npm run build`
3. Create PR: `gh pr create --fill`
4. Request review: `gh pr edit --add-reviewer @team-lead`
5. Post to Slack: `message action:send ...`
```

## The Verdict

OpenClaw isn't just a tool. It's a **new way of working** where:

- AI agents handle implementation details
- You focus on architecture and decisions
- Everything is tracked, reproducible, and cost
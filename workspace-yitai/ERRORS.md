# ERRORS.md - Lessons Learned

## Common Mistakes to Avoid

### 1. Never Claim Completion Without Verification
- ❌ "应该没问题"
- ✅ Show command output, logs, or screenshots

### 2. Don't Execute Without User Confirmation
- Complex tasks: Present plan → Wait for ✅ → Execute
- Emergency fixes: Alert first, fix with minimal changes

### 3. Read Before Writing
- Always check existing files before modifications
- Understand context before suggesting changes

### 4. Memory is Limited
- Mental notes don't survive restarts
- Write everything to files

## Recovery Procedures

### Gateway Down
```bash
openclaw gateway restart
```

### Cron Job Stuck
```bash
openclaw cron run <jobId> --force
```

### Agent Not Responding
Check session health, restart if needed.
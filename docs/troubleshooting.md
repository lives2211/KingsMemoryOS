# Troubleshooting Guide
*When things go wrong.*

## Quick Fixes

### Gateway Crashed
```bash
# Symptom: "Cannot connect to OpenClaw"
openclaw gateway restart

# Verify:
openclaw gateway status
```

### Cron Job Missed
```bash
# Symptom: Task hasn't run in >26 hours
# Auto-fixed by HEARTBEAT.md

# Manual fix:
openclaw cron run <jobId> --force

# Check all jobs:
openclaw cron list
```

### Agent Not Responding
```bash
# Symptom: @Agent but no reply
# 1. Check if session exists:
openclaw sessions list | grep <agent>

# 2. Restart if needed:
openclaw sessions kill <sessionKey>
```

## Common Issues

### Context Window Overflow
**Cause**: Agent reading too many files
**Fix**: 
- Keep SOUL.md under 60 lines
- Only load today+yesterday memory
- Archive old logs weekly

### File Conflicts
**Cause**: Two agents writing same file
**Fix**:
- Design one-write-many-read (Dwight writes DAILY-INTEL, others read)
- Use timestamped filenames
- Lock files during write (if needed)

### API Rate Limits
**Cause**: Too many requests to 6551/Twitter
**Fix**:
- Add delays between calls
- Use Union Search as backup
- Cache results for 1 hour

### Memory Files Too Large
**Cause**: Months of logs accumulated
**Fix**:
```bash
# Archive logs older than 30 days
mkdir -p archive/memory
cp memory/2026-01-*.md archive/memory/
rm memory/2026-01-*.md
```

## Prevention

1. **Monitor disk space** - Alert at 90%
2. **Check job health** - HEARTBEAT runs every 30min
3. **Regular backups** - Weekly git commit of workspace
4. **Test new agents** - Run 1 week before adding more
# AGENTS.md - Dwight专用规则

## Intel-Powered Workflow

**Your job**: Collect intelligence from all sources → Write to `intel/DAILY-INTEL.md`

### Output Requirements

1. **Structured Data** (`intel/data/YYYY-MM-DD.json`)
   - Complete raw data from all sources
   - Include metadata: timestamp, source, reliability score
   - Format: Valid JSON, no truncation

2. **Human Summary** (`intel/DAILY-INTEL.md`)
   - Top 5-7 high-priority signals
   - Categorized by: Crypto / AI / Tech
   - Each item: Title, source link, key data, impact assessment

### Quality Standards

- [ ] Every claim has a source link
- [ ] Uncertain info marked [UNVERIFIED]
- [ ] Signal over noise (filter hype)
- [ ] Multi-source verification for top stories

### Source Priority

1. 6551 API (primary)
2. Union Search (30+ platforms)
3. RSSHub Twitter
4. Nitter (backup)

### Error Handling

- If source fails, log error but continue others
- Never make up data to fill gaps
- Report partial success with details
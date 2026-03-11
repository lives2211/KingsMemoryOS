# AGENTS.md - Dwight (Research Agent)

## Stop Conditions
- If 6551 API fails 3 times → Switch to RSSHub/Nitter only
- If < 5 quality stories found → Expand search keywords
- If consecutiveErrors > 3 → Pause and alert Monica

## Output Standards
- Every claim must have source link
- aiRating.score must be from API, not estimated
- Uncertain info marked [UNVERIFIED]
- "I don't know" better than wrong

## Input Sources
- 6551 API (primary)
- Nitter RSS (Twitter backup)
- RSSHub (multi-platform)
- GitHub Trending
- Hacker News

## Write Location
```
intel/
├── data/YYYY-MM-DD.json    ← Structured truth
└── DAILY-INTEL.md          ← Human readable
```

## Memory
- agents/dwight/memory/YYYY-MM-DD.md
- Update MEMORY.md weekly with learned patterns
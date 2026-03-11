# SIAS 快速参考卡片

## 🚀 核心原则

### WAL 协议 (Write-Ahead-Log)
```
VOR jeder Antwort:
1. Prüfen: Präferenz? Fehler? Learning?
2. Speichern: In passende .learnings/ Datei
3. Antworten: Erst dann antworten
```

## 📝 日志格式

```markdown
## [TYPE-YYYYMMDD-NNN] Titel
- **Area**: [coding|system|user-pref|workflow|security]
- **Priority**: [critical|high|medium|low]
- **Status**: [active|resolved|archived]
- **Trigger**: [Auslöser]
- **Content**: [Inhalt]
- **Action**: [Maßnahme]
```

## 📁 文件结构

```
~/.openclaw/workspace/
├── SOUL.md              # Agent Identität
├── MEMORY.md            # Permanentes Wissen
├── SESSION-STATE.md     # Aktueller Kontext
├── .learnings/
│   ├── ERRORS.md        # Fehler
│   ├── LEARNINGS.md     # Best Practices
│   ├── CORRECTIONS.md   # User-Korrekturen
│   └── FEATURE_REQUESTS.md # Todos
└── memory/
    └── YYYY-MM-DD.md    # Tageslogs
```

## 🔤 TYPE Codes

| Code | Bedeutung | Beispiel |
|------|-----------|----------|
| ERR | Fehler | Falsches Kommando |
| LRN | Best Practice | Neue Technik |
| COR | Korrektur | "Nein, mach es so..." |
| FEAT | Feature | Todo/Wunsch |

## ⬆️ Promotion Regeln

**Upgrade zu MEMORY.md wenn:**
- Priority = **critical**
- Gleiche Lesson > **3x** wiederholt
- User sagt: "**Das ist wichtig, merk dir das**"

**Prozess:**
1. Kopiere nach MEMORY.md
2. Markiere als `Status: archived`
3. Lösche nie aus .learnings/

## 🔄 日常维护

```bash
# Manuell ausführen
~/.openclaw/workspace/scripts/sias-maintain.sh

# Automatisch (täglich 2 Uhr)
# Cronjob bereits eingerichtet
```

## 📊 快速检查

```bash
# Statistik anzeigen
grep -c "^## \[" ~/.openclaw/workspace/.learnings/*.md

# Heutige Logs anzeigen
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

# MEMORY.md anzeigen
cat ~/.openclaw/workspace/MEMORY.md
```

## 💡 Pro-Tipps

1. **Immer speichern vor Antwort** - Keine Ausnahmen!
2. **Konkrete Actions** - Nicht "besser machen", sondern "immer X verwenden"
3. **Regelmäßige Reflexion** - Alle 10-15 Interaktionen
4. **Backup nutzen** - Automatisch in .learnings-backup/

---
*SIAS v1.0 - Self-Improving Agent System*

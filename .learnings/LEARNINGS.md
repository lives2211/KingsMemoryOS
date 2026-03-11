# LEARNINGS.md - Best Practices

## [LRN-20260310-001] SIAS 框架 erfolgreich deployt
- **Area**: workflow
- **Priority**: high
- **Status**: active
- **Trigger**: User: "安装部署这个项目"
- **Content**: SIAS (Self-Improving Agent System) erfolgreich geklont und deployt
- **Action**: 1) Git clone 2) Templates kopieren 3) .learnings/ Ordner erstellen 4) Verify deployment

## [LRN-20260310-002] WAL-Protokoll korrekt implementiert
- **Area**: workflow
- **Priority**: critical
- **Status**: archived
- **Trigger**: Training Session 1 & 2
- **Content**: Vor jeder Antwort prüfen ob etwas zu speichern ist, dann ZUERST speichern, DANN antworten
- **Action**: Immer Reihenfolge einhalten: 1. Speichern 2. Antworten

## [LRN-20260310-003] Memory-LanceDB-Pro Integration
- **Area**: system
- **Priority**: high
- **Status**: active
- **Trigger**: Optimierung des Memory-Plugins
- **Content**: Hybrid Retrieval (Vector + BM25) mit Cross-Encoder Rerank erfolgreich konfiguriert
- **Action**: Jina API Key in systemd Environment setzen, Config validieren

## [LRN-20260310-004] Automatische Wartung mit Cron
- **Area**: system
- **Priority**: medium
- **Status**: active
- **Trigger**: SIAS Wartung automatisieren
- **Content**: sias-maintain.sh Script erstellt und täglich um 2 Uhr per Cron ausgeführt
- **Action**: Script in ~/.openclaw/workspace/scripts/ speichern, Cronjob erstellen

## [LRN-20260310-005] SIAS CLI Test
- **Area**: system
- **Priority**: high
- **Status**: active
- **Trigger**: CLI add command
- **Content**: Successfully tested SIAS CLI tool
- **Action**: Review and apply

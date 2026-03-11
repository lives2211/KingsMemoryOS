# FEATURE_REQUESTS.md - Feature-Todos

## [FEAT-20260310-001] SIAS Dashboard erstellen
- **Area**: workflow
- **Priority**: medium
- **Status**: active
- **Trigger**: Training abgeschlossen, Übersicht fehlt
- **Content**: Web-Dashboard um SIAS Statistiken zu visualisieren
- **Action**: 1) React/Vue Dashboard erstellen 2) API für SIAS Daten 3) Charts für Learning-Trends

## [FEAT-20260310-002] Automatische Promotion
- **Area**: workflow
- **Priority**: high
- **Status**: active
- **Trigger**: Manuelle Promotion mühsam
- **Content**: Script das automatisch prüft welche Learnings promoted werden sollen
- **Action**: sias-auto-promote.sh erstellen, prüft auf critical oder 3x Wiederholung

## [FEAT-20260310-003] Cross-Agent Memory Sync
- **Area**: system
- **Priority**: medium
- **Status**: active
- **Trigger**: Mehrere Agents mit SIAS
- **Content**: Wichtige Learnings zwischen Agents teilen
- **Action**: Shared Memory Scope nutzen, regelmäßige Sync

## [FEAT-20260310-004] SIAS CLI Tool
- **Area**: workflow
- **Priority**: low
- **Status**: active
- **Trigger**: Manuelles Editieren mühsam
- **Content**: CLI Tool zum schnellen Hinzufügen von Learnings
- **Action**: openclaw sias add --type LRN --content "..."

# ERRORS.md - Fehler-Log

## [ERR-20260310-001] Versucht nicht existierenden Service zu starten
- **Area**: system
- **Priority**: medium
- **Status**: active
- **Trigger**: User sagte "运行不存在的服务"
- **Content**: Versucht `systemctl start non-existent-service` auszuführen, Service existiert nicht
- **Action**: Immer vorher prüfen ob Service existiert mit `systemctl status <service>`

## [ERR-20260310-002] Training Session 2 - Fehlerbehandlung
- **Area**: workflow
- **Priority**: high
- **Status**: active
- **Trigger**: User: "下一步" nach Session 1
- **Content**: Sollte Fehler simulieren und korrekt loggen
- **Action**: 1) Fehler simulieren 2) In ERRORS.md loggen 3) Analyse und Lösung dokumentieren

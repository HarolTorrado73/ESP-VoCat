# Documentación técnica en español

Índice de la documentación del proyecto ESP-VoCat Base.

[← Guía central del proyecto](../README_ES.md)

| Documento | Descripción |
|-----------|-------------|
| [arquitectura.md](arquitectura.md) | Diagramas Mermaid: sistema, capas, UART, calibración, estados |
| [hardware.md](hardware.md) | **Hardware completo:** Main/Sub Board, análisis esquemático, GPIO, motor, sensores |
| [BOM.md](BOM.md) | **Lista de materiales** — designadores, valores, MPN, alternativas |
| [lista-compra.md](lista-compra.md) | **Lista de compra** por categorías + Espressif vs equivalentes |
| [guia-ensamblaje.md](guia-ensamblaje.md) | **Guía de fabricación** — impresión 3D, ensamblaje, calibración |
| [auditoria-hardware.md](auditoria-hardware.md) | **Auditoría hardware** — MPN, contradicciones, checklist, reproducibilidad |
| [auditoria-documentacion.md](auditoria-documentacion.md) | **Auditoría docs** — archivos chinos, plan de limpieza |
| [tablas-referencia.md](tablas-referencia.md) | GPIO, hardware, sensores, UART, eventos, proyectos |
| [arranque-firmware.md](arranque-firmware.md) | Secuencia de boot + diagramas de secuencia |
| [perfiles.md](perfiles.md) | Arquitectura `MAG_SW_PROFILE` y diferencias entre demos |
| [extender-proyecto.md](extender-proyecto.md) | Nuevo perfil, sensor, acción; buenas prácticas |
| [troubleshooting.md](troubleshooting.md) | Resolución de problemas frecuentes |

## Firmware por proyecto

- [esp_vocat_rotating_base](../software/esp_vocat_rotating_base/README_ES.md) — perfil `base`
- [bell_event_detection](../software/esp_vocat_rotating_base_bell_event_detection/README_ES.md) — perfil `bell`
- [iphone_detection](../software/esp_vocat_rotating_base_iphone_detection/README_ES.md) — perfil `iphone`
- [magnetic_accessory_detection](../software/esp_vocat_rotating_base_magnetic_accessory_detection/README_ES.md) — perfil `magnetic_accessory`

# ESP-VoCat Base: Firmware estándar

**[Español](README_ES.md)** | [English](README.md)

> **Perfil:** `base` · **Versión:** V1.0.4  
> **Documentación completa:** [Guía central del proyecto](../../README_ES.md)

---

## Descripción

Firmware principal de la base rotatoria ESP-VoCat. Implementa control del motor paso a paso, detección magnética con perfil `base`, comunicación UART y calibración automática.

**Diferencia clave respecto a los demos:** en este proyecto los eventos magnéticos se envían por UART **directamente** desde `magnetic_slide_switch.c` (sin callback en `app_main`).

---

## Eventos soportados (perfil `base`)

| Código | Evento |
|--------|--------|
| 1–7 | Deslizamiento, colocación, retirada, clic simple |
| 8–9 | Pez adherido / retirado |
| 10–11 | Emparejamiento / cancelado |

Tabla completa: [Tablas de referencia → Eventos](../../docs/es/tablas-referencia.md#perfil-base-esp_vocat_rotating_base)

---

## Compilar

```bash
cd software/esp_vocat_rotating_base
idf.py set-target esp32c61
idf.py menuconfig    # Magnetic Slide Switch → Sensor Type
idf.py build flash monitor
```

---

## Documentación relacionada

| Tema | Enlace |
|------|--------|
| GPIO, UART, acciones | [Tablas de referencia](../../docs/es/tablas-referencia.md) |
| Arranque y secuencias | [Arranque del firmware](../../docs/es/arranque-firmware.md) |
| Arquitectura | [Arquitectura del sistema](../../docs/es/arquitectura.md) |
| Comandos UART detallados | [Tablas → UART](../../docs/es/tablas-referencia.md#comandos-uart) |
| Calibración magnética | [Arquitectura → Calibración](../../docs/es/arquitectura.md#5-flujo-de-calibración-automática-magnética) |
| Problemas frecuentes | [Troubleshooting](../../docs/es/troubleshooting.md) |

---

## Tareas FreeRTOS de esta aplicación

```
app_main
├── base_calibration_task          # Homing mecánico (GPIO 1 → +95°)
├── uart_cmd_receive_task          # Comandos UART (prioridad 12)
├── magnetic_detect_task           # Acoplamiento magnético cada 500 ms
├── mag_data_read_task             # Lectura sensor I2C
├── mag_calibration_task           # Calibración automática 3 posiciones
└── slide_switch_event_detect_task # Detección de eventos → UART directo
```

---

## Licencia

GPL-3.0 — Firmware de referencia para el kit ESP-VoCat de Espressif.

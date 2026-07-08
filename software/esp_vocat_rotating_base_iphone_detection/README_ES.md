# ESP-VoCat Base: Detección de iPhone

**[Español](README_ES.md)** | [English](README.md)

> **Perfil:** `iphone` · **Versión:** V1.0.4  
> **Documentación completa:** [Guía central del proyecto](../../README_ES.md)

---

## Descripción

Demostración de **detección de proximidad de iPhone** mediante variaciones del eje Z del magnetómetro respecto a la línea base calibrada. Usa el perfil `magnetic_slide_switch/profiles/iphone`.

Los eventos se reportan vía callback registrado en `app_main` → `control_serial_send_magnetic_switch_event()`.

---

## Eventos soportados (perfil `iphone`)

| Código | Evento | Criterio (BMM150) |
|--------|--------|-------------------|
| 16 | `IPHONE_LEAN_FRONT` | ΔZ ≥ 450 respecto a baseline |
| 17 | `IPHONE_LEAN_FRONT_DETACHED` | iPhone se separa del frente |
| 18 | `IPHONE_UNDER_BASE` | Caída de Z ≥ 600 (bajo la base) |
| 19 | `IPHONE_UNDER_BASE_DETACHED` | iPhone retirado de debajo |

Umbrales definidos en `profiles/iphone/include/magnetic_slide_switch.h` (`MAGNETIC_ACCESSORY_DETECTION_Z_INCREASE`, `MAGNETIC_ACCESSORY_DETECTION_Z_DROP_UNDER_BASE`).

Detalle: [Sensado magnético → iPhone](../../magnetic_sensing_interaction_solution_es.md#22-demostración-de-detección-de-iphone)

---

## Compilar

```bash
cd software/esp_vocat_rotating_base_iphone_detection
idf.py set-target esp32c61
idf.py build flash monitor
```

`CMakeLists.txt` define `set(MAG_SW_PROFILE "iphone")`.

---

## Diferencias respecto al firmware base

| Aspecto | `base` | `iphone` (este proyecto) |
|---------|--------|--------------------------|
| Eventos de deslizador | Sí (1–7) | No |
| Eventos iPhone | No | Sí (16–19) |
| Lógica de detección | Eje Z + estados UP/DOWN | Variación ΔZ vs baseline |

---

## Documentación relacionada

| Tema | Enlace |
|------|--------|
| Perfiles | [docs/es/perfiles.md](../../docs/es/perfiles.md) |
| Calibración | [docs/es/arranque-firmware.md](../../docs/es/arranque-firmware.md) |
| Troubleshooting | [docs/es/troubleshooting.md](../../docs/es/troubleshooting.md) |

---

## Licencia

GPL-3.0

# ESP-VoCat Base: Detección de accesorios magnéticos

**[Español](README_ES.md)** | [English](README.md)

> **Perfil:** `magnetic_accessory` · **Versión:** V1.0.4  
> **Documentación completa:** [Guía central del proyecto](../../README_ES.md)

---

## Descripción

Demostración de **accesorios magnéticos** (pez, helado, dona) y modo emparejamiento. Usa el perfil `magnetic_slide_switch/profiles/magnetic_accessory` con detección basada en incrementos del eje Z respecto a la posición `REMOVED` calibrada.

Incluye **baseline dinámico** (EMA) y **confirmación retardada** (`ACCESSORY_CONFIRM_MS = 200 ms`) para distinguir accesorios.

---

## Eventos soportados (perfil `magnetic_accessory`)

| Código | Evento |
|--------|--------|
| 8 | `FISH_ATTACHED` |
| 9 | `FISH_DETACHED` |
| 10 | `PAIRING` |
| 11 | `PAIRING_CANCELLED` |
| 12 | `ICE_CREAM_ATTACHED` |
| 13 | `ICE_CREAM_DETACHED` |
| 14 | `DONUT_ATTACHED` |
| 15 | `DONUT_DETACHED` |

### Rangos ΔZ (BMM150, desde `magnetic_slide_switch.h`)

| Accesorio | ΔZ mínimo | ΔZ máximo |
|-----------|-----------|-----------|
| Pez | 50 | 130 |
| Helado | 140 | 200 |
| Dona | 270 | 310 |

Detalle: [Sensado magnético → Accesorios](../../magnetic_sensing_interaction_solution_es.md#23-demostración-de-detección-de-accesorios-magnéticos)

---

## Compilar

```bash
cd software/esp_vocat_rotating_base_magnetic_accessory_detection
idf.py set-target esp32c61
idf.py build flash monitor
```

`CMakeLists.txt` define `set(MAG_SW_PROFILE "magnetic_accessory")`.

---

## Diferencias respecto al firmware base

| Aspecto | `base` | `magnetic_accessory` |
|---------|--------|----------------------|
| Detección pez | Por deslizador (campo total) | Por ΔZ en posición REMOVED |
| Helado / dona | No | Sí |
| Baseline dinámico | No | Sí (`DYNAMIC_BASELINE_EMA_SHIFT`) |
| Confirmación retardada | No | Sí (200 ms) |

---

## Documentación relacionada

| Tema | Enlace |
|------|--------|
| Perfiles y extensión | [docs/es/perfiles.md](../../docs/es/perfiles.md) |
| Tablas de eventos | [docs/es/tablas-referencia.md](../../docs/es/tablas-referencia.md) |
| Troubleshooting calibración | [docs/es/troubleshooting.md#2-el-sensor-no-calibra](../../docs/es/troubleshooting.md#2-el-sensor-no-calibra) |

---

## Licencia

GPL-3.0

# ESP-VoCat Base: Detección de eventos de campana

**[Español](README_ES.md)** | [English](README.md)

> **Perfil:** `bell` · **Versión:** V1.0.4  
> **Documentación completa:** [Guía central del proyecto](../../README_ES.md)

---

## Descripción

Demostración centrada en el **deslizador tipo campana**. Utiliza el perfil `magnetic_slide_switch/profiles/bell` y registra un callback en `app_main` que reenvía los eventos detectados a ESP-VoCat por UART.

```c
// esp_vocat_rotating_base_main.c
magnetic_slide_switch_register_callback(magnetic_slide_switch_event_cb);
```

---

## Eventos soportados (perfil `bell`)

| Código | Evento |
|--------|--------|
| 1 | `SLIDE_DOWN` |
| 2 | `SLIDE_UP` |
| 3 | `REMOVE_FROM_UP` |
| 4 | `REMOVE_FROM_DOWN` |
| 5 | `PLACE_FROM_UP` |
| 6 | `PLACE_FROM_DOWN` |
| 7 | `SINGLE_CLICK` |

No incluye eventos de pez, emparejamiento, iPhone ni accesorios.

Detalle: [Sensado magnético → Campana](../../magnetic_sensing_interaction_solution_es.md#21-demostración-de-eventos-del-deslizador-tipo-campana)

---

## Compilar

```bash
cd software/esp_vocat_rotating_base_bell_event_detection
idf.py set-target esp32c61
idf.py build flash monitor
```

`CMakeLists.txt` define `set(MAG_SW_PROFILE "bell")`.

---

## Diferencias respecto al firmware base

| Aspecto | `base` | `bell` (este proyecto) |
|---------|--------|------------------------|
| Perfil CMake | `base` | `bell` |
| Eventos | 1–11 | 1–7 |
| Reporte UART | Directo en componente | Callback en `app_main` |
| Pez / emparejamiento | Sí | No |

Comparativa completa: [Perfiles](../../docs/es/perfiles.md#diferencias-entre-perfiles)

---

## Documentación relacionada

| Tema | Enlace |
|------|--------|
| Arquitectura de perfiles | [docs/es/perfiles.md](../../docs/es/perfiles.md) |
| Tablas GPIO / UART | [docs/es/tablas-referencia.md](../../docs/es/tablas-referencia.md) |
| Troubleshooting | [docs/es/troubleshooting.md](../../docs/es/troubleshooting.md) |

---

## Licencia

GPL-3.0

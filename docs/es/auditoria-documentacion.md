# Auditoría de documentación — archivos en chino

> **Fecha:** 2026-07-08  
> **Alcance:** todos los Markdown en chino del repositorio, comparados con `README_ES.md`, `docs/es/` y documentación en inglés.  
> **Acción:** limpieza completada el 2026-07-08 — **7 archivos en chino eliminados**.

[← Índice documentación](README.md) · [Auditoría hardware](auditoria-hardware.md)

---

## 1. Inventario de archivos en chino

| # | Archivo | Líneas (aprox.) | Tipo |
|---|---------|-----------------|------|
| 1 | `README_CN.md` | 129 | README raíz |
| 2 | `magnetic_sensing_interaction_solution_zh.md` | 44 | Guía magnética |
| 3 | `software/esp_vocat_rotating_base/README_CN.md` | 349 | README firmware |
| 4 | `software/esp_vocat_rotating_base_bell_event_detection/README_CN.md` | 350 | README firmware |
| 5 | `software/esp_vocat_rotating_base_iphone_detection/README_CN.md` | 349 | README firmware |
| 6 | `software/esp_vocat_rotating_base_magnetic_accessory_detection/README_CN.md` | 350 | README firmware |
| 7 | `software/common_components/BMM150_SensorAPI/README_CN.md` | 175 | README componente tercero |

**Total:** 7 archivos Markdown en chino.

**Nota:** `docs/7726, 2155.txt` contiene texto en chino (exportación OSHWHUB) pero no es README; se conserva como fuente de hardware, fuera del alcance de esta limpieza.

---

## 2. Tabla de auditoría por archivo

| Archivo | ¿Migrado al español? | ¿Info exclusiva? | Enlaces activos | ¿Conservar? | Acción recomendada |
|---------|---------------------|------------------|-----------------|-------------|-------------------|
| `README_CN.md` | **Sí** — contenido equivalente en `README_ES.md` (más completo) y `README.md` | No — duplicado de `README.md` en chino; enlaces Bilibili/Gitee/OSHWHUB ya en `README_ES.md` | Sí (internos y externos) | **No** (si se mantiene inglés) | **Eliminar** tras actualizar `README.md` |
| `magnetic_sensing_interaction_solution_zh.md` | **Sí** — equivalente a `magnetic_sensing_interaction_solution_es.md` | No | Sí | **No** | **Eliminar** |
| `software/.../README_CN.md` (×4) | **Parcial** — lo esencial está en `docs/es/`; detalle extenso duplicado en `README.md` (EN) | No respecto al CN; sí hay detalle no traducido al ES pero **presente en inglés** (API motor, rangos magnéticos BMM150, historial versiones) | Sí | **No** (si se mantiene `README.md` EN) | **Eliminar** los 4 archivos |
| `BMM150_SensorAPI/README_CN.md` | **No** al español — traducción del `README.md` EN del componente | No — duplicado del README inglés del driver Bosch/Espressif | Sí | **No** (si se mantiene EN) | **Eliminar** |

---

## 3. Comparativa de cobertura

### 3.1 README raíz

| Contenido | README_CN | README.md (EN) | README_ES |
|-----------|-----------|----------------|-----------|
| Descripción del proyecto | ✓ | ✓ | ✓ |
| Estructura del repo | ✓ | ✓ | ✓ (actualizada) |
| Demos / perfiles | ✓ | ✓ | ✓ + enlaces `docs/es/` |
| UART / comandos | Enlace a README_CN firmware | Enlace a README EN firmware | `docs/es/tablas-referencia.md` |
| Hardware / fabricación | Enlace OSHWHUB | Enlace OSHWHUB | `docs/es/BOM.md`, `guia-ensamblaje.md`, etc. |
| CSI, Bilibili, Gitee | ✓ | ✓ | ✓ |

**Conclusión:** `README_ES.md` es **superset** de `README_CN.md` para uso en español.

### 3.2 README firmware (`software/*/README_CN` vs `README_ES`)

| Contenido | README_CN (~350 líneas) | README_ES (~50 líneas) | `docs/es/` |
|-----------|-------------------------|------------------------|------------|
| Compilar / flashear | ✓ | ✓ | `arranque-firmware.md` |
| GPIO / UART | ✓ | Enlaces | `tablas-referencia.md` |
| Ejemplos hex UART | ✓ extenso | Enlace | `tablas-referencia.md` (principal) |
| Arquitectura tareas | ✓ | Enlace | `arquitectura.md`, `arranque-firmware.md` |
| Calibración magnética | ✓ detallado | Enlace | `arquitectura.md` |
| API `stepper_*` con firmas | ✓ | — | Mención en `arquitectura.md`, no firmas completas |
| Rangos magnéticos BMM150 (709/1383/2047) | ✓ | — | **No migrado** |
| Parámetros rendimiento | ✓ | — | `tablas-referencia.md` § rendimiento |
| FAQ extendido | ✓ | — | `troubleshooting.md` (cobertura similar) |
| Historial de versiones | ✓ | — | **No migrado** |

**Conclusión:** los README_CN de firmware son **traducción paralela** de `README.md` (inglés), no de `README_ES.md`. Para español, la documentación operativa está en `docs/es/`. Quedan **brechas menores** (firmas API motor, rangos de campo magnético, changelog firmware) disponibles en inglés en `software/*/README.md`.

### 3.3 Sensado magnético

| Archivo | Líneas | Equivalente ES |
|---------|--------|----------------|
| `magnetic_sensing_interaction_solution_zh.md` | 44 | `magnetic_sensing_interaction_solution_es.md` (45) + `docs/es/perfiles.md` |

**Contenido:** migrado al 100 %.

### 3.4 BMM150_SensorAPI

| Archivo | Notas |
|---------|-------|
| `README_CN.md` | Traducción de `README.md` (adaptador AUX BMI270); **no usado directamente** por la base ESP-VoCat (BMM150 vía I2C directo) |
| `README.md` (EN) | Conservar como referencia del componente |

---

## 4. ¿Es autosuficiente la documentación en español?

| Área | Autosuficiente | Notas |
|------|----------------|-------|
| Guía del proyecto | **Sí** | `README_ES.md` |
| Arquitectura / UART / GPIO | **Sí** | `docs/es/` |
| Fabricación hardware | **Sí** | BOM, lista compra, ensamblaje, auditoría HW |
| Firmware — uso diario | **Sí** | Compilar, perfiles, troubleshooting |
| Firmware — referencia API motor | **Parcial** | Firmas en `README.md` EN; opcional migrar a `docs/es/extender-proyecto.md` |
| Rangos calibración BMM150 (709…) | **Parcial** | Solo en README EN/CN; no crítico para operación |
| Driver BMM150 AUX | **N/A** | Componente auxiliar; EN suficiente |

**Veredicto:** la documentación en español es **autosuficiente para usar, fabricar y depurar** el proyecto. Eliminar archivos chinos **no rompe** ese flujo si se conserva `README.md` en inglés para detalle firmware residual.

---

## 5. Referencias internas a archivos chinos

### 5.1 Archivos que enlazan a documentación china (pre-limpieza)

| Archivo | Enlace a eliminar | Estado |
|---------|-------------------|--------|
| `README_ES.md` | `README_CN.md` | **Corregido** — barra ES \| EN |
| `software/*/README_ES.md` (×4) | `README_CN.md` | **Corregido** |
| `magnetic_sensing_interaction_solution_es.md` | `_zh.md` | **Corregido** |
| `README.md` | `README_CN.md` | **Corregido** — barra ES \| EN |
| `README_CN.md` | `software/.../README_CN.md` | Desaparece con el archivo |
| `software/*/README.md` (×4) | `README_CN.md` | **Corregido** |
| `magnetic_sensing_interaction_solution_en.md` | `_zh.md` | **Corregido** |
| `magnetic_sensing_interaction_solution_zh.md` | `_zh.md` | Desaparece con el archivo |
| `CHANGELOG.md` | Mención histórica `README_CN.md` | Conservar (texto, no enlace roto) |
| `BMM150_SensorAPI/CHECKSUMS.json` | Hash de `README_CN.md` | **Eliminado** (2026-07-08) |

### 5.2 `docs/es/` — enlaces a chino

**Ninguno.** La documentación española no referencia archivos chinos.

---

## 6. Plan de limpieza (orden recomendado)

### Fase A — Preparación (completada en parte)

- [x] Quitar enlaces chinos de todos los `README_ES.md`
- [x] Quitar enlace zh de `magnetic_sensing_interaction_solution_es.md`
- [ ] (Opcional) Migrar rangos magnéticos BMM150 a `docs/es/troubleshooting.md` o `tablas-referencia.md`

### Fase B — Actualizar enlaces EN (antes de borrar)

- [x] `README.md`: quitar `[简体中文](README_CN.md)` de la barra de idiomas
- [x] `software/*/README.md` (×4): quitar enlace `[中文](README_CN.md)`
- [x] `magnetic_sensing_interaction_solution_en.md`: quitar enlace `_zh.md`

### Fase C — Eliminar archivos (7)

- [x] Eliminados los 7 archivos Markdown en chino (2026-07-08)
- [x] Actualizado `BMM150_SensorAPI/CHECKSUMS.json`

### Fase D — Post-eliminación

- [x] Regenerar o editar `BMM150_SensorAPI/CHECKSUMS.json` (eliminar entrada `README_CN.md`)
- [x] Verificar con búsqueda: `README_CN`, `_zh.md`, `简体中文` — sin enlaces rotos en docs activos

---

## 7. Lista exacta de archivos eliminables

Estos **7 archivos** pueden eliminarse **sin pérdida de información funcional** ni rotura de enlaces desde documentación en español, **después** de completar la Fase B:

```
README_CN.md
magnetic_sensing_interaction_solution_zh.md
software/esp_vocat_rotating_base/README_CN.md
software/esp_vocat_rotating_base_bell_event_detection/README_CN.md
software/esp_vocat_rotating_base_iphone_detection/README_CN.md
software/esp_vocat_rotating_base_magnetic_accessory_detection/README_CN.md
software/common_components/BMM150_SensorAPI/README_CN.md
```

### Condiciones

1. Conservar `README.md` (inglés) en raíz y en cada proyecto firmware.
2. Completar actualización de enlaces en archivos EN (Fase B).
3. No eliminar `docs/7726, 2155.txt` (fuente hardware, no README).

### Archivos que **no** deben eliminarse

| Archivo | Motivo |
|---------|--------|
| `README.md` | Idioma principal del upstream / detalle firmware |
| `magnetic_sensing_interaction_solution_en.md` | Equivalente EN vigente |
| `magnetic_sensing_interaction_solution_es.md` | Documentación ES vigente |
| `docs/es/**` | Documentación principal en español |
| `docs/7726, 2155.txt` | Fuente OSHWHUB (hardware) |

---

## 8. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Archivos Markdown en chino | 7 |
| Migrados completamente al español | 2 (`README_CN` raíz, `magnetic_sensing_interaction_solution_zh`) |
| Duplicados del inglés (no migrados al ES, pero redundantes) | 5 (4 firmware + BMM150) |
| Eliminables con plan completo | **7** |
| Enlaces rotos en docs ES tras limpieza | **0** (ya corregidos) |
| Autosuficiencia documentación ES | **~95 %** (brechas menores en API motor / rangos magnéticos) |

---

*No se ha eliminado ningún archivo. Este documento es el plan de limpieza aprobado para una PR posterior.*

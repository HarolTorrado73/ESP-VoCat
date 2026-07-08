# Cómo extender el proyecto

> Basado en la estructura real de `common_components/` y el mecanismo `MAG_SW_PROFILE`.

[← Volver a la guía principal](../../README_ES.md) · [Perfiles](perfiles.md)

---

## 1. Crear un nuevo perfil magnético

### Paso 1 — Copiar un perfil existente

```bash
cd software/common_components/magnetic_slide_switch/profiles
cp -r bell mi_perfil
```

### Paso 2 — Definir eventos en el header

Editar `profiles/mi_perfil/include/magnetic_slide_switch.h`:

- Definir `typedef enum { ... } magnetic_slide_switch_event_t` con los eventos deseados.
- Configurar umbrales bajo `#ifdef CONFIG_SENSOR_BMM150` / `CONFIG_SENSOR_QMC6309`.
- Mantener las funciones públicas: `magnetic_slide_switch_start()`, `magnetic_slide_switch_get_event()`, `magnetic_slide_switch_start_recalibration()`.
- Si necesita reporte UART vía aplicación, incluir `magnetic_slide_switch_register_callback()`.

### Paso 3 — Implementar lógica de detección

Editar `profiles/mi_perfil/magnetic_slide_switch.c`:

- Reutilizar tareas existentes como referencia: `magnetometer_data_read_task`, `magnetometer_calibration_task`, `slide_switch_event_detect_task`.
- La calibración automática (máquina de estados `CALIBRATION_*`) puede reutilizarse del perfil `base` o `bell`.
- Invocar callbacks o `control_serial_send_magnetic_switch_event()` al confirmar eventos.

### Paso 4 — Registrar el perfil en CMake

En `software/common_components/magnetic_slide_switch/CMakeLists.txt`:

```cmake
elseif(MAG_SW_PROFILE STREQUAL "mi_perfil")
    set(MAG_SW_PROFILE_DIR "profiles/mi_perfil")
```

### Paso 5 — Crear proyecto de aplicación

```bash
cp -r software/esp_vocat_rotating_base_bell_event_detection \
      software/esp_vocat_rotating_base_mi_perfil
```

En el `CMakeLists.txt` del nuevo proyecto:

```cmake
set(MAG_SW_PROFILE "mi_perfil")
project(esp_vocat_rotating_base_mi_perfil)
```

En `main/esp_vocat_rotating_base_main.c`:

- Registrar callback si el perfil lo requiere.
- Mantener la lógica de homing y botones sin cambios.

### Paso 6 — Compilar y verificar

```bash
cd software/esp_vocat_rotating_base_mi_perfil
idf.py set-target esp32c61
idf.py menuconfig   # Seleccionar sensor
idf.py build flash monitor
```

---

## 2. Agregar un nuevo sensor magnético

### Opción A — Nuevo magnetómetro I2C

1. Añadir opción en `magnetic_slide_switch/Kconfig`:

```kconfig
config SENSOR_MI_SENSOR
    bool "MI Sensor Magnetometer"
    depends on SENSOR_MAGNETOMETER
```

2. En el header del perfil activo, añadir bloque `#elif defined(CONFIG_SENSOR_MI_SENSOR)` con:
   - `MAGNETOMETER_I2C_ADDR`
   - `MAGNETOMETER_CHIP_ID`
   - Umbrales `MAG_STATE_*_CENTER` / `OFFSET`
   - `MAG_SAMPLE_PERIOD_MS`, `MAG_WINDOW_SIZE`

3. En `magnetic_slide_switch.c`, implementar inicialización y lectura I2C (seguir patrón BMM150/QMC6309 en `magnetometer_data_read_task`).

4. Si el sensor requiere driver dedicado, añadir componente en `common_components/` (como `BMM150_SensorAPI`) y declararlo en `idf_component.yml`.

### Opción B — Sensor sin soporte en perfil actual

El sensor Hall lineal (`CONFIG_SENSOR_LINEAR_HALL`) solo implementa `SLIDE_UP`/`SLIDE_DOWN` en el código actual. Para más eventos con Hall, extender `hall_sensor_read_task` en el perfil correspondiente.

---

## 3. Agregar nuevas acciones del motor

### Paso 1 — Extender el enum

En `stepper_motor/include/stepper_motor.h`:

```c
typedef enum {
    STEPPER_ACTION_SHAKE_HEAD,
    // ... existentes ...
    STEPPER_ACTION_MI_ACCION,    // Nuevo
    STEPPER_ACTION_MAX
} stepper_action_type_t;
```

### Paso 2 — Implementar la función

En `stepper_motor/stepper_motor.c`:

```c
void stepper_mi_accion(float parametro, int speed_us) {
    // Usar stepper_rotate_angle_with_accel() o secuencias half-step
}
```

### Paso 3 — Despachar desde UART

En `control_serial.c`, dentro del `switch (action)` de `CMD_BASE_ACTION_CONTROL`:

```c
case STEPPER_ACTION_MI_ACCION:
    stepper_mi_accion(15.0, STEPPER_SPEED_NORMAL);
    stepper_motor_power_off();
    control_serial_send_action_complete();
    break;
```

### Paso 4 — Documentar el código UART

Actualizar [tablas-referencia.md](tablas-referencia.md) con el nuevo valor de acción (será el índice del enum, p. ej. `0x0005` si es el sexto elemento).

> **Compatibilidad:** No reutilizar valores numéricos de acciones existentes. El host ESP-VoCat debe actualizarse en paralelo.

---

## 4. Buenas prácticas de compatibilidad

### Protocolo UART

| Regla | Motivo |
|-------|--------|
| No cambiar cabecera `0xAA 0x55` | Sincronización de tramas en `uart_cmd_receive_task` |
| No cambiar cálculo de checksum | Validación antes de ejecutar comandos |
| Añadir comandos nuevos con CMD nuevo | CMD `0x02` se usa tanto para acciones como para `ACTION_COMPLETE` en dirección Base→Host |
| Documentar nuevos códigos de evento | El host interpreta el campo DATA de CMD `0x03` |

### Perfiles

| Regla | Motivo |
|-------|--------|
| Un perfil por build | `CMakeLists.txt` solo compila un `magnetic_slide_switch.c` |
| No mezclar enums entre perfiles | Cada perfil tiene su propio `magnetic_slide_switch_event_t` |
| Mantener API pública consistente | `start()`, `get_event()`, `start_recalibration()` en todos los perfiles |

### Calibración NVS

| Regla | Motivo |
|-------|--------|
| No cambiar claves NVS sin migración | Datos de calibración persisten entre actualizaciones |
| Mantener 3 posiciones (REMOVED/UP/DOWN) | Máquina de estados compartida entre perfiles con deslizador |
| Umbral `CALIBRATION_VALUE_DIFF_THRESHOLD = 100` | Coherencia con firmware existente |

### Motor

| Regla | Motivo |
|-------|--------|
| Llamar `stepper_motor_power_off()` tras cada movimiento | Evita calentamiento y consumo |
| Respetar rango 0–180° en control de ángulo | Validado en `uart_cmd_receive_task` |
| No modificar GPIO 25–28 sin actualizar `stepper_motor.h` | Asignación de hardware fija en PCB |

### Compilación

| Regla | Motivo |
|-------|--------|
| Usar ESP-IDF ≥ 5.5 | Declarado en `idf_component.yml` |
| `idf.py set-target esp32c61` | MCU de la base es ESP32-C61 |
| `EXTRA_COMPONENT_DIRS` apunta a `../common_components` | Requerido en CMakeLists de cada app |

---

## 5. Estructura recomendada para un nuevo proyecto demo

```
software/esp_vocat_rotating_base_mi_demo/
├── CMakeLists.txt              # MAG_SW_PROFILE="mi_perfil"
├── sdkconfig.defaults
└── main/
    ├── CMakeLists.txt
    ├── idf_component.yml
    └── esp_vocat_rotating_base_main.c   # callback + homing
```

Documentar el nuevo proyecto en:
- `README_ES.md` (raíz) — tabla de proyectos
- `docs/es/tablas-referencia.md` — eventos y comparativa
- `docs/es/perfiles.md` — descripción del perfil
- `software/esp_vocat_rotating_base_mi_demo/README_ES.md` — guía rápida del demo

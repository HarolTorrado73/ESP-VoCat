# Tablas de referencia técnica

> Fuente: `control_serial.h`, `stepper_motor.h`, `magnetic_slide_switch.h` (por perfil), `esp_vocat_rotating_base_main.c`, documentación oficial del repositorio.

[← Volver a la guía principal](../../README_ES.md)

---

## Asignación de GPIO

| GPIO | Función | Dirección | Módulo | Nivel activo / Notas |
|------|---------|-----------|--------|----------------------|
| GPIO 1 | Fin de carrera de homing | Entrada | `base_calibration_task` | Activo en bajo (`active_level = 0`) |
| GPIO 2 | I2C SDA | I/O | Magnetómetro BMM150 / QMC6309 | Frecuencia I2C: 400 kHz |
| GPIO 3 | I2C SCL | Salida | Magnetómetro BMM150 / QMC6309 | `I2C_NUM_0` |
| GPIO 5 | ADC Hall lineal | Entrada | `magnetic_slide_switch` | `ADC_CHANNEL_3`, solo si `CONFIG_SENSOR_LINEAR_HALL` |
| GPIO 9 | Botón Boot | Entrada | `app_main` | Activo en bajo; pulsación larga → recalibración magnética |
| GPIO 25 | Motor IN4 | Salida | `stepper_motor` | Secuencia half-step |
| GPIO 26 | Motor IN3 | Salida | `stepper_motor` | Secuencia half-step |
| GPIO 27 | Motor IN2 | Salida | `stepper_motor` | Secuencia half-step |
| GPIO 28 | Motor IN1 | Salida | `stepper_motor` | Secuencia half-step |
| GPIO 8 | UART RX | Entrada | `control_serial` | UART1, 115200 bps |
| GPIO 29 | UART TX | Salida | `control_serial` | UART1, 115200 bps |

---

## Componentes de hardware

| Componente | Modelo / referencia | Función | Interfaz |
|------------|---------------------|---------|----------|
| MCU | ESP32-C61-WROOM-1(N8R2) | Control principal, FreeRTOS | USB Type-C |
| Motor paso a paso | 24BYJ48 | Rotación de la base | 4 líneas → ULN2003 |
| Driver de motor | ULN2003 | Excitación de bobinas | GPIO 25–28 |
| Fin de carrera | Interruptor mecánico | Homing angular | GPIO 1 |
| Botón Boot | Integrado en módulo | Recalibración magnética | GPIO 9 |
| Magnetómetro (defecto) | BMM150 | Detección de campo magnético | I2C `0x10` |
| Magnetómetro (alt.) | QMC6309 | Detección de campo magnético | I2C `0x7C` |
| Sensor Hall (alt.) | Lineal | Solo SLIDE_UP / SLIDE_DOWN | ADC GPIO 5 |
| Host | ESP-VoCat (unidad principal) | Comandos y localización de sonido | UART + acoplamiento magnético |
| PCB | ESP-VoCat-Base Main/Sub Board V1.0 | Distribución de señales | Ver `hardware/` |
| Mecánica | Carcasa, plataforma, bola | Soporte físico | Ver `3D_models/` |

**Enlaces de hardware abierto:**
- [Base magnética (OSHWHUB)](https://oshwhub.com/esp-college/esp-echoear-base)
- [ESP-VoCat (OSHWHUB)](https://oshwhub.com/esp-college/echoear)

---

## Sensores compatibles

| Sensor | Configuración `menuconfig` | Dirección I2C / Pin | Período de muestreo | Eventos soportados |
|--------|---------------------------|---------------------|---------------------|-------------------|
| BMM150 | `SENSOR_MAGNETOMETER` + `SENSOR_BMM150` | I2C `0x10`, GPIO 2/3 | 5 ms (200 Hz) | Todos (según perfil) |
| QMC6309 | `SENSOR_MAGNETOMETER` + `SENSOR_QMC6309` | I2C `0x7C`, GPIO 2/3 | 2 ms (500 Hz) | Todos (según perfil) |
| Hall lineal | `SENSOR_LINEAR_HALL` | ADC GPIO 5, canal 3 | 50 ms | Solo `SLIDE_UP` / `SLIDE_DOWN` |

**Ruta de configuración:** `idf.py menuconfig` → `Component config` → `Magnetic Slide Switch` → `Sensor Type`

---

## Acciones del motor (`stepper_action_type_t`)

Valores recibidos por UART en `CMD_BASE_ACTION_CONTROL` (campo de 16 bits). El firmware interpreta el valor como índice del enum `stepper_action_type_t` definido en `stepper_motor.h`.

| Valor UART | Enum | Función | Parámetros usados en firmware (`control_serial.c`) | Notifica fin |
|------------|------|---------|---------------------------------------------------|--------------|
| `0x0000` | `STEPPER_ACTION_SHAKE_HEAD` | Sacudir cabeza | amplitud 6°, 2 ciclos, 600 µs/paso | Sí |
| `0x0001` | `STEPPER_ACTION_SHAKE_HEAD_DECAY` | Sacudir con decaimiento | amplitud inicial 20°, decay 0.8, 800 µs/paso | Sí |
| `0x0002` | `STEPPER_ACTION_LOOK_AROUND` | Mirar alrededor | 35°/35°, scan 10°, pausa 600 ms | Sí |
| `0x0003` | `STEPPER_ACTION_BEAT_SWING` | Seguir ritmo | ángulo 20°, 800 µs/paso | **No** (comentado en código) |
| `0x0004` | `STEPPER_ACTION_CAT_NUZZLE` | Acariciar | 20°, 3 ciclos, 1500 µs/paso | Sí |

**Velocidades predefinidas** (`stepper_motor.h`):

| Macro | Retardo por paso | Uso típico |
|-------|------------------|------------|
| `STEPPER_SPEED_ULTRA_FAST` | 600 µs | Control de ángulo (localización de sonido) |
| `STEPPER_SPEED_FAST` | 800 µs | Homing |
| `STEPPER_SPEED_NORMAL` | 1500 µs | Movimiento general |
| `STEPPER_SPEED_SLOW` | 2000 µs | Acariciar / gestos suaves |

---

## Comandos UART

### Formato de trama

```
AA 55 [LEN_H] [LEN_L] [CMD] [DATA...] [CHECKSUM]
```

- **Cabecera:** `0xAA 0x55`
- **LEN:** longitud de `CMD` + `DATA` (big-endian, 16 bits)
- **CHECKSUM:** suma aritmética de todos los bytes desde `CMD` hasta el último byte de `DATA`

### Comandos recibidos por la base (ESP-VoCat → Base)

| CMD | Nombre | DATA (16 bits) | Descripción |
|-----|--------|----------------|-------------|
| `0x01` | `CMD_BASE_ANGLE_CONTROL` | Ángulo 0–180 | Ángulo absoluto respecto al frente (90° = centro). La base calcula `diff = ángulo - 90` y rota en consecuencia. |
| `0x02` | `CMD_BASE_ACTION_CONTROL` | Código de acción | Ejecuta acción predefinida del motor (ver tabla anterior). |
| `0x03` | `CMD_MAGNETIC_SWITCH_EVENT` | `0x0010` | Comando de recalibración magnética (`MAG_SWITCH_CMD_RECALIBRATE`). |

**Ejemplo — rotar a 45°:**
```
AA 55 00 03 01 00 2D 2E
```
- Ángulo: `0x002D` = 45 → `diff = -45°` desde centro
- Checksum: `0x01 + 0x00 + 0x2D = 0x2E`

**Ejemplo — recalibración magnética:**
```
AA 55 00 03 03 00 10 13
```
- Checksum: `0x03 + 0x00 + 0x10 = 0x13`

### Comandos enviados por la base (Base → ESP-VoCat)

| CMD | Nombre | DATA (16 bits) | Descripción |
|-----|--------|----------------|-------------|
| `0x00` | `CMD_MAGNETIC_ATTACH_STATUS` | `0x0001` / `0x0000` | Notificación periódica de acoplamiento magnético (cada 500 ms, actualmente siempre `ATTACHED`). |
| `0x02` | `CMD_ACTION_COMPLETE` | `0x0010` | Acción del motor completada. |
| `0x03` | `CMD_MAGNETIC_SWITCH_EVENT` | Código de evento | Evento del interruptor magnético o paso de calibración. |

### Códigos de calibración magnética (enviados con CMD `0x03`)

| Código | Constante | Significado |
|--------|-----------|-------------|
| `0x0081` | `MAG_SWITCH_CALIB_START` | Inicio de recalibración |
| `0x0082` | `MAG_SWITCH_CALIB_FIRST_DONE` | Segunda posición registrada; mover a tercera |
| `0x0083` | `MAG_SWITCH_CALIB_COMPLETE` | Calibración finalizada |

---

## Eventos magnéticos por perfil

### Perfil `base` (`esp_vocat_rotating_base`)

| Valor | Evento | Descripción |
|-------|--------|-------------|
| 1 | `SLIDE_DOWN` | Deslizar de arriba a abajo |
| 2 | `SLIDE_UP` | Deslizar de abajo a arriba |
| 3 | `REMOVE_FROM_UP` | Retirar desde posición superior |
| 4 | `REMOVE_FROM_DOWN` | Retirar desde posición inferior |
| 5 | `PLACE_FROM_UP` | Colocar desde arriba |
| 6 | `PLACE_FROM_DOWN` | Colocar desde abajo |
| 7 | `SINGLE_CLICK` | Clic simple en posición inferior |
| 8 | `FISH_ATTACHED` | Accesorio pez adherido |
| 9 | `FISH_DETACHED` | Accesorio pez retirado |
| 10 | `PAIRING` | Modo emparejamiento |
| 11 | `PAIRING_CANCELLED` | Emparejamiento cancelado |

> En perfil `base`, los eventos se envían por UART directamente desde `magnetic_slide_switch.c` (sin callback en `app_main`).

### Perfil `bell` (`esp_vocat_rotating_base_bell_event_detection`)

Eventos 1–7 (misma tabla que deslizador/campana). Reporte vía callback registrado en `app_main` → `control_serial_send_magnetic_switch_event()`.

### Perfil `iphone` (`esp_vocat_rotating_base_iphone_detection`)

| Valor | Evento | Descripción |
|-------|--------|-------------|
| 16 | `IPHONE_LEAN_FRONT` | iPhone apoyado en el frente (ΔZ ≥ umbral) |
| 17 | `IPHONE_LEAN_FRONT_DETACHED` | iPhone se separa del frente |
| 18 | `IPHONE_UNDER_BASE` | iPhone debajo de la base |
| 19 | `IPHONE_UNDER_BASE_DETACHED` | iPhone retirado de debajo |

### Perfil `magnetic_accessory` (`esp_vocat_rotating_base_magnetic_accessory_detection`)

| Valor | Evento | Descripción |
|-------|--------|-------------|
| 8 | `FISH_ATTACHED` | Pez adherido |
| 9 | `FISH_DETACHED` | Pez retirado |
| 10 | `PAIRING` | Emparejamiento activo |
| 11 | `PAIRING_CANCELLED` | Emparejamiento cancelado |
| 12 | `ICE_CREAM_ATTACHED` | Helado adherido |
| 13 | `ICE_CREAM_DETACHED` | Helado retirado |
| 14 | `DONUT_ATTACHED` | Dona adherida |
| 15 | `DONUT_DETACHED` | Dona retirada |

---

## Proyectos de ejemplo — comparativa

| Proyecto | `MAG_SW_PROFILE` | Versión | Reporte de eventos | Caso de uso |
|----------|------------------|---------|-------------------|-------------|
| `esp_vocat_rotating_base` | `base` | V1.0.4 | Directo desde componente | Firmware estándar con todos los eventos base |
| `esp_vocat_rotating_base_bell_event_detection` | `bell` | V1.0.4 | Callback → UART | Deslizador tipo campana (7 eventos) |
| `esp_vocat_rotating_base_iphone_detection` | `iphone` | V1.0.4 | Callback → UART | Detección de proximidad de iPhone |
| `esp_vocat_rotating_base_magnetic_accessory_detection` | `magnetic_accessory` | V1.0.4 | Callback → UART | Accesorios magnéticos (pez, helado, dona) |

**Componentes compartidos** (idénticos en los 4 proyectos):

| Componente | Ruta | Función |
|------------|------|---------|
| `stepper_motor` | `software/common_components/stepper_motor/` | Control del motor 24BYJ48 |
| `control_serial` | `software/common_components/control_serial/` | Protocolo UART |
| `magnetic_slide_switch` | `software/common_components/magnetic_slide_switch/` | Detección magnética (perfil seleccionado en CMake) |
| `BMM150_SensorAPI` | `software/common_components/BMM150_SensorAPI/` | Driver BMM150 (I2C) |

**Selección de perfil** (en `CMakeLists.txt` de cada proyecto):

```cmake
set(MAG_SW_PROFILE "base")   # base | bell | iphone | magnetic_accessory
```

---

## Parámetros de rendimiento (documentados en firmware)

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Precisión angular | ±0,5° | Documentación del proyecto |
| Velocidad máxima | 600 µs/paso (~200°/s) | `STEPPER_SPEED_ULTRA_FAST` |
| Respuesta interruptor magnético | < 50 ms | Documentación del proyecto |
| Muestreo BMM150 | 5 ms (200 Hz) | `MAG_SAMPLE_PERIOD_MS` |
| Muestreo QMC6309 | 2 ms (500 Hz) | `MAG_SAMPLE_PERIOD_MS` |
| Estabilidad en calibración | 500 ms | `CALIBRATION_STABILITY_TIME_MS` |
| UART | 115200 bps, 8N1 | `control_serial.h` |
| RAM / Flash | ~80 KB / ~200 KB | Documentación del proyecto |
| Timeout homing motor | 2000 ms | `base_calibration_task` |
| Ángulo de centrado tras homing | 95° a la derecha | `base_calibration_task` |

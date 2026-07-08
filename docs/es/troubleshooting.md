# Resolución de problemas (Troubleshooting)

> Basado en: documentación del repositorio, comentarios en código fuente y comportamiento observable del firmware.

[← Volver a la guía principal](../../README_ES.md) · [Arranque del firmware](arranque-firmware.md)

---

## Índice rápido

| Síntoma | Sección |
|---------|---------|
| Motor no encuentra Home | [§1](#1-el-motor-no-encuentra-el-home) |
| Sensor no calibra | [§2](#2-el-sensor-no-calibra) |
| Error UART | [§3](#3-error-de-comunicación-uart) |
| Sensor mal configurado | [§4](#4-configuración-incorrecta-del-sensor) |
| Fallo al compilar | [§5](#5-problemas-al-compilar-con-esp-idf) |
| Motor vibra o no gira | [§6](#6-motor-vibra-o-no-gira) |
| Clic magnético errático | [§7](#7-evento-de-clic-falso-o-no-detectado) |
| Rotación en dirección incorrecta | [§8](#8-rotación-incorrecta-en-el-primer-arranque) |

---

## 1. El motor no encuentra el Home

### Síntomas
- Log: `Calibration timeout! Limit switch not pressed within 2 seconds`
- Log: `Assuming mechanical fault, moving directly to home position`
- La base gira 95° sin haber tocado el fin de carrera.

### Causas probables (según `base_calibration_task`)

| Causa | Verificación |
|-------|--------------|
| Fin de carrera mal conectado | GPIO 1, activo en bajo (`active_level = 0`) |
| Fin de carrera mal posicionado mecánicamente | El motor gira -5° en bucle; debe activarse en ≤ 2 s |
| Cable del interruptor roto o invertido | Medir continuidad en GPIO 1 |
| Motor no gira (sin alimentación) | Ver [§6](#6-motor-vibra-o-no-gira) |

### Solución

1. Verificar cableado del fin de carrera en GPIO 1 (ver [tablas-referencia.md](tablas-referencia.md)).
2. Confirmar que el motor gira a la izquierda durante el homing (log `Base calibration task started`).
3. Ajustar la posición mecánica del interruptor de fin de carrera.
4. Si el timeout es intencional (entorno de prueba sin fin de carrera), el firmware usa **modo fallback**: gira +95° directamente. La posición angular puede ser imprecisa.

### Referencia de código

```c
// esp_vocat_rotating_base_main.c — timeout 2000 ms
const TickType_t timeout_ticks = pdMS_TO_TICKS(2000);
// Tras fin de carrera: stepper_rotate_angle_with_accel(95.0, STEPPER_SPEED_FAST);
```

---

## 2. El sensor no calibra

### Síntomas
- La base permanece en calibración magnética indefinidamente.
- No se inicia `slide_switch_event_detect_task` (log ausente: `Calibration completed, starting slide switch detection task`).
- Log sin `MAG_SWITCH_CALIB_COMPLETE` en UART.

### Causas probables

| Causa | Verificación |
|-------|--------------|
| Posiciones no suficientemente distintas | Diferencia entre posiciones debe ser > 100 (`CALIBRATION_VALUE_DIFF_THRESHOLD`) |
| Usuario no mantiene posición 500 ms | `CALIBRATION_STABILITY_TIME_MS = 500` |
| I2C no conectado | SCL=GPIO3, SDA=GPIO2; dirección BMM150=0x10 |
| Sensor incorrecto en menuconfig | `idf.py menuconfig` → Magnetic Slide Switch → Sensor Type |
| NVS corrupto | Borrar flash: `idf.py erase-flash` |

### Procedimiento de calibración correcto

1. Encender la base (primera vez o tras `erase-flash`).
2. **Posición 1:** dejar el deslizador inmóvil ~500 ms.
3. **Posición 2:** mover a posición claramente diferente (arriba/abajo/retirado); esperar ~500 ms.
   - La base envía `0x0082` (segunda posición OK).
4. **Posición 3:** tercera posición distinta; esperar ~500 ms.
   - La base envía `0x0083` (calibración completa).
5. Los datos se guardan en NVS automáticamente.

### Recalibración manual

- **Botón Boot:** pulsación larga en GPIO 9 (`BUTTON_LONG_PRESS_START`).
- **UART:** `AA 55 00 03 03 00 10 13` (`MAG_SWITCH_CMD_RECALIBRATE`).

---

## 3. Error de comunicación UART

### Síntomas
- ESP-VoCat no recibe eventos ni responde a movimientos.
- Log: `Checksum verification failed` o `Frame header not found`.
- Log: `Unknown command code`.

### Verificaciones

| Parámetro | Valor esperado | Fuente |
|-----------|----------------|--------|
| Baudrate | 115200 | `ECHO_UART_BAUD_RATE` |
| Formato | 8N1, sin flow control | `control_serial_init()` |
| TX base | GPIO 29 | Conectar a RX del host |
| RX base | GPIO 8 | Conectar a TX del host |
| Cabecera | `0xAA 0x55` | Obligatoria en cada trama |
| Checksum | Suma de CMD + DATA | Ver [tablas-referencia.md](tablas-referencia.md) |

### Errores frecuentes

| Error | Causa |
|-------|-------|
| TX conectado a TX | Inversión de líneas; usar cruce TX↔RX |
| Checksum incorrecto | Recalcular: suma aritmética de bytes CMD+DATA |
| Ángulo ignorado | Valor > 180 o resultado fuera de rango 0–180° absoluto |
| Trama cortada | `LEN` no coincide con bytes reales |

### Herramientas de depuración

```bash
idf.py monitor          # Ver logs de parsing UART
```

Enviar trama de prueba (ángulo 90° = sin movimiento):
```
AA 55 00 03 01 00 5A 5B
```
Checksum: `0x01 + 0x00 + 0x5A = 0x5B`

---

## 4. Configuración incorrecta del sensor

### Síntomas
- Lecturas magnéticas erráticas o siempre cero.
- Solo funcionan SLIDE_UP/DOWN (cuando se esperan más eventos).
- Log de error I2C en `magnetometer_data_read_task`.

### Matriz de configuración

| Hardware montado | menuconfig requerido |
|------------------|---------------------|
| BMM150 | `SENSOR_MAGNETOMETER` + `SENSOR_BMM150` |
| QMC6309 | `SENSOR_MAGNETOMETER` + `SENSOR_QMC6309` |
| Hall lineal | `SENSOR_LINEAR_HALL` |

### Limitaciones documentadas en código

- **Hall lineal:** solo `SLIDE_UP` / `SLIDE_DOWN` (sin calibración de 3 posiciones completa).
- **BMM150 vs QMC6309:** umbrales diferentes en cada header de perfil; no intercambiar sin recalibrar.

### Verificación I2C

| Sensor | Dirección I2C | Chip ID esperado |
|--------|---------------|------------------|
| BMM150 | `0x10` | `0x32` |
| QMC6309 | `0x7C` | `0x90` |

Tras cambiar sensor en menuconfig: `idf.py fullclean build flash` y recalibrar.

---

## 5. Problemas al compilar con ESP-IDF

### Requisitos

| Requisito | Valor | Fuente |
|-----------|-------|--------|
| ESP-IDF | ≥ 5.5.0 | `idf_component.yml` |
| Target | `esp32c61` | MCU de la base |
| Dependencia | `espressif/button == 3.5.0` | `idf_component.yml` |

### Errores comunes

| Error | Solución |
|-------|----------|
| `Unknown MAG_SW_PROFILE` | Verificar `set(MAG_SW_PROFILE "...")` en CMakeLists del proyecto |
| Componente no encontrado | Confirmar `EXTRA_COMPONENT_DIRS` apunta a `../common_components` |
| Target incorrecto | `idf.py set-target esp32c61` antes de `build` |
| Versión IDF antigua | Actualizar a release/v5.5 o superior |
| `managed_components` faltante | Ejecutar `idf.py build` (descarga automática vía Component Manager) |

### Secuencia de compilación recomendada

```bash
cd software/esp_vocat_rotating_base
idf.py set-target esp32c61
idf.py menuconfig    # Opcional: tipo de sensor
idf.py build
idf.py -p PORT flash monitor
```

### Selección del proyecto correcto

Cada demo es un directorio independiente. No compilar desde la raíz del repositorio; entrar al subdirectorio del proyecto deseado.

---

## 6. Motor vibra o no gira

| Causa | Solución |
|-------|----------|
| Alimentación insuficiente | Mínimo 5 V / 1 A recomendado en documentación |
| Cableado IN1–IN4 incorrecto | GPIO 28, 27, 26, 25 respectivamente |
| Velocidad demasiado alta | Aumentar `speed_us` (valor más alto = más lento) |
| Motor bloqueado mecánicamente | Verificar engranajes y carga |

---

## 7. Evento de clic falso o no detectado

Basado en umbrales del perfil `base` con BMM150:

| Problema | Causa | Solución |
|----------|-------|----------|
| Falso clic al deslizar | Transición rápida en eje X/Y | El firmware filtra con relación mag_x/mag_y |
| Clic no detectado | Deslizador no en posición DOWN | Requiere mag_x > mag_y |
| Clic demasiado lento | Duración > 500 ms (BMM150) | Acción rápida < 300 ms recomendada en docs |

---

## 8. Rotación incorrecta en el primer arranque

| Causa | Solución |
|-------|----------|
| Fin de carrera en lado incorrecto | Revisar montaje mecánico |
| Ángulo de centrado incorrecto | Valor fijo 95° en `base_calibration_task`; ajustar mecánica, no software sin validar |

---

## 9. Otros problemas documentados en código

| Problema | Detalle | Fuente |
|----------|---------|--------|
| `BEAT_SWING` sin notificación de fin | `control_serial_send_action_complete()` comentado para `STEPPER_ACTION_BEAT_SWING` | `control_serial.c` línea ~198 |
| Detección de acoplamiento siempre ATTACHED | `magnetic_detect_task` envía siempre `0x0001`; TODO para detección real | `control_serial.c` |
| `app_main` bloqueado en calibración | `magnetic_slide_switch_start()` espera calibración antes de retornar | Diseño intencional |

---

## Registro de diagnóstico

Al reportar un problema, incluir:

1. Proyecto compilado (`esp_vocat_rotating_base` / demo).
2. Perfil (`MAG_SW_PROFILE`) y sensor (`menuconfig`).
3. Versión ESP-IDF (`idf.py --version`).
4. Log completo de `idf.py monitor` desde el arranque.
5. Trama UART enviada (hex) si aplica.

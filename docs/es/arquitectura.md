# Arquitectura del sistema

> Derivado de: `app_main`, `control_serial.c`, `stepper_motor.c`, `magnetic_slide_switch/`, `CMakeLists.txt` de cada proyecto.

[← Volver a la guía principal](../../README_ES.md) · [Tablas de referencia](tablas-referencia.md)

---

## 1. Arquitectura general

```mermaid
flowchart TB
    subgraph Host["ESP-VoCat (Host)"]
        SSL[Localización de fuente sonora]
        UI[Interfaz / animaciones]
        HOST_UART[UART TX/RX]
    end

    subgraph Base["Base rotatoria (ESP32-C61)"]
        APP[app_main]
        UART[control_serial]
        MOTOR[stepper_motor]
        MAG[magnetic_slide_switch]
        NVS[(NVS Flash)]

        APP --> UART
        APP --> MOTOR
        APP --> MAG
        MAG --> NVS
        UART --> MOTOR
        MAG --> UART
    end

    subgraph HW["Hardware"]
        STEPPER[24BYJ48 + ULN2003]
        LIMIT[Fin de carrera GPIO1]
        SENSOR[BMM150 / QMC6309 / Hall]
        BOOT[Botón Boot GPIO9]
    end

    HOST_UART <-->|115200 bps| UART
    MOTOR --> STEPPER
    APP --> LIMIT
    APP --> BOOT
    MAG --> SENSOR
```

La base actúa como **periférico inteligente**: recibe comandos de ángulo y acción del host ESP-VoCat, ejecuta movimiento mecánico y reporta eventos del interruptor magnético de vuelta por UART.

---

## 2. Hardware, firmware y componentes compartidos

```mermaid
flowchart LR
    subgraph Physical["Capa física"]
        PCB[PCB Main + Sub Board]
        MECH[3D_models / mecánica]
        MOTOR_HW[Motor + fin de carrera]
        MAG_HW[Sensor magnético]
    end

    subgraph FW["Capa firmware (ESP-IDF)"]
        subgraph Apps["Aplicaciones (4 proyectos)"]
            A1[esp_vocat_rotating_base]
            A2[bell_event_detection]
            A3[iphone_detection]
            A4[magnetic_accessory_detection]
        end

        subgraph Common["common_components"]
            SM[stepper_motor]
            CS[control_serial]
            MSS[magnetic_slide_switch]
            BMM[BMM150_SensorAPI]
        end

        subgraph IDF["ESP-IDF / drivers"]
            GPIO_DRV[driver/gpio]
            UART_DRV[driver/uart]
            I2C_DRV[driver/i2c / i2c_bus]
            ADC_DRV[driver/adc]
            NVS_DRV[nvs_flash]
            BTN[espressif/button]
        end
    end

    PCB --> MOTOR_HW
    PCB --> MAG_HW
    MECH --> MOTOR_HW

    A1 & A2 & A3 & A4 --> SM
    A1 & A2 & A3 & A4 --> CS
    A1 & A2 & A3 & A4 --> MSS
    MSS --> BMM

    SM --> GPIO_DRV
    CS --> UART_DRV
    MSS --> I2C_DRV
    MSS --> ADC_DRV
    MSS --> NVS_DRV
    A1 --> BTN
```

**Nota sobre capas HAL:** Este repositorio no define un directorio `hal/` explícito. La abstracción de hardware se implementa dentro de cada componente (`stepper_motor` encapsula GPIO; `magnetic_slide_switch` encapsula I2C/ADC; `control_serial` encapsula UART), apoyándose en los drivers oficiales de ESP-IDF.

---

## 3. Flujo de comunicación UART

```mermaid
sequenceDiagram
    participant Host as ESP-VoCat
    participant UART as uart_cmd_receive_task
    participant Motor as stepper_motor
    participant Mag as magnetic_slide_switch

    Note over Host,Mag: Recepción de comando (Host → Base)
    Host->>UART: Trama AA 55 ...
    UART->>UART: Sincronizar cabecera 0xAA 0x55
    UART->>UART: Validar longitud y checksum
    alt CMD 0x01 Ángulo
        UART->>Motor: stepper_rotate_angle_with_accel(diff)
        Motor-->>UART: Rotación completada
        UART->>Motor: stepper_motor_power_off()
    else CMD 0x02 Acción
        UART->>Motor: stepper_shake_head / look_around / ...
        Motor-->>UART: Acción completada
        UART->>Host: CMD 0x02 ACTION_COMPLETE (0x0010)
    else CMD 0x03 Recalibrar
        UART->>Mag: magnetic_slide_switch_start_recalibration()
    end

    Note over Host,Mag: Notificación de evento (Base → Host)
    Mag->>Host: CMD 0x03 + código de evento
    Note over UART,Host: magnetic_detect_task envía CMD 0x00 cada 500 ms
```

**Reglas de parsing** (`control_serial.c`):
1. Búsqueda de cabecera `0xAA 0x55` en el buffer recibido.
2. Lectura de `LEN` y validación de trama completa.
3. Cálculo de checksum **antes** de ejecutar el comando.
4. Para ángulo: rango válido 0–180°; posición absoluta interna inicializada en 90°.

---

## 4. Flujo de inicialización del sistema

```mermaid
flowchart TD
    START([Reset / Power-on]) --> NVS[nvs_flash_init]
    NVS -->|Error NVS| ERASE[nvs_flash_erase + reinit]
    ERASE --> SEM[Semáforo fin de carrera]
    NVS --> SEM
    SEM --> GPIO_MOTOR[stepper_motor_gpio_init]
    GPIO_MOTOR --> LIMIT_INIT[base_angle_limit_switch_init]
    LIMIT_INIT --> BOOT_INIT[boot_button_init]
    BOOT_INIT --> UART_INIT[control_serial_init]
    UART_INIT --> MAG_TASK[control_serial_start_magnetic_detect_task]
    MAG_TASK --> CAL_TASK[xTaskCreate base_calibration_task]
    CAL_TASK --> MAG_START[magnetic_slide_switch_start]

    MAG_START --> I2C_INIT[Inicializar I2C + sensor]
    I2C_INIT --> MAG_READ[xTaskCreate magnetometer_data_read_task]
    MAG_READ --> CAL_MAG[xTaskCreate magnetometer_calibration_task]
    CAL_MAG --> WAIT_CAL{Calibración magnética<br/>en NVS o automática}
    WAIT_CAL -->|Completa| DETECT[xTaskCreate slide_switch_event_detect_task]
    DETECT --> READY([Modo operativo])

    CAL_TASK --> HOMING[Girar izq. hasta fin de carrera]
    HOMING -->|Timeout 2s| FALLBACK[Girar 95° derecha]
    HOMING -->|Fin de carrera| CENTER[Girar 95° derecha]
    FALLBACK --> MOTOR_OFF[stepper_motor_power_off]
    CENTER --> MOTOR_OFF
    MOTOR_OFF --> HOMING_DONE[Tarea homing finalizada]
```

**Orden real en `app_main`** (líneas 154–181 de `esp_vocat_rotating_base_main.c`):

| Paso | Función | Descripción |
|------|---------|-------------|
| 1 | `nvs_flash_init()` | Persistencia para calibración magnética |
| 2 | `xSemaphoreCreateBinary()` | Sincronización fin de carrera ↔ homing |
| 3 | `stepper_motor_gpio_init()` | Configura GPIO 25–28 como salidas |
| 4 | `base_angle_limit_switch_init()` | GPIO 1 + callbacks `iot_button` |
| 5 | `boot_button_init()` | GPIO 9; pulsación larga → recalibración |
| 6 | `control_serial_init()` | UART1 @ 115200 + `uart_cmd_receive_task` |
| 7 | `control_serial_start_magnetic_detect_task()` | Reporte periódico de acoplamiento |
| 8 | `xTaskCreate(base_calibration_task)` | Homing mecánico (paralelo) |
| 9 | `magnetic_slide_switch_start()` | I2C, calibración magnética, detección |

> **I2C:** La inicialización del bus I2C y del sensor BMM150/QMC6309 ocurre dentro de `magnetic_slide_switch_start()` → `magnetometer_data_read_task`, no en `app_main`.

---

## 5. Flujo de calibración automática magnética

```mermaid
stateDiagram-v2
    [*] --> CALIBRATION_IDLE
    CALIBRATION_IDLE --> CALIBRATION_DETECTING_FIRST: Sin datos NVS / recalibración
    CALIBRATION_DETECTING_FIRST --> CALIBRATION_WAITING_CHANGE_1: Posición 1 estable 500ms
    CALIBRATION_WAITING_CHANGE_1 --> CALIBRATION_DETECTING_SECOND: diff > 100
    CALIBRATION_DETECTING_SECOND --> CALIBRATION_WAITING_CHANGE_2: Posición 2 estable 500ms
    note right of CALIBRATION_DETECTING_SECOND: UART 0x0082 (2ª posición OK)
    CALIBRATION_WAITING_CHANGE_2 --> CALIBRATION_DETECTING_THIRD: diff > 100
    CALIBRATION_DETECTING_THIRD --> CALIBRATION_COMPLETED: Posición 3 estable 500ms
    note right of CALIBRATION_DETECTING_THIRD: Ordenar REMOVED/UP/DOWN + NVS
    CALIBRATION_COMPLETED --> [*]: UART 0x0083
```

**Asignación automática** (tras la tercera posición):
- Valor magnético **menor** → `REMOVED`
- Valor **intermedio** → `UP`
- Valor **mayor** → `DOWN`

Constantes (`magnetic_slide_switch.h`, BMM150): `CALIBRATION_STABILITY_TIME_MS = 500`, `CALIBRATION_VALUE_DIFF_THRESHOLD = 100`.

---

## 6. Máquina de estados del interruptor magnético (perfil `base`)

Durante el modo operativo, `slide_switch_event_detect_task` evalúa el eje Z filtrado (ventana deslizante) contra los umbrales calibrados:

```mermaid
stateDiagram-v2
    [*] --> INIT
    INIT --> REMOVED: Estado inicial detectado
    REMOVED --> UP: PLACE_FROM_UP / campo aumenta
    REMOVED --> DOWN: PLACE_FROM_DOWN
    UP --> DOWN: SLIDE_DOWN
    DOWN --> UP: SLIDE_UP
    UP --> REMOVED: REMOVE_FROM_UP
    DOWN --> REMOVED: REMOVE_FROM_DOWN
    DOWN --> DOWN: SINGLE_CLICK (transitorio)
    REMOVED --> FISH: FISH_ATTACHED (Δ campo 150–200)
    FISH --> REMOVED: FISH_DETACHED
    REMOVED --> PAIRING: Campo cae > umbral
    PAIRING --> REMOVED: PAIRING_CANCELLED
```

Cada transición confirmada dispara `control_serial_send_magnetic_switch_event()` en perfil `base`, o invoca callbacks registrados en perfiles `bell`, `iphone` y `magnetic_accessory`.

---

## 7. Flujo de ejecución de acciones del motor

```mermaid
flowchart LR
    CMD[CMD 0x02 recibido] --> PARSE[Extraer action 16 bits]
    PARSE --> SWITCH{stepper_action_type_t}
    SWITCH -->|0| SHAKE[stepper_shake_head]
    SWITCH -->|1| DECAY[stepper_shake_head_decay]
    SWITCH -->|2| LOOK[stepper_look_around]
    SWITCH -->|3| BEAT[stepper_beat_swing]
    SWITCH -->|4| NUZZLE[stepper_cat_nuzzle]
    SHAKE & DECAY & LOOK & NUZZLE --> OFF[stepper_motor_power_off]
    OFF --> NOTIFY[control_serial_send_action_complete]
    BEAT --> OFF2[stepper_motor_power_off]
    OFF2 --> DONE[Sin notificación en código actual]
```

Todas las funciones de acción utilizan **half-step** (8 pasos por ciclo) con curvas de aceleración/desaceleración (`STEPPER_ACCEL_STEPS = 30`, `STEPPER_DECEL_STEPS = 30`).

---

## 8. Arquitectura del código

```
software/
├── esp_vocat_rotating_base/              # Aplicación (perfil base)
│   └── main/
│       ├── esp_vocat_rotating_base_main.c   # app_main, homing, botones
│       ├── CMakeLists.txt
│       └── idf_component.yml
├── esp_vocat_rotating_base_*_*/          # Aplicaciones demo (otros perfiles)
│   └── main/                             # Igual estructura + callback UART
└── common_components/
    ├── stepper_motor/                    # Lógica de movimiento
    │   ├── stepper_motor.c
    │   └── include/stepper_motor.h
    ├── control_serial/                   # Protocolo UART
    │   ├── control_serial.c
    │   └── include/control_serial.h
    ├── magnetic_slide_switch/            # Detección magnética multi-perfil
    │   ├── CMakeLists.txt                # Selección MAG_SW_PROFILE
    │   ├── Kconfig                       # Tipo de sensor
    │   └── profiles/
    │       ├── base/
    │       ├── bell/
    │       ├── iphone/
    │       └── magnetic_accessory/
    └── BMM150_SensorAPI/                 # Driver Bosch BMM150
```

### Tareas FreeRTOS en ejecución (magnetómetro, perfil típico)

| Tarea | Prioridad | Origen | Función |
|-------|-----------|--------|---------|
| `uart_cmd_receive_task` | 12 | `control_serial_init` | Recibe y despacha comandos UART |
| `base_calibration_task` | 10 | `app_main` | Homing mecánico (se autodestruye) |
| `magnetic_detect_task` | 5 | `control_serial` | Reporte periódico acoplamiento |
| `mag_data_read_task` | 3 | `magnetic_slide_switch` | Lectura continua del sensor |
| `mag_calibration_task` | 3 | `magnetic_slide_switch` | Calibración automática |
| `slide_switch_detect_task` | 2 | `magnetic_slide_switch` | Detección de eventos |

### Comunicación entre módulos

```mermaid
flowchart LR
    MAIN[app_main] -->|init| CS[control_serial]
    MAIN -->|init| SM[stepper_motor]
    MAIN -->|start| MSS[magnetic_slide_switch]
    CS -->|comandos ángulo/acción| SM
    MSS -->|eventos UART| CS
    MSS -->|lee/escribe| NVS[(NVS)]
    MSS -->|I2C| BMM[BMM150_SensorAPI]
    CS -->|UART| HOST[ESP-VoCat]
```

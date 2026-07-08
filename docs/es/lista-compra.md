# Lista de compra — ESP-VoCat Base V1.0

> Lista orientada a la compra y fabricación. Detalle de designadores en [BOM.md](BOM.md).  
> **PCB:** fabricar desde [OSHWHUB esp-echoear-base](https://oshwhub.com/esp-college/esp-echoear-base) (Gerber no incluido en este repo).

[← BOM](BOM.md) · [Guía de ensamblaje](guia-ensamblaje.md)

---

## Componentes electrónicos

### Obligatorios (función mínima del firmware)

| Cant. | Descripción | MPN / referencia | Notas |
|-------|-------------|------------------|-------|
| 1 | Módulo ESP32-C61-WROOM-1 | ESP32-C61-WROOM-1-N8R2 | **Espressif** — no sustituir por ESP32 clásico sin adaptar firmware |
| 1 | Regulador buck TLV62569DBVR | TLV62569DBVR | 5 V → 3,3 V |
| 1 | Interruptor potencia TPS2051BDBVR | TPS2051BDBVR | Límite 500 mA |
| 1 | Driver ULN2003A | ULN2003A | Motor paso a paso |
| 1 | MOSFET AO3400A | AO3400A | Rama RGB (soldar aunque no uses LED) |
| 1 | Sensor Hall lineal SS49E | SS49E | Perfil `ss49e` |
| **1** | **Magnetómetro (elegir uno)** | BMM150 **o** QMC6309 | Solo uno en PCB; BMM150 = perfil por defecto |
| 1 | Pulsador Boot GT-TC072A-H060-L1 | GT-TC072A-H060-L1 | O tact switch 6×6 mm equivalente |
| 1 | Inductor 2,2 µH | **Pendiente de verificar** (BOM OSHWHUB) | Para buck |
| 1 | Condensador 22 µF | **Pendiente de verificar** encapsulado | C7 |
| 1 | Condensador 10 nF | C0402 genérico | C15 filtro Hall |
| 3 | Condensador 10 µF | CL10A106K o 0603 10 µF X5R | C1, C3, C8 |
| 9 | Condensador 100 nF | CL05B104K o 0402 100 nF | C2, C4, C5, C6, C10–C14 |
| 1 | Condensador 1 µF | CL05A105K o 0402 1 µF | C9 |
| 2 | Resistencia 5,1 kΩ | 0402/0603 | CC USB |
| 1 | Resistencia 100 kΩ | 0402/0603 | FB DC-DC |
| 1 | Resistencia 22,1 kΩ (o 22 kΩ) | 0402/0603 | FB DC-DC — verificar valor exacto en BOM |
| 1 | Resistencia 1 kΩ | 0402/0603 | R7 |
| 4 | Resistencia 10 kΩ | 0402WGF1002 | R3, R6, R10, R11 |
| 2 | Resistencia 4,7 kΩ | 0402WGF4700 | R8, R9 |
| 6+ | Diodos D1–D7 | **Pendiente de verificar** | Ver esquemático OSHWHUB |
| 1 | LED indicador | **Pendiente de verificar** | LED1 |
| 2 | PCB | Main + Sub Board V1.0 | Espesor 1,0 mm |

### Sub Board (obligatorio para homing UART)

| Cant. | Descripción | MPN / referencia | Notas |
|-------|-------------|------------------|-------|
| 1 | PCB Sub Board | ESP-VoCat-Base-SubBoard-V1_0 | — |
| 1 | Micro interruptor TM-8764-1 | TM-8764-1 | Fin de carrera |
| 1 | Pogo pin 4P 2,5 mm | **Pendiente de verificar** | U1 Sub Board |
| 1 | Resistencia 51 kΩ | — | R1 |
| 1 | Resistencia 100 kΩ | — | R2 |

### Opcionales (hardware presente, firmware demo limitado)

| Cant. | Descripción | Notas |
|-------|-------------|-------|
| 1 | Módulo radar LD2402 | Header H1; no usado en demos actuales |
| 1 | Tira / LED WS2812B | Conector CN4; control vía Q1 |

---

## Conectores

| Cant. | Descripción | Referencia PCB | Notas |
|-------|-------------|----------------|-------|
| 1 | USB Type-C 16P | TYPE-C 16PIN 2MD(073) | **Pendiente MPN** — OSHWHUB |
| 1 | Wafer 1,25 mm 5P | 1.25-5P WT | Motor CN1 |
| 2 | Wafer SH1.0 5P | WAFER-SHB1.0-5PLT-W1-P | CN3 Main + CN1 Sub |
| 1 | Header 1,25 mm 4P | HC-1.25-4PLT | I2C CN2 |
| 1 | Header 1,25 mm 3P | HC-1.25-3PLT | RGB CN4 |
| 1 | Header 2,54 mm 5P | PZ254V-11-05P | LD2402 H1 |
| 1 | Cable FFC SH1.0 5P 60 mm | — | Misma dirección de contactos (OSHWHUB) |

---

## Sensores

| Cant. | Sensor | Perfil firmware | Alternativa |
|-------|--------|-----------------|-------------|
| 1 | BMM150 (I2C 0x10) | `bmm150` (por defecto) | — |
| **o** 1 | QMC6309 (I2C 0x7C) | `qmc6309` | Sustituye a BMM150 en PCB |
| 1 | SS49E (analógico) | `ss49e` | Otros Hall lineales — recalibrar ADC |

---

## Motor

| Cant. | Descripción | Especificación |
|-------|-------------|----------------|
| 1 | Motor paso a paso 24BYJ48 | 5 V DC, 4 fases, reducción interna típica 1:64 |
| 1 | Cable motor | Incluido con el motor; conector compatible CN1 1,25 mm 5P |

---

## Tornillería

| Cant. | Especificación | Uso |
|-------|----------------|-----|
| 2 | M4 × 5 mm | Fijación motor a base |
| 2 | M2 × 4 mm | Fijación Main Board |
| 2 | M2 × 3 mm | Cubierta superior plato |

---

## Imanes

| Cant. | Especificación | Uso |
|-------|----------------|-----|
| 2 | Imán circular D10 × 1,5 mm | Acoplamiento magnético carcasa / ESP-VoCat (OSHWHUB paso 1 de montaje) |
| 1 | Imán circular D6 × 5 mm | Pieza deslizador magnético (impresión 3D) |

> **Discrepancia OSHWHUB:** el paso 1 de montaje indica **2** imanes D10×1,5 mm, pero la lista de compra OSHWHUB menciona **1** unidad. Se recomienda comprar **2** para replicar el ensamblaje documentado.

---

## Piezas impresas en 3D

Archivos en `3D_models/` (correspondencia con OSHWHUB en [guía de ensamblaje](guia-ensamblaje.md#impresión-3d)):

| Archivo | Pieza OSHWHUB | Cant. |
|---------|---------------|-------|
| `ESP-VoCat_catbase_20251128.stp` | Carcasa exterior | 1 |
| `ESP-VoCat_catbase_platform_btm_20251128.stp` | Cubierta inferior carcasa / base plato | 1 |
| `ESP-VoCat catbase cover 2025-11-22.STEP` | Cubierta plato giratorio | 1 |
| `ESP-VoCat catbase platform top 2025-11-22.STEP` | Tapa inferior plato | 1 |
| `ESP-VoCat catbase ball only 2025-11-22.STEP` | Interruptor deslizante magnético | 1 |

Parámetros de impresión: ver [guia-ensamblaje.md → Impresión 3D](guia-ensamblaje.md#impresión-3d) (no documentados en archivos STEP).

---

## Mecánica adicional

| Cant. | Descripción | Notas |
|-------|-------------|-------|
| 1 | Rodamiento 7 × 11 × 3 mm | **Pendiente MPN** — OSHWHUB |

---

## Espressif vs equivalentes comerciales

| Componente | ¿Espressif / proyecto? | ¿Reemplazable? | Comentario |
|------------|------------------------|----------------|------------|
| **ESP32-C61-WROOM-1** | Sí (Espressif) | **No** sin portar firmware | Único MCU soportado en este repo |
| **BMM150** | No (Bosch); perfil por defecto | Sí → QMC6309 | Cambiar `MAG_SW_PROFILE` y soldar solo un magnetómetro |
| **QMC6309** | No (QST) | Sí → BMM150 | Mutuamente excluyentes en PCB |
| **SS49E** | No (Honeywell) | Parcial | Otros Hall lineales; requiere calibración ADC |
| **LD2402** | Referencia Espressif ecosystem | Sí (omitir) | Opcional; no en firmware demo |
| **TLV62569DBVR** | No (TI) | Sí | Buck 3,3 V con mismas corrientes/pinout |
| **TPS2051BDBVR** | No (TI) | Sí | Power switch USB 500 mA |
| **ULN2003A** | No | Sí | Clones ampliamente disponibles |
| **AO3400A** | No | Sí | MOSFET N canal genérico |
| **24BYJ48** | No | Sí | Cualquier 24BYJ48 5V estándar |
| **PCB** | Diseño Espressif | Fabricar copia | Gerber desde OSHWHUB |
| **Carcasa 3D** | Diseño proyecto | Replicar STEP | Sin licencia adicional en repo |
| Pasivos (R, C) | No | Sí | Valores estándar 0402/0603 |
| Conectores | Footprints genéricos | Parcial | Respetar paso 1,0 / 1,25 / 2,54 mm |
| **TM-8764-1** | No | Sí | Micro switch activo bajo similar |
| **GT-TC072A-H060-L1** | No | Sí | Tact switch 6×6 mm |

---

## Orden sugerido de compra

1. Descargar Gerber + BOM completa desde OSHWHUB.
2. Pedir PCB + SMT (JLCPCB u otro) con BOM oficial.
3. Comprar motor, cable FFC, imanes, rodamiento y tornillería.
4. Imprimir piezas 3D mientras llega el PCB.
5. Reservar ESP32-C61-WROOM-1 (disponibilidad variable según región).

---

*Cantidades alineadas con una unidad. Para varias unidades, multiplicar salvo resistencias/diodos ya agrupados por valor en BOM.*

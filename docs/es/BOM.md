# BOM — Lista de materiales (ESP-VoCat Base V1.0)

> **Fuentes:** esquemáticos PDF en `hardware/`, exportación parcial OSHWHUB en `docs/7726, 2155.txt`, PCB PDF (designadores).  
> **Versión hardware:** V1.0 (2026-03-11)  
> **BOM completa en CSV:** no incluida en el repositorio → descargar en [OSHWHUB esp-echoear-base](https://oshwhub.com/esp-college/esp-echoear-base)

[← Guía de fabricación](guia-ensamblaje.md) · [Lista de compra](lista-compra.md) · [Hardware](hardware.md)

---

## Leyenda de estado

| Estado | Significado |
|--------|-------------|
| **Confirmado** | Valor/designador extraído del esquemático PDF |
| **MPN parcial** | Código de fabricante parcial desde OSHWHUB (exportación incompleta) |
| **Pendiente de verificar** | Dato no presente en el repositorio; verificar en OSHWHUB o esquemático interactivo |

---

## Main Board (`ESP-VoCat-Base-MainBoard-V1_0`)

### Circuitos integrados y módulos

| Designador | Componente | Valor | Encapsulado | Fabricante | MPN / referencia | Alternativas | Cant. | Función | Estado |
|------------|------------|-------|-------------|------------|------------------|--------------|-------|---------|--------|
| `U1` | Módulo Wi-Fi MCU | ESP32-C61-WROOM-1 | Módulo SMD | **Espressif** | ESP32-C61-WROOM-1-N8R2 (OSHWHUB) | ESP32-C61-WROOM-1U | 1 | MCU principal, UART, I2C, ADC, GPIO | Confirmado |
| `U2` | Regulador buck DC-DC | TLV62569 | SOT-23-6 (`DBVR`) | Texas Instruments | TLV62569DBVR | **Pendiente de verificar** — buck 5V→3,3V equivalente | 1 | Alimentación 3,3 V | Confirmado |
| `U3` | Interruptor de potencia USB | TPS2051B | SOT-23-5 (`DBVR`) | Texas Instruments | TPS2051BDBVR | TPS2051C, AP2161 (verificar pinout) | 1 | Limitación 500 mA a `VBUS_OUT` | Confirmado |
| `U4` | Driver Darlington | ULN2003A | DIP-16 / SOP-16 | TI / múltiples | ULN2003A | ULN2003AN, TD62783 | 1 | Driver motor paso a paso | Confirmado |
| `U5` | Magnetómetro 3 ejes | BMM150 | **WLCSP** (OSHWHUB) | Bosch Sensortec | BMM150 | — (excluyente con U6) | 1 | Sensor magnético I2C 0x10 | Confirmado |
| `U6` | Magnetómetro 3 ejes (alt.) | QMC6309 | **WLCSP** (OSHWHUB) | QST | QMC6309 | — (excluyente con U5) | 1 | Sensor magnético I2C 0x7C | Confirmado |
| `U7` | Sensor Hall lineal | SS49E | — | Honeywell | SS49E | SS49E-T, otros Hall lineales (verificar curva ADC) | 1 | Detección magnética analógica | Confirmado |
| `Q1` | MOSFET N | AO3400A | SOT-23 | AOS / Alpha & Omega | AO3400A | 2N7002, SI2302 (verificar Id/Vgs) | 1 | Control / nivel WS2812B | Confirmado |

### Conectores y electromecánicos

| Designador | Componente | Valor / modelo PCB | Encapsulado | Fabricante | MPN | Alternativas | Cant. | Función | Estado |
|------------|------------|-------------------|-------------|------------|-----|--------------|-------|---------|--------|
| `USB1` | USB Type-C receptáculo | TYPE-C 16PIN 2MD(073) | SMD 16P | **Pendiente de verificar** | — | USB-C 16P con CC (ver OSHWHUB) | 1 | Entrada 5 V + USB debug | Confirmado (ref. PCB) |
| `CN1` | Conector motor | 1.25-5P WT | Wafer 1,25 mm 5P | **Pendiente de verificar** | — | Conector 1,25 mm 5P ángulo recto | 1 | Cable motor 24BYJ48 | Confirmado (ref. PCB) |
| `CN3` | Conector Sub Board | WAFER-SHB1.0-5PLT-W1-P | FFC 1,0 mm 5P | **Pendiente de verificar** | — | SH1.0 5P wafer | 1 | Cable plano a Sub Board | Confirmado (ref. PCB) |
| `CN2` | Header I2C expansión | HC-1.25-4PLT | Pin header 1,25 mm 4P | **Pendiente de verificar** | — | Header 2,54 mm (adaptar PCB) | 1 | Expansión I2C | Confirmado (ref. PCB) |
| `CN4` | Header RGB | HC-1.25-3PLT | Pin header 1,25 mm 3P | **Pendiente de verificar** | — | — | 1 | Expansión WS2812B | Confirmado (ref. PCB) |
| `H1` | Header LD2402 | PZ254V-11-05P | Header 2,54 mm 5P | **Pendiente de verificar** | — | — | 1 | Interfaz radar LD2402 (opcional) | Confirmado (ref. PCB) |
| `BOOT` | Pulsador táctil | GT-TC072A-H060-L1 | THT/SMD 6×6 mm | G-Switch (ref. esquemático) | GT-TC072A-H060-L1 | Tact switch 6×6 mm activo bajo | 1 | Botón Boot → GPIO9 | Confirmado |
| `LED1` | LED indicador | — | **Pendiente de verificar** | — | — | LED 0603/0805 | 1 | Indicador visual | Pendiente de verificar |

### Diodos

| Designador | Componente | Valor | Encapsulado | Fabricante | MPN | Alternativas | Cant. | Función | Estado |
|------------|------------|-------|-------------|------------|-----|--------------|-------|---------|--------|
| `D1`–`D3` | Diodo protección USB | — | **Pendiente de verificar** | — | — | ESD USB (ej. USBLC6) si aplica | 3 | Protección / ruta USB | Pendiente de verificar |
| `D4`–`D5` | Diodo (circuito Boot) | — | **Pendiente de verificar** | — | — | — | 2 | Circuito botón Boot | Pendiente de verificar |
| `D6`–`D7` | Diodo (rama VBUS) | — | **Pendiente de verificar** | — | — | — | 2 | Protección / polaridad VBUS | Pendiente de verificar |

### Inductor

| Designador | Componente | Valor | Encapsulado | Fabricante | MPN | Alternativas | Cant. | Función | Estado |
|------------|------------|-------|-------------|------------|-----|--------------|-------|---------|--------|
| `L1` | Inductor power | 2,2 µH | **Pendiente de verificar** | — | — | Inductor 2,2 µH ≥ rated current DC-DC | 1 | Buck TLV62569 | Confirmado (valor) |

### Condensadores — Main Board

| Designador | Valor | Encapsulado (OSHWHUB) | MPN (OSHWHUB) | Cant. | Función | Estado |
|------------|-------|----------------------|---------------|-------|---------|--------|
| `C1`, `C3`, `C8` | 10 µF | C0603 | CL10A106K (Samsung) | 3 | Bulk / desacoplo 3,3 V | MPN parcial |
| `C2`, `C4`, `C5`, `C6`, `C10`, `C11`, `C12`, `C13`, `C14` | 100 nF | C0402 | CL05B104KB8NNNC (CL05B104K en export.) | 9 | Desacoplo por IC / ruta | MPN parcial |
| `C9` | 1 µF | C0402 | CL05A105KA5NQNC (CL05A105K en export.) | 1 | Desacoplo | MPN parcial |
| `C7` | 22 µF | **Pendiente de verificar** | — | 1 | Entrada/salida DC-DC / VBUS | Confirmado (valor) |
| `C15` | 10 nF | **Pendiente de verificar** | — | 1 | Filtro Hall SS49E | Confirmado (valor) |

### Resistencias — Main Board

| Designador | Valor | Encapsulado (OSHWHUB) | MPN (OSHWHUB) | Cant. | Función | Estado |
|------------|-------|----------------------|---------------|-------|---------|--------|
| `R1`, `R4` | 5,1 kΩ | **Pendiente de verificar** | — | 2 | Resistencias CC USB Type-C | Confirmado (valor) |
| `R2` | 100 kΩ | **Pendiente de verificar** | — | 1 | Retroalimentación DC-DC (FB) | Confirmado (valor) |
| `R3`, `R6` | 10 kΩ | R0402 | 0402WGF1002 (0402WGF1 truncado) | 2 | Circuito EN / GPIO9 | MPN parcial |
| `R5` | 22,1 kΩ | **Pendiente de verificar** | — | 1 | Retroalimentación DC-DC (FB) | Confirmado (valor) |
| `R7` | 1 kΩ | **Pendiente de verificar** | — | 1 | — | Confirmado (valor) |
| `R8`, `R9` | 4,7 kΩ | R0402 | 0402WGF4700 (0402WGF4 truncado) | 2 | Limitación corriente LED1 | MPN parcial |
| `R10`, `R11` | 10 kΩ | R0402 | 0402WGF1002 | 2 | Polarización Q1 (RGB) | MPN parcial |

### PCB — Main Board

| Designador | Componente | Valor | Cant. | Función | Estado |
|------------|------------|-------|-------|---------|--------|
| — | PCB | ESP-VoCat-Base-MainBoard-V1_0 | 1 | Placa principal | Confirmado; espesor **1,0 mm** (OSHWHUB) |

---

## Sub Board (`ESP-VoCat-Base-SubBoard-V1_0`)

| Designador | Componente | Valor | Encapsulado | Fabricante | MPN | Alternativas | Cant. | Función | Estado |
|------------|------------|-------|-------------|------------|-----|--------------|-------|---------|--------|
| `U1` | Conector magnético pogo | 4P 2,5 mm con oreja | — | **Pendiente de verificar** | — | Pogo pin 4P según OSHWHUB | 1 | Acoplamiento magnético ESP-VoCat | Confirmado (desc. OSHWHUB) |
| `CN1` | Conector Main Board | WAFER-SHB1.0-5PLT-W1-P | FFC 1,0 mm 5P | **Pendiente de verificar** | — | Igual que CN3 Main | 1 | Enlace a Main Board | Confirmado |
| `SW1` | Interruptor de límite | TM-8764-1 | — | **Pendiente de verificar** | TM-8764-1 | Micro switch similar (activo bajo) | 1 | Fin de carrera homing | Confirmado |
| `R1` | Resistencia | 51 kΩ | **Pendiente de verificar** | — | — | 1 | Red divisor fin de carrera | Confirmado (valor) |
| `R2` | Resistencia | 100 kΩ | **Pendiente de verificar** | — | — | 1 | Red divisor fin de carrera | Confirmado (valor) |
| — | PCB | ESP-VoCat-Base-SubBoard-V1_0 | 1 | Placa secundaria | Confirmado; espesor **1,0 mm** (OSHWHUB) |

---

## Componentes externos (no en PCB)

| Ref. | Componente | Especificación | Fabricante | MPN | Cant. | Función | Fuente |
|------|------------|----------------|------------|-----|-------|---------|--------|
| `M1` | Motor paso a paso | 24BYJ48 DC 5V | Múltiples | 24BYJ48 | 1 | Actuador rotación | OSHWHUB + esquemático |
| — | Cable motor | Incluido con 24BYJ48 | — | — | 1 | Motor → CN1 | Implícito |
| `J1` | Rodamiento | ID 7 mm, OD 11 mm, H 3 mm | Múltiples | **Pendiente de verificar** | 1 | Soporte plato giratorio | OSHWHUB |
| `FFC1` | Cable plano | SH 1,0 mm, 5P, 60 mm, misma dirección | — | — | 1 | Main ↔ Sub | OSHWHUB |
| `MAG1` | Imán | D10×1,5 mm | — | — | 2 | Acoplamiento en carcasa | OSHWHUB |
| `MAG2` | Imán | D6×5 mm | — | — | 1 | Deslizador magnético 3D | OSHWHUB |
| `LD1` | Radar (opcional) | LD2402 | Hi-Link / Espressif ref. | LD2402 | 1 | Detección presencia (no en firmware base) | OSHWHUB + esquemático |
| `LED_STRIP` | Tira LED (opcional) | WS2812B | Múltiples | WS2812B | 1 | RGB expansión (no en firmware base) | Esquemático |

---

## Tornillería (OSHWHUB)

| Especificación | Cant. | Uso |
|--------------|-------|-----|
| Tornillo M4×5 mm | 2 | Fijación motor |
| Tornillo M2×4 mm | 2 | Fijación Main Board a carcasa |
| Tornillo M2×3 mm | 2 | Cubierta superior plato giratorio |

---

## Resumen de cantidades por categoría

| Categoría | Ítems únicos (aprox.) | Notas |
|-----------|---------------------|-------|
| IC / módulo | 8–9 | Soldar U5 **o** U6, no ambos |
| Conectores | 7 + pogo | — |
| Pasivos SMD | ~25 | Ver tablas R/C/L |
| Diodos / LED | 8+ | Mayoría pendiente MPN |
| PCB | 2 | Pedir en JLCPCB/OSHWHUB |
| Mecánica / cable / imanes | 8+ | Ver lista de compra |

---

## Componentes Espressif vs reemplazables

Ver sección detallada en [lista-compra.md → Espressif vs equivalentes](lista-compra.md#espressif-vs-equivalentes-comerciales).

---

## Datos pendientes de verificar (resumen)

| Dato | Archivo donde debería aparecer |
|------|--------------------------------|
| MPN completos de todos los pasivos | BOM CSV en [OSHWHUB](https://oshwhub.com/esp-college/esp-echoear-base) |
| MPN diodos D1–D7 | Esquemático interactivo EasyEDA (no en PDF extraído) |
| Tipo exacto LED1 (color, corriente) | Esquemático / BOM OSHWHUB |
| MPN inductor L1 | BOM OSHWHUB |
| MPN conectores USB1, CN1–CN4, H1 | BOM OSHWHUB |
| MPN pogo pin U1 Sub Board | BOM OSHWHUB |
| MPN rodamiento | OSHWHUB lista de compra |
| Resistencias pull-up I2C (si existen) | Netlist EasyEDA |

---

> **Auditoría:** ver [auditoria-hardware.md](auditoria-hardware.md) para MPN pendientes, contradicciones y checklist.

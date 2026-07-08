# Guía de ensamblaje — ESP-VoCat Base V1.0

> Orden recomendado para montar una réplica funcional.  
> Referencias: [BOM](BOM.md) · [Lista de compra](lista-compra.md) · [Hardware](hardware.md) · pasos 1–10 en `docs/7726, 2155.txt` (OSHWHUB).

---

## Herramientas recomendadas

| Herramienta | Uso |
|-------------|-----|
| Estación de soldadura / hot air | SMD en Main y Sub Board |
| Multímetro | Comprobar 3,3 V y continuidad |
| Destornilladores M2 / M4 | Mecánica |
| Cable USB-C | Alimentación y flasheo |
| Impresora 3D FDM | Carcasa (archivos STEP en `3D_models/`) |
| Pinzas, cinta kapton | Cable FFC e imanes |

---

## Impresión 3D

Los archivos STEP **no contienen** material, orientación, soportes, altura de capa ni relleno. Los parámetros siguientes deben tomarse de OSHWHUB o determinarse por prueba.

### Correspondencia piezas OSHWHUB ↔ archivos del repositorio

| # OSHWHUB | Pieza (OSHWHUB) | Archivo en `3D_models/` |
|-----------|-----------------|-------------------------|
| 1 | Carcasa exterior | `ESP-VoCat_catbase_20251128.stp` |
| 2 | Cubierta inferior carcasa | `ESP-VoCat_catbase_platform_btm_20251128.stp` |
| 3 | Cubierta plato giratorio | `ESP-VoCat catbase cover 2025-11-22.STEP` |
| 4 | Tapa inferior plato | `ESP-VoCat catbase platform top 2025-11-22.STEP` |
| 8 | Interruptor deslizante magnético | `ESP-VoCat catbase ball only 2025-11-22.STEP` |

| Archivo (`3D_models/`) | Pieza | Material recomendado | Orientación | Soportes | Altura capa | Relleno | Estado |
|------------------------|-------|---------------------|-------------|----------|-------------|---------|--------|
| `ESP-VoCat_catbase_20251128.stp` | Base / carcasa principal | **Pendiente de verificar** — típ. PLA/PETG | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | Sin datos en STEP |
| `ESP-VoCat_catbase_platform_btm_20251128.stp` | Plataforma inferior plato | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | Sin datos en STEP |
| `ESP-VoCat catbase platform top 2025-11-22.STEP` | Plataforma superior plato | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | Sin datos en STEP |
| `ESP-VoCat catbase cover 2025-11-22.STEP` | Cubierta | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | Sin datos en STEP |
| `ESP-VoCat catbase ball only 2025-11-22.STEP` | Bola / inserto mecánico | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | **Pendiente de verificar** | Sin datos en STEP |

**Sugerencia provisional (no oficial):** PLA o PETG, capa 0,2 mm, relleno 20–30 % en piezas estructurales; orientar de modo que las superficies de asiento del PCB queden planas (verificar en slicer). Confirmar en [OSHWHUB](https://oshwhub.com/esp-college/esp-echoear-base).

**Imanes en piezas 3D:** insertar imán D10×1,5 mm (×2) y D6×5 mm (×1) según alojamientos del modelo; fijar con adhesivo si el ajuste es holgado.

---

## Fase 1 — Electrónica

### 1.1 Main Board (SMT)

Seguir orden típico SMT (de menor a mayor altura):

1. Soldar pasivos 0402/0603: resistencias y condensadores según [BOM](BOM.md).
2. Soldar `U2` (TLV62569), `U3` (TPS2051B), `Q1` (AO3400A).
3. Soldar **solo uno**: `U5` (BMM150) **o** `U6` (QMC6309) — no ambos.
4. Soldar `U7` (SS49E), `U4` (ULN2003A).
5. Soldar `USB1`, conectores `CN1`, `CN3`, `CN2`, `CN4`, `H1`.
6. Soldar `BOOT`, `LED1`, diodos `D1`–`D7`, inductor `L1`.
7. Soldar `U1` (ESP32-C61-WROOM-1) al final (mayor altura / sensible a calor).

**Comprobaciones antes de energizar:**

- Sin cortocircuitos entre `VBUS` y `GND`.
- `VCC_3V3` estable (~3,3 V) con USB conectado.
- Resistencias CC `R1`/`R4` (5,1 kΩ) presentes en USB-C.

### 1.2 Sub Board

1. Soldar `R1` (51 kΩ), `R2` (100 kΩ).
2. Soldar `SW1` (TM-8764-1) con orientación que permita accionamiento mecánico del fin de carrera.
3. Soldar `U1` (pogo pin 4P) y `CN1` (wafer SH1.0 5P).
4. **Orientación pogo pin (OSHWHUB):** el extremo marcado en rojo debe quedar en el **mismo lado** que el círculo blanco impreso en la PCB Sub Board.
5. **No** conectar aún el cable FFC a la Main Board.

> **Nota WLCSP:** los magnetómetros BMM150/QMC6309 usan encapsulado WLCSP, difícil de soldar a mano. OSHWHUB recomienda servicio SMT para usuarios sin experiencia.

### 1.3 Ensamblaje eléctrico Main ↔ Sub

1. Crimpolar / insertar cable FFC **SH1.0 5P 60 mm** en `CN3` (Main) y `CN1` (Sub).
2. Verificar pinout: `GND`, `VBUS`, `TX`, `RX`, `ANGLE_LIMIT_SW` (ver [hardware.md](hardware.md)).

---

## Fase 2 — Motor

1. Atornillar motor **24BYJ48** a la base impresa con **2× M4×5 mm** (alojamientos en carcasa).
2. Conectar cable del motor a `CN1` (1,25 mm 5P) respetando orden de fases `IN1`–`IN4` del esquemático.
3. Comprobar que el eje gira libremente antes de montar el plato superior.

---

## Fase 3 — Final de carrera

1. Fijar Sub Board en su alojamiento mecánico (posición según modelo 3D).
2. Ajustar `SW1` para que se active cuando el plato alcanza el límite de giro (homing).
3. Con firmware cargado, comprobar que `ANGLE_LIMIT_SW` (**GPIO1**) lee **activo bajo** al pulsar el switch (ver [tablas-referencia.md](tablas-referencia.md)).

---

## Fase 4 — Sensor magnético

### Hall lineal (SS49E)

1. `U7` ya está en Main Board; posicionar imán D6×5 mm en pieza deslizadora 3D según diseño.
2. Verificar señal analógica en GPIO5 con multímetro o monitor serie (`ss49e` profile).

### Magnetómetro (BMM150 o QMC6309)

1. Confirmar que el firmware usa el perfil correcto (`bmm150` o `qmc6309`).
2. Instalar imanes D10×1,5 mm en carcasa y en dispositivo acoplado (ESP-VoCat) para acoplamiento magnético vía pogo pin.
3. Alinear Sub Board / pogo con la zona magnética del host.

---

## Fase 5 — Carcasa

Orden de montaje según OSHWHUB (pasos 1–10, `docs/7726, 2155.txt`), alineado con las fases anteriores:

| Paso | Acción |
|------|--------|
| 1 | Insertar **2× imán D10×1,5 mm** en la carcasa exterior; **respetar polaridad** |
| 2 | Montar rodamiento **7×11×3 mm** en la ranura de la carcasa |
| 3 | Instalar motor **24BYJ48** con **2× M4×5 mm** — **no apretar al máximo** aún |
| 4 | Fijar **Sub Board** en la cubierta inferior del plato (`platform_btm`) |
| 5 | Montar cubierta superior del plato (`cover`) con **2× M2×3 mm** en la parte posterior |
| 6 | Insertar cable FFC **SH1.0 5P** en el conector del plato (Sub Board) |
| 7 | Acoplar plato ensamblado al eje del motor; superficie al ras con carcasa; **apretar tornillos M4** |
| 8 | Fijar **Main Board** a la carcasa con **2× M2×4 mm** |
| 9 | Conectar cable motor a `CN1` (ángulo recto, silk **Motor**) y FFC Sub→Main (conector recto en Main). **Ambos extremos del FFC en la misma dirección** — verificar antes de insertar |
| 10 | Insertar imán **D6×5 mm** en pieza deslizadora 3D (`ball only`); polaridad debe **atraer** a imanes D10×1,5 mm. Colocar sobre la base |

**Pedido PCB:** espesor **1,0 mm** (OSHWHUB).

---

## Fase 6 — Calibración inicial

### 6.1 Flasheo firmware

1. Conectar USB-C a `USB1`.
2. Flashear el proyecto adecuado desde `software/` (ver [arranque-firmware.md](arranque-firmware.md)).
3. Configurar `MAG_SW_PROFILE` según sensor soldado (`bmm150`, `qmc6309` o `ss49e`).

### 6.2 Homing y límite angular

1. Ejecutar secuencia de homing del firmware demo.
2. Verificar que el motor detiene al activar `SW1`.
3. Si el giro es incorrecto, revisar cableado motor y sentido de fases.

### 6.3 Calibración magnética

| Perfil | Acción |
|--------|--------|
| `bmm150` / `qmc6309` | Verificar lecturas I2C y detección de acoplamiento magnético con host |
| `ss49e` | Ajustar posición del imán D6×5 mm; revisar umbrales ADC en firmware si es necesario |

### 6.4 UART con host ESP-VoCat

1. Conectar host a través del acoplamiento pogo / magnético.
2. Probar trama UART (115200 baud) según [arquitectura.md](arquitectura.md).
3. Confirmar eventos de rotación y estado del fin de carrera.

### 6.5 Lista de verificación final

- [ ] 3,3 V y 5 V dentro de especificación
- [ ] Motor gira en ambos sentidos
- [ ] Fin de carrera responde (GPIO1)
- [ ] Sensor magnético coherente con perfil elegido
- [ ] UART operativa con host
- [ ] Calibración automática al centro tras encender (OSHWHUB paso 10)
- [ ] Sin calentamiento anormal en `U3` / `U4` tras 10 min de uso

---

## Solución de problemas de montaje

| Síntoma | Comprobar |
|---------|-----------|
| No arranca | USB-C, `EN`, soldadura `U1`, corto VBUS |
| Motor no gira | `CN1`, `U4`, alimentación VBUS al motor |
| Homing falla | `SW1`, cable FFC, GPIO1, orientación switch |
| I2C magnetómetro NACK | Solo un de U5/U6 soldado, dirección I2C, perfil firmware |
| Hall errático | Imán D6×5, posición mecánica, `C15` |

Más detalle: [troubleshooting.md](troubleshooting.md).

---

*Parámetros 3D marcados como «Pendiente de verificar» deben confirmarse en OSHWHUB antes de una producción en serie.*

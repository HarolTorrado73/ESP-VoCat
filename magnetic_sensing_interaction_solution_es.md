# Introducción a la solución de interacción por sensado magnético

[Español](./magnetic_sensing_interaction_solution_es.md) | [English](./magnetic_sensing_interaction_solution_en.md)

> Documentación ampliada: [Guía central](README_ES.md) · [Arquitectura de perfiles](docs/es/perfiles.md) · [Tablas de eventos UART](docs/es/tablas-referencia.md#eventos-magnéticos-por-perfil)

## 1. Descripción general

La base ESP-VoCat utiliza un interruptor deslizante magnético para ofrecer un control de interacción enriquecido. Las distintas posiciones del deslizador modifican el campo magnético local; el firmware muestrea continuamente los datos del sensor para detectar las acciones del deslizador. Los eventos detectados se reportan a ESP-VoCat mediante UART.

## 2. Tipos de eventos por proyecto de demostración

### 2.1 Demostración de eventos del deslizador tipo campana
Proyecto: [`software/esp_vocat_rotating_base_bell_event_detection`](./software/esp_vocat_rotating_base_bell_event_detection/)

Eventos soportados:

- `SLIDE_DOWN`: El deslizador se mueve de la posición superior a la inferior.
- `SLIDE_UP`: El deslizador se mueve de la posición inferior a la superior.
- `REMOVE_FROM_UP`: El deslizador se retira de la posición superior.
- `REMOVE_FROM_DOWN`: El deslizador se retira de la posición inferior.
- `PLACE_FROM_UP`: El deslizador se coloca en la posición superior.
- `PLACE_FROM_DOWN`: El deslizador se coloca en la posición inferior.
- `SINGLE_CLICK`: Se detecta una acción de clic simple cuando el deslizador permanece en la posición inferior.

### 2.2 Demostración de detección de iPhone
Proyecto: [`software/esp_vocat_rotating_base_iphone_detection`](./software/esp_vocat_rotating_base_iphone_detection/)

Eventos soportados:

- `IPHONE_LEAN_FRONT`: El iPhone se apoya contra el frente de la base.
- `IPHONE_LEAN_FRONT_DETACHED`: El iPhone se separa del frente de la base.
- `IPHONE_UNDER_BASE`: El iPhone se coloca debajo de la base y entra en estado de detección válido.
- `IPHONE_UNDER_BASE_DETACHED`: El iPhone se retira de debajo de la base.

### 2.3 Demostración de detección de accesorios magnéticos
Proyecto: [`software/esp_vocat_rotating_base_magnetic_accessory_detection`](./software/esp_vocat_rotating_base_magnetic_accessory_detection/)

Eventos soportados:

- `FISH_ATTACHED`: Se detecta el accesorio de pez adherido.
- `FISH_DETACHED`: El accesorio de pez se retira de la base.
- `PAIRING`: Se detecta la condición de emparejamiento y se entra en modo de emparejamiento.
- `PAIRING_CANCELLED`: La condición de emparejamiento desaparece y se sale del modo de emparejamiento.
- `ICE_CREAM_ATTACHED`: Se detecta el accesorio de helado adherido.
- `ICE_CREAM_DETACHED`: El accesorio de helado se retira de la base.
- `DONUT_ATTACHED`: Se detecta el accesorio de dona adherido.
- `DONUT_DETACHED`: El accesorio de dona se retira de la base.

> **Nota:** Los conjuntos de eventos están definidos por el perfil `magnetic_slide_switch` seleccionado en cada demostración. La definición del enum en el código fuente es la referencia final.

## 3. Sensores compatibles

Se puede utilizar uno de los siguientes sensores:

- Magnetómetro de 3 ejes BMM150 (predeterminado)
- Magnetómetro de 3 ejes QMC6309
- Sensor Hall lineal

## 4. Notas de uso

1. Cada proyecto de demostración expone un conjunto de eventos diferente. Cambie de proyecto para cambiar el comportamiento de detección.
2. Antes del primer uso, ejecute la calibración automática completa para capturar los valores de referencia de los estados superior, inferior y retirado.
3. Los datos de calibración se almacenan de forma persistente en NVS y sobreviven a los ciclos de encendido.
4. La recalibración puede activarse mediante comando UART o manteniendo pulsado el botón Boot de la base.

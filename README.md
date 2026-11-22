# Simulador de Smart Antennas — MIMO Masivo 360°
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3D-green)

## Descripción
Este repositorio contiene el código fuente de un simulador interactivo de Antenas Inteligentes (Smart Antennas) aplicado a sistemas MIMO Masivo. Desarrollado en Python con Tkinter y Matplotlib, el simulador modela un arreglo planar uniforme (UPA) de 8×8 (64 elementos) que realiza un barrido espacial de 360° para detectar y asignar haces de radiación a 6 usuarios distribuidos en el plano.
El objetivo principal es demostrar visualmente cómo la frecuencia portadora afecta la viabilidad del Acceso Múltiple por División Espacial (SDMA). El simulador permite comparar dos escenarios:
- 28 GHz (mmWave): Haces estrechos y bien separados, ideales para SDMA.
- 3.5 GHz (sub-6 GHz): Haces anchos y traslapados, que dificultan el SDMA con el mismo arreglo físico.

## Características principales
- Interfaz gráfica oscura y moderna con Tkinter.
- Panel de control editable para 6 usuarios: Azimut (0°–360°), Elevación (0°–90°) y Potencia (W).
- Selector de frecuencia (28 GHz por defecto, configurable).
- Motor de barrido de 360° con animación en tiempo real.
- Detección automática de usuarios cuando el haz de escaneo pasa a ±2° del azimut del usuario.
- Visualización polar con anillos de amplitud normalizada y colores distintivos por usuario.
- Cálculo dinámico de la longitud de onda (λ) y del ancho de haz (HPBW) en función de la frecuencia.

## Requisitos del sistema
- Python 3.x (probado en Python 3.10+).
- NumPy: Para cálculos vectoriales.
- Matplotlib: Para la renderización de la gráfica polar y la animación.
- Tkinter: Incluido por defecto en la instalación estándar de Python.

Instalación de dependencias:
```bash
pip install numpy matplotlib

Cómo ejecutar el simulador
Clona este repositorio:

bash
git clone https://github.com/222-mph/Simulador-Smart-Antennas.git
Navega a la carpeta del proyecto:

bash
cd Simulador-Smart-Antennas
Ejecuta el script:

bash
python simulador_MIMO.py
Ajusta los parámetros de los usuarios y la frecuencia, y presiona "INICIAR BARRIDO 360°".


Experimentos incluidos
Experimento 1: 28 GHz (SDMA viable)
Frecuencia: 28 GHz.
Longitud de onda: λ ≈ 10.71 mm.
Resultado: Los 6 haces se mantienen separados, permitiendo la multiplexación espacial de los usuarios.
Experimento 2: 3.5 GHz (SDMA inviable)
Frecuencia: 3.5 GHz.
Longitud de onda: λ ≈ 85.71 mm.
Resultado: El ancho de haz se incrementa ~8 veces, provocando traslape espacial severo entre usuarios adyacentes.

Marco teórico resumido
Beamforming: Ajuste dinámico de fase y amplitud en cada elemento del arreglo para dirigir el haz.
UPA 8×8: 64 elementos separados a λ/2, con control de haz en azimut y elevación.
HPBW vs Frecuencia: El ancho de haz es inversamente proporcional a la frecuencia para un arreglo de tamaño físico fijo: HPBW ∝ 1/f.
SDMA: Técnica de multiplexación espacial que permite atender múltiples usuarios en la misma frecuencia y tiempo.

Video demostrativo
Puedes ver una demostración del simulador en funcionamiento en el siguiente enlace:
https://youtu.be/5rYF83m2lqs

Licencia y uso académico
Este proyecto fue desarrollado con fines exclusivamente académicos para la asignatura de Comunicaciones Móviles. El código es de libre consulta y uso educativo. Si lo utilizas como base para otros proyectos, se agradece una mención o referencia.

Autor
Gerardo Hernández — Desarrollo del simulador y documentación

Facultad de Ingeniería Mecánica y Eléctrica, incorporada a la Universidad Autónoma de Nuevo León.

9no semestre, Ingeniería en Electrónica y Comunicaciones.

Este proyecto fue desarrollado como una herramienta de apoyo didáctico para comprender los límites físicos del MIMO Masivo y el SDMA en redes 5G/6G.

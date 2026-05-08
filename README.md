📊 KODE: Narrative Data Intelligence
Kode es un motor de análisis de datos textuales diseñado para desglosar narrativas (reales o ficticias) y transformarlas en métricas visuales. El proyecto demuestra la capacidad de integrar una interfaz de usuario personalizada con el procesamiento de bases de datos para extraer insights en tiempo real.

🎯 Propósito del Proyecto
A diferencia de un sitio web estático, Kode funciona como una herramienta de inteligencia narrativa que:

Cuantifica la Información: Escanea relatos para identificar patrones de repetición y frecuencia de palabras.

Visualización Dinámica: Genera gráficas basadas en el contenido actual de la base de datos de historias.

Interfaz Narrativa: Utiliza narradores digitales para presentar los datos de forma inmersiva, apoyándose en tecnologías de Text-to-Speech.

🛠️ Arquitectura Técnica
El sistema está construido bajo un enfoque de Full-Stack Development:

Gestión de Datos: Scripts en Python encargados de la limpieza de texto y la lógica de estadísticas.

Panel de Administración: Una interfaz en Tkinter que permite la edición manual de archivos y la gestión de la base de datos de historias.

Visual Layer: Frontend desarrollado con HTML5 y CSS3 utilizando Flexbox para una estructura limpia y alineada.

Assets: Diseño de UI/UX gótico y minimalista creado con Inkscape y GIMP.

📈 Visualización de Datos
El dashboard de Kode traduce el texto plano en información accionable:

Análisis de Repeticiones: Gráficas de las palabras más frecuentes para entender el tono del relato.

Modificación en Tiempo Real: Capacidad de alterar la historia "base" y observar cómo cambian las estadísticas instantáneamente.


🛡️ Capa de Curación Ética y Privacidad

A diferencia de otros analizadores, Kode implementa una "aduana de datos" mediante una interfaz de administración en Tkinter. Este módulo permite:

Anonimización Dinámica: Sustitución manual de PII (Personally Identifiable Information) antes de la persistencia.

Mitigación de Errores de Procesamiento: Corrección de fallos en el escaneo automático (ej. nombres en minúsculas) para garantizar que la base de datos visual solo contenga información sanitizada.


💡 Próximos Pasos
Migrar el procesamiento de datos a una base de datos SQL para mayor escalabilidad.

Implementar visualizaciones más complejas (gráficas de calor o nubes de palabras dinámicas).


⚖️ Licencia
Este proyecto está protegido bajo la licencia GNU General Public License v3.0.

Puedes usar y modificar el código siempre que se mantenga el reconocimiento del autor original y cualquier derivado se mantenga como código abierto.

Los activos visuales fueron generados con asistencia de IA para fines de prototipado y diseño conceptual.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge)
![Inkscape](https://img.shields.io/badge/Inkscape-e0e0e0?style=for-the-badge&logo=inkscape&logoColor=black)
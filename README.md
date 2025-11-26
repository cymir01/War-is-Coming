## Estructura
(estrucutra MVC https://es.wikipedia.org/wiki/Modelo%E2%80%93vista%E2%80%93controlador)

War-is-Coming/
│
├── main.py                    # 🎯 Punto de entrada principal
├── requirements.txt           # 📦 Dependencias
├── README.md                  # 📖 Documentación
├── .gitignore                 # 🔒 Archivos a ignorar en Git
│
├── data/                      # 💾 Datos y persistencia
│   ├── __init__.py
│   ├── recursos.json          # 📋 Recursos predefinidos
│   └── eventos.json           # 🗓️ Eventos guardados
│
├── models/                    # 🏗️ Modelos de datos (Clases)
│   ├── __init__.py
│   ├── evento.py              # 📅 Clase Evento
│   ├── recurso.py             # ⚔️ Clase Recurso
│   └── restriccion.py         # 🔗 Clase Restriccion
│
├── services/                  # 🧠 Lógica de negocio
│   ├── __init__.py
│   ├── planificador.py        # ⚙️ Motor de planificación
│   ├── validador.py           # ✅ Validación de restricciones
│   └── gestor_datos.py        # 💾 Guardar/cargar datos
│
└── ui/                        # 🖥️ Interfaz de usuario
    ├── __init__.py
    ├── consola.py             # ⌨️ Menús y entrada de datos
    └── calendario.py          # 🗓️ Visualización de calendarios


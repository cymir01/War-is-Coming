<a id="top"></a>

<div align="center">
  <img src="https://img.icons8.com/color/96/sword.png" alt="Espada">
  <img src="https://img.icons8.com/color/96/dragon.png" alt="Dragón">
  <img src="https://img.icons8.com/color/96/castle.png" alt="Castillo">
  <h1>War is Coming</h1>
  <p><em>Planificador Inteligente de Eventos Bélicos – Universo de A Song of Ice and Fire</em></p>
</div>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/forged%20in-fire-E760A4.svg" alt="Forjado en fuego">
  </a>
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="Licencia">
  </a>
  <a href="https://www.python.org/downloads/" target="_blank">
    <img src="https://img.shields.io/badge/python-3.12%2B-blue.svg" alt="Python 3.12+">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/status-complete-brightgreen.svg" alt="Estado">
  </a>
</p>

---

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Cómo Empezar](#-cómo-empezar)
- [Instrucciones de Uso](#-instrucciones-de-uso)
- [Restricciones del Dominio](#-restricciones-del-dominio)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Mejoras Futuras](#-mejoras-futuras)
- [Licencia](#-licencia)

---

## 📃 Acerca del Proyecto

**War is Coming** es un sistema inteligente de planificación de eventos militares inspirado en el universo de *A Song of Ice and Fire*. La aplicación permite al usuario organizar campañas bélicas (asedios, batallas navales, asaltos, defensas, emboscadas, misiones diplomáticas y batallas campales) asignando recursos limitados (tropas de distintas casas, maquinaria de asedio, elementos especiales como Fuego Valyrio, personajes clave y recursos económicos) respetando estrictas reglas de co‑requisito, exclusión mutua y conflictos temporales.

El sistema garantiza que:
- Ningún recurso se asigne a dos eventos simultáneamente.
- Las combinaciones de recursos cumplan la lógica del universo (casas enemigas no pueden compartir evento).
- Cada tipo de evento exija o prohíba ciertos recursos específicos.
- Los eventos se planifiquen respetando todas las restricciones definidas.

El proyecto ha sido desarrollado aplicando principios de modularidad, buenas prácticas de Python y una interfaz de consola enriquecida con la librería `rich`. La arquitectura en capas (modelos, servicios, interfaz) facilita el mantenimiento y la extensión del sistema.

---

## ✨ Características

### Funcionalidades Principales

- **Planificación Inteligente**: validación automática de disponibilidad de recursos, conflictos horarios y cumplimiento de restricciones personalizadas. El sistema verifica que ningún recurso esté ocupado en el mismo intervalo de tiempo y que se cumplan todas las reglas del dominio antes de guardar un evento.

- **Búsqueda Automática de Huecos**: encuentra el siguiente intervalo libre para agendar un evento sin colisiones ni violaciones de reglas. El algoritmo analiza el calendario existente, respeta conflictos de recursos y verifica todas las restricciones del dominio. La búsqueda es granular (prueba hora por hora) y solo avanza cuando los eventos usan los recursos solicitados, optimizando la sugerencia de horarios.

- **Inventario de Recursos**: unidades militares con atributos (casa, tipo) que definen su comportamiento en las restricciones. Los recursos pueden ser tropas, personajes nobles, maquinaria de asedio, elementos especiales o recursos económicos. Cada recurso tiene un tipo que determina cómo interactúa con las reglas del sistema.

- **Gestión Completa de Eventos**: añadir, listar, ver detalles y eliminar eventos. La interfaz permite visualizar toda la información de cada evento, incluyendo su duración, recursos asignados y estado actual.

- **Persistencia Automática**: todo el estado se guarda y carga desde un único archivo JSON. El sistema mantiene la consistencia de los datos entre ejecuciones y maneja errores de archivo de forma robusta.

- **Interfaz de Usuario Enriquecida**: menú interactivo con comandos claros, tablas formateadas con colores, mensajes semánticos (verde para éxito, rojo para errores, amarillo para advertencias) y paneles visuales que mejoran la legibilidad y la experiencia de usuario.

### Restricciones Implementadas

| Tipo de Restricción | Descripción | Ejemplo |
|---------------------|-------------|---------|
| **Co‑requisito (Inclusión)** | Un recurso requiere otro complementario | Maquinaria de asedio → Ingeniero de asedio |
| **Exclusión Mutua** | Recursos incompatibles en un mismo evento | Fuego Valyrio + Maquinaria de asedio |
| **Por Tipo de Evento (Inclusión)** | Cada evento exige recursos específicos | Asedio requiere Maquinaria de asedio |
| **Por Tipo de Evento (Exclusión)** | Cada evento prohíbe ciertos recursos | Batalla Naval prohíbe caballería |
| **Exclusión entre Casas** | Casas enemigas no pueden aliarse | Lannister + Stark |

### Interfaz de Usuario

- Menú interactivo con comandos claros (`a`, `l`, `v`, `d`, `s`).
- Tablas enriquecidas para listar eventos y detalles.
- Colores para mensajes de éxito (verde) y error (rojo).
- Asistentes paso a paso con validación de entrada.
- Paneles y separadores visuales para mejorar la legibilidad.
- Visualización de restricciones antes de seleccionar recursos.
- Panel de bienvenida con título estilizado usando `rich.panel.Panel`.

---

## 🏰 Arquitectura

El código se organiza en capas modulares siguiendo principios de separación de responsabilidades:

```
war-is-coming/
├── src/
│   ├── models/           # Capa de Modelos
│   │   ├── event.py      # Entidad Evento
│   │   └── resource.py   # Entidad Recurso
│   ├── services/         # Capa de Servicios (Lógica de Negocio)
│   │   ├── data_manager.py  # Persistencia y operaciones CRUD
│   │   └── planner.py       # Validación de restricciones y búsqueda de huecos
│   ├── interface/        # Capa de Interfaz de Usuario
│   │   ├── main_menu.py      # Menú principal
│   │   ├── command_add_event.py
│   │   ├── command_list_events.py
│   │   ├── command_view_details.py
│   │   └── command_delete_event.py
│   └── data/             # Datos por defecto
│       └── default_data.json
├── data/                 # Datos de trabajo
│   └── war_planner.json  # (se genera automáticamente)
├── main.py               # Punto de entrada
├── README.md
├── requirements.txt
└── pyproject.toml
```

### Flujo de Datos

1. **Inicialización**: `data_manager.load_data()` carga el estado desde `war_planner.json` o crea uno nuevo desde `default_data.json`. En caso de error, se llama a `load_default_data()` que crea estructuras vacías y guarda un archivo por defecto.

2. **Menú Principal**: `main_menu.py` muestra las opciones y redirige al comando correspondiente. Utiliza `rich.panel.Panel` para mostrar el título estilizado.

3. **Operaciones**:
   - **Agregar**: `command_add_event.py` → `data_manager.add_event()` → `planner.validate_restrictions()` + `planner.resources_conflict_check()` → guardado. Antes de pedir recursos, se muestran las restricciones de inclusión y exclusión por tipo de evento.
   - **Listar**: `command_list_events.py` → `data_manager.list_events()` → tabla formateada con colores.
   - **Ver**: `command_view_details.py` → `data_manager.get_event_by_id()` / `get_event_by_resource()` → tabla de dos columnas.
   - **Eliminar**: `command_delete_event.py` → `data_manager.delete_event()` → guardado.

4. **Búsqueda de Huecos**: `command_add_event.py` → `planner.find_next_available_time_slot()`. El algoritmo es granular y maneja correctamente todos los casos.

### Detalles de Implementación

- **Persistencia**: El estado se guarda automáticamente en `data/war_planner.json` después de cada operación que modifica los datos (añadir o eliminar eventos). La función `save_data()` utiliza `default=str` para manejar correctamente la serialización de objetos `datetime`.

- **Ordenamiento**: La lista de eventos se mantiene ordenada cronológicamente usando `bisect.insort`, lo que optimiza la búsqueda de huecos y la detección de conflictos. La clase `Event` implementa el método `__lt__` para permitir la comparación por fecha de inicio.

- **Validación en Capas**: Las restricciones se validan en múltiples niveles (interfaz, servicios y modelos) para garantizar la integridad de los datos. La validación de recursos incluye verificación de existencia, conflictos temporales y cumplimiento de todas las reglas del dominio.

- **Consistencia en Tipos de Recurso**: Los métodos `robject_to_dict` y `create_robject_from_dict` en `resource.py` utilizan consistentemente la clave `"resource_type"` para el tipo del recurso, garantizando una correcta serialización y deserialización.

---

## ⚒️ Tecnologías

- **Python 3.12+**: lenguaje principal.
- **Rich**: librería para interfaces de consola avanzadas (tablas, colores, paneles, prompts). Se utiliza `Panel` para títulos, `Table` para datos estructurados, y `Prompt.ask` y `Confirm.ask` para entrada interactiva.
- **Datetime**: gestión de fechas, duraciones y comparaciones temporales. Se usa `datetime.fromisoformat` para cargar desde JSON y `datetime.isoformat` para guardar.
- **Bisect**: mantenimiento de la lista de eventos ordenada cronológicamente.
- **JSON**: persistencia de datos en archivo con manejo de errores robusto.

---

## 🚀 Cómo Empezar

### Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes)

### Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/war-is-coming.git
   cd war-is-coming
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python main.py
   ```

5. **Sigue las instrucciones en consola.**

### Archivo de Datos

- **Datos por defecto**: `src/data/default_data.json` (recursos y restricciones predefinidos). Contiene todas las casas, sus unidades y las reglas del dominio.
- **Datos de trabajo**: `data/war_planner.json` (se genera automáticamente al primer inicio). Este archivo guarda el estado actual de la planificación.
- Puedes modificar `default_data.json` para personalizar el dominio inicial o restaurar la configuración por defecto eliminando `war_planner.json`.

---

## 📖 Instrucciones de Uso

Al iniciar, verás un panel de bienvenida y un menú con los siguientes comandos:

### Menú Principal

```
¡War is Coming!
¿Cuál es su nombre, milord? [tu nombre]

A continuación los comandos para realizar acciones en el planificador:
  a - agregar evento
  l - listar eventos
  d - eliminar evento
  v - ver detalles de un evento o recurso
  s - salir
```

### Comandos Detallados

#### `a` - Agregar Evento

Asistente paso a paso que te guía en la creación de un nuevo evento:

1. **Nombre** del evento.
2. **Descripción** (opcional).
3. **Tipo de evento** (seleccionar de lista: Asedio, Batalla naval, Asalto, Defensa, Emboscada, Batalla campal, Misión diplomática).
4. **Era histórica** (DC: Después de la Conquista / AC: Antes de la Conquista).
5. **Ubicación** (opcional).
6. **Visualización de restricciones**: se muestran las restricciones de inclusión y exclusión por tipo de evento para que el usuario sepa qué recursos necesita y cuáles no puede combinar.
7. **Selección de recursos**:
   - Se muestra la lista completa de recursos con IDs, tipos y casas.
   - Introduce los IDs separados por comas.
   - El sistema valida que todos existan y elimina duplicados automáticamente.
8. **Fechas**:
   - Se piden año, mes, día, hora y minuto por separado para inicio y fin.
   - Validación automática de que fin > inicio.
   - Manejo robusto de errores con `try-except`.
9. **Búsqueda de hueco** (opcional):
   - Si lo solicitas, el sistema analiza el calendario y sugiere el próximo intervalo disponible.
   - El algoritmo verifica tanto conflictos de recursos como todas las restricciones del dominio.
   - La búsqueda es granular (prueba hora por hora) y solo avanza cuando los eventos usan los recursos solicitados.
   - Puedes aceptar el hueco sugerido o rechazarlo.
10. **Validación y guardado**:
    - El sistema verifica conflictos de recursos y restricciones.
    - Si todo es correcto, el evento se guarda con un ID único.
    - Se muestra mensaje de éxito en verde o error en rojo.

**Ejemplo de uso - Defensa de Invernalia:**
```
Nombre del evento: Defensa de Invernalia
¿Desea agregar descripción? Sí
Descripción: Defender las murallas contra los caminantes blancos
Tipo de evento: Defensa
Era: DC
Ubicación: Invernalia

Restricciones de inclusión de recursos por tipo de evento:
- Asedio requiere Maquinaria de asedio, Ingeniero de asedio, Arqueros e Infantería pesada
- Batalla naval requiere Almirante, Flota y Fuego valyrio
- Batalla campal requiere Infantería pesada, Caballería pesada y Arqueros
- Asalto requiere Infantería pesada y Caballería pesada
- Defensa requiere Infantería pesada y Arqueros
- Emboscada requiere Infantería ligera y Arqueros
- Misión diplomática requiere Embajador

Recursos disponibles:
1: Infantería pesada Arryn (tipo: Infantería pesada, casa: Arryn)
2: Infantería ligera Arryn (tipo: Infantería ligera, casa: Arryn)
...
89: Infantería pesada Stark (tipo: Infantería pesada, casa: Stark)
90: Infantería ligera Stark (tipo: Infantería ligera, casa: Stark)
93: Arqueros Stark (tipo: Arqueros, casa: Stark)
101: Eddard Stark (tipo: Noble, casa: Stark)
...

Ingrese los IDs de los recursos que desea agregar (separados por comas): 89,93,101

Año - Inicio: 302
Mes - Inicio [1-12]: 1
Día - Inicio [1-31]: 15
Hora - Inicio [0-23]: 8
Minuto - Inicio [0-59]: 0
Año - Fin: 302
Mes - Fin [1-12]: 1
Día - Fin [1-31]: 15
Hora - Fin [0-23]: 20
Minuto - Fin [0-59]: 0

¿Desea buscar el próximo hueco disponible para estos recursos? No
✅ Evento 'Defensa de Invernalia' agregado con ID: 1
```

**Ejemplo de uso - Asedio a Harrenhal (con búsqueda de hueco):**
```
Nombre del evento: Asedio a Harrenhal
¿Desea agregar descripción? Sí
Descripción: Asediar la fortaleza de Harrenhal
Tipo de evento: Asedio
Era: DC
Ubicación: Harrenhal

Restricciones de inclusión de recursos por tipo de evento:
- Asedio requiere Maquinaria de asedio, Ingeniero de asedio, Arqueros e Infantería pesada
...

Recursos disponibles:
7: Maquinaria de asedio Arryn (tipo: Maquinaria de asedio, casa: Arryn)
8: Ingeniero de asedio Arryn (tipo: Ingeniero de asedio, casa: Arryn)
...

Ingrese los IDs de los recursos que desea agregar (separados por comas): 7,8

Año - Inicio: 302
Mes - Inicio [1-12]: 1
Día - Inicio [1-31]: 20
Hora - Inicio [0-23]: 8
Minuto - Inicio [0-59]: 0
Año - Fin: 302
Mes - Fin [1-12]: 1
Día - Fin [1-31]: 20
Hora - Fin [0-23]: 18
Minuto - Fin [0-59]: 0

¿Desea buscar el próximo hueco disponible para estos recursos? Sí
Buscando hueco en los próximos 30 días...
Hueco encontrado: 302-01-20 08:00 - 302-01-20 18:00
¿Desea usar este hueco? Sí
✅ Evento 'Asedio a Harrenhal' agregado con ID: 2
```

#### `l` - Listar Eventos

Muestra una tabla con todos los eventos planificados:

- ID (cian)
- Nombre (blanco)
- Tipo (magenta)
- Era (amarillo)
- Descripción (magenta)
- Estado (magenta)
- Inicio (verde)
- Fin (verde)
- Recursos (amarillo) - IDs separados por comas

**Ejemplo de salida:**
```
Lista de Eventos
┌────┬─────────────────────┬──────────┬──────┬──────────────────────────┬─────────┬─────────────────────┬─────────────────────┬──────────┐
│ ID │ Nombre              │ Tipo     │ Era  │ Descripción              │ Estado  │ Inicio              │ Fin                 │ Recursos │
├────┼─────────────────────┼──────────┼──────┼──────────────────────────┼─────────┼─────────────────────┼─────────────────────┼──────────┤
│ 1  │ Defensa de Invernalia│ Defensa  │ DC   │ Defender las murallas... │ planned │ 302-01-15 08:00     │ 302-01-15 20:00     │ 89,93,101│
│ 2  │ Asedio a Harrenhal  │ Asedio   │ DC   │ Asediar la fortaleza...  │ planned │ 302-01-20 08:00     │ 302-01-20 18:00     │ 7,8      │
└────┴─────────────────────┴──────────┴──────┴──────────────────────────┴─────────┴─────────────────────┴─────────────────────┴──────────┘
```

#### `v` - Ver Detalles

Ofrece dos subopciones:

- **`e` - Evento**: introduce el ID y muestra toda la información del evento en una tabla de dos columnas (Campo y Valor), incluyendo nombre, descripción, tipo, era, ubicación, inicio, fin, duración, recursos y estado.
- **`r` - Recurso**: introduce el ID del recurso y muestra su agenda completa con todos los eventos en los que participa, sus fechas y estado.

**Ejemplo de detalle de evento (ID 1):**
```
Acción: e
Introduzca el ID del evento para mostrar los detalles: 1
Detalles del evento número 1
┌────────────┬──────────────────────────────┐
│ Campo      │ Valor                        │
├────────────┼──────────────────────────────┤
│ Nombre     │ Defensa de Invernalia        │
│ Descripción│ Defender las murallas...     │
│ Tipo       │ Defensa                      │
│ Era        │ DC                           │
│ Ubicación  │ Invernalia                   │
│ Inicio     │ 302-01-15 08:00              │
│ Fin        │ 302-01-15 20:00              │
│ Duración   │ 12:00:00                     │
│ Recursos   │ 89, 93, 101                  │
│ Estado     │ planned                      │
└────────────┴──────────────────────────────┘
```

**Ejemplo de agenda de recurso (ID 89 - Infantería pesada Stark):**
```
Acción: r
Introduzca el id del recurso: 89
Agenda del recurso: Infantería pesada Stark (ID: 89)
┌───────────┬─────────────────────┬──────────┬──────┬─────────────────────┬─────────────────────┬─────────┐
│ Evento ID │ Nombre              │ Tipo     │ Era  │ Inicio              │ Fin                 │ Estado  │
├───────────┼─────────────────────┼──────────┼──────┼─────────────────────┼─────────────────────┼─────────┤
│ 1         │ Defensa de Invernalia│ Defensa  │ DC   │ 302-01-15 08:00     │ 302-01-15 20:00     │ planned │
└───────────┴─────────────────────┴──────────┴──────┴─────────────────────┴─────────────────────┴─────────┘
```

#### `d` - Eliminar Evento

1. Muestra la lista de eventos existentes con ID, nombre y fecha de inicio.
2. Solicita el ID del evento a eliminar.
3. Confirma la eliminación y libera los recursos.
4. Muestra mensaje de éxito en verde.

**Ejemplo:**
```
Eventos existentes:
ID: 1 - Defensa de Invernalia (302-01-15 08:00)
ID: 2 - Asedio a Harrenhal (302-01-20 08:00)
Introduzca el id del evento que desea eliminar o presione 's' para salir: 2
✅ Evento 2 eliminado satisfactoriamente :)
```

#### `s` - Salir

Guarda automáticamente el estado y cierra la aplicación.

---

## 🚫 Restricciones del Dominio

El sistema implementa cinco tipos de restricciones que reflejan la lógica del universo de *Game of Thrones* y las tácticas militares.

### 1. Inclusión entre Recursos (Co-requisitos)

Un recurso siempre requiere otro complementario para ser utilizado:

| Recurso Principal | Recurso Requerido |
|-------------------|-------------------|
| Maquinaria de asedio | Ingeniero de asedio |
| Fuego Valyrio | Piromante |
| Maestro de espías | Oro |
| Mercenarios | Oro |
| Dragón | Noble de sangre valyria |
| Espada de acero valyrio | Noble |
| Flota | Almirante |

### 2. Exclusión Mutua entre Recursos

Ciertos recursos no pueden combinarse en un mismo evento:

| Recurso A | Recurso B (excluido) |
|-----------|---------------------|
| Fuego Valyrio | Maquinaria de asedio |
| Mercenarios | Caballero |
| Dragón | Maquinaria de asedio |
| Maestro de espías | Caballero |

### 3. Inclusión por Tipo de Evento

Cada tipo de evento exige recursos específicos:

| Tipo de Evento | Recursos Requeridos |
|----------------|---------------------|
| Asedio | Maquinaria de asedio, Ingeniero de asedio, Arqueros, Infantería pesada |
| Batalla naval | Almirante, Flota, Fuego Valyrio |
| Batalla campal | Infantería pesada, Caballería pesada, Arqueros |
| Asalto | Infantería pesada, Caballería pesada |
| Defensa | Infantería pesada, Arqueros |
| Emboscada | Infantería ligera, Arqueros |
| Misión diplomática | Embajador |

### 4. Exclusión por Tipo de Evento

Cada tipo de evento prohíbe ciertos recursos:

| Tipo de Evento | Recursos Prohibidos |
|----------------|---------------------|
| Emboscada | Maquinaria de asedio |
| Batalla naval | Caballería pesada, Caballería ligera |
| Batalla campal | Maestro de espías, Flota |
| Asedio | Caballería pesada, Caballería ligera |
| Defensa | Caballería pesada, Caballería ligera |
| Asalto | Maquinaria de asedio |
| Misión diplomática | Maquinaria de asedio |

### 5. Exclusión entre Casas (Enemistades)

Las casas enemigas no pueden compartir un mismo evento:

| Casa | Enemigas |
|------|----------|
| Lannister | Stark, Targaryen, Tully, Martell |
| Stark | Lannister, Bolton, Greyjoy |
| Targaryen | Baratheon, Lannister |
| Baratheon | Targaryen |
| Tully | Lannister, Frey |
| Martell | Lannister |
| Greyjoy | Stark |
| Bolton | Stark |
| Frey | Stark, Tully |
| Arryn | Lannister |

---

## 📁 Estructura del Proyecto

```
war-is-coming/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py          # Clase Event con métodos de conversión y __lt__
│   │   └── resource.py       # Clase Resource con atributos (casa, tipo)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_manager.py   # Persistencia CRUD + estado global + funciones auxiliares
│   │   └── planner.py        # Validación de restricciones + búsqueda de huecos
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── main_menu.py          # Menú principal con Panel
│   │   ├── command_add_event.py  # Asistente de creación con visualización de restricciones
│   │   ├── command_list_events.py
│   │   ├── command_view_details.py
│   │   └── command_delete_event.py
│   └── data/
│       └── default_data.json     # Datos iniciales (recursos + restricciones)
├── data/                        # Directorio de datos de trabajo
│   └── war_planner.json         # Estado guardado (se genera automáticamente)
├── main.py                      # Punto de entrada
├── README.md
├── requirements.txt
└── pyproject.toml               # Metadatos del proyecto
```

### Detalles de Archivos Clave

- **`event.py`**: Define la clase `Event` con atributos como id, name, start, end, event_type, resources_ids, status, era. Implementa `__lt__` para ordenamiento cronológico y métodos de serialización.

- **`resource.py`**: Define la clase `Resource` con atributos id, name, resource_type, house. Los métodos `robject_to_dict` y `create_robject_from_dict` usan consistentemente `"resource_type"` como clave.

- **`data_manager.py`**: Gestiona el estado global con variables EVENTS, RESOURCES, RESTRICTIONS, NEXT_EVENT_ID. Incluye funciones para carga, guardado, CRUD de eventos y funciones auxiliares como `get_event_by_type()` y `get_events_in_range()`.

- **`planner.py`**: Contiene el motor de validación con funciones específicas para cada tipo de restricción y el algoritmo de búsqueda de huecos `find_next_available_time_slot` con búsqueda granular.

- **`command_add_event.py`**: El comando más complejo, con visualización de restricciones, selección de recursos con validación, entrada de fechas por componentes y búsqueda de huecos opcional.

---

## 🔮 Mejoras Futuras

Funcionalidades opcionales para futuras versiones:

### Recursos con Cantidad (Pools)
En lugar de recursos únicos, permitir cantidades disponibles (ej. "Infantería pesada" cantidad: 5). El sistema deberá comprobar que queden unidades disponibles en lugar de un simple ocupado/libre. Esto requeriría modificar la lógica de conflictos para manejar cantidades.

### Eventos Recurrentes
Añadir opción para crear eventos que se repitan automáticamente cada día, semana o mes. El sistema validará conflictos y restricciones para cada ocurrencia individual, planificando todas las ocurrencias futuras.

### Actualización de Estado
Implementar `update_event_status()` para cambiar el estado de los eventos (planned → in progress → completed → cancelled). Esto permitiría un seguimiento más preciso del ciclo de vida de los eventos.

### Reportes y Estadísticas
- Generar informes de uso de recursos por casa.
- Estadísticas de ocupación y disponibilidad.
- Visualización de calendario mensual.
- Reportes de conflictos y restricciones violadas.

### Filtros y Búsquedas Avanzadas
- Filtrar eventos por tipo, era, casa, estado.
- Buscar eventos por nombre o descripción.
- Ver eventos en un rango de fechas específico.
- Visualización de recursos por casa (como se sugiere en ToDo.md).

### Interfaz Gráfica
Portar la aplicación a una GUI con Tkinter o PyQt para una experiencia más visual. La arquitectura en capas facilita esta transición.

---

## 📄 Licencia

Distribuido bajo licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">
  <p>Hecho por <strong>Cynthia Moreno Miranda</strong></p>
  <p><em>MatCom 2025-2026</em></p>
  <p>
    <a href="#top">⬆️ Volver al inicio</a>
  </p>
</div>
<a id="top"></a>

<div align="center">
  <img src="https://img.icons8.com/color/96/sword.png" alt="Espada">
  <img src="https://img.icons8.com/color/96/dragon.png" alt="Dragón">
  <img src="https://img.icons8.com/color/96/castle.png" alt="Castillo">
  <h1>War is coming</h1>
  <p><em>Planificador de Eventos Bélicos – Universo de A Song of Ice and Fire</em></p>
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
</p>

<div align="center">
  <a href="#-acerca-del-proyecto">Acerca del Proyecto</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-características">Características</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-arquitectura">Arquitectura</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-tecnologías">Tecnologías</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-cómo-empezar">Cómo Empezar</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-instrucciones-de-uso">Instrucciones de Uso</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-restricciones-del-dominio">Restricciones</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-pruebas">Pruebas</a>
  <span>&nbsp;⚔️&nbsp;</span>
  <a href="#-licencia">Licencia</a>
</div>

<br>

---

## 📃 Acerca del Proyecto

**War is Coming** es un sistema inteligente de planificación de eventos militares inspirado en el universo de *Canción de Hielo y Fuego*. La aplicación permite a un comandante organizar campañas bélicas (asedios, batallas navales, asaltos, defensas, emboscadas) asignando recursos limitados – tropas de distintas casas, maquinaria de asedio, elementos especiales como Fuego Valyrio – respetando estrictas reglas de co‑requisito, exclusión mutua y conflictos temporales.

El sistema garantiza que ningún recurso se asigne a dos eventos simultáneamente, que las combinaciones de recursos cumplan la lógica del universo (las casas enemigas no pueden compartir evento) y que cada tipo de evento exija o prohíba ciertos recursos. Todo ello mediante un motor de planificación que valida restricciones y busca automáticamente el próximo hueco disponible.

El proyecto ha sido desarrollado aplicando principios de modularidad, buenas prácticas de Python y una interfaz de consola enriquecida con la librería `rich`.

---

## ✨ Características

- **Planificación inteligente**: validación automática de disponibilidad de recursos, conflictos horarios y cumplimiento de restricciones personalizadas.
- **Búsqueda de huecos**: encuentra el siguiente intervalo libre para agendar un evento sin colisiones ni violaciones de reglas.
- **Inventario de recursos**: unidades militares con atributos (casa, tipo) que definen su comportamiento en las restricciones.
- **Restricciones configurables**:
  - Co‑requisito (inclusión): un recurso requiere otro para ser usado (ej. maquinaria de asedio necesita infantería).
  - Exclusión mutua: ciertos recursos no pueden combinarse en un mismo evento (ej. Lannister y Stark no se alían).
  - Por tipo de evento: cada tipo exige o prohíbe recursos específicos (ej. Asedio necesita maquinaria; Batalla Naval no permite caballería).
- **Gestión de eventos**: añadir, listar, ver detalles y eliminar eventos, con persistencia automática en JSON.
- **Interfaz de consola CLI**: menú interactivo con paneles, tablas y colores gracias a `rich`.
- **Persistencia completa**: el estado (recursos, restricciones, eventos) se guarda y carga desde un único archivo JSON.

---

## 🏰 Arquitectura

El código se organiza en capas modulares siguiendo principios de separación de responsabilidades:

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| **Modelos** | `src/models/` | Definición de las entidades `Event` y `Resource` con métodos de conversión a/desde diccionario. |
| **Servicios** | `src/services/` | Lógica de negocio: `data_manager` (persistencia y operaciones CRUD) y `planner` (validación de restricciones y búsqueda de huecos). |
| **Interfaz** | `src/interface/` | Comandos CLI (`add`, `list`, `delete`, `view`) y menú principal con `rich`. |
| **Datos** | `src/data/` | Configuración inicial por defecto (recursos y restricciones predefinidas). |

### Flujo Principal

1. **Inicialización**: carga del estado desde `war_planner.json` o datos por defecto.
2. **Menú principal**: el usuario elige comandos (agregar, listar, ver, eliminar, salir).
3. **Agregar evento**: asistente paso a paso que recoge nombre, tipo, recursos, fechas y valida todo.
4. **Búsqueda de hueco**: si el usuario lo solicita, el motor sugiere el próximo intervalo libre.
5. **Persistencia automática**: cada cambio en el estado se guarda en el archivo JSON.
6. **Comandos auxiliares**: listado, detalles y eliminación de eventos.

---

## ⚒️ Tecnologías

- **Python 3.12+**: lenguaje principal.
- **Rich**: librería para interfaces de consola avanzadas (tablas, colores, paneles, prompts).
- **Datetime**: gestión de fechas, duraciones y comparaciones temporales.
- **Bisect**: mantenimiento de la lista de eventos ordenada cronológicamente.
- **JSON**: persistencia de datos en archivo.
- **Pytest** (pendiente de implementación): pruebas unitarias planificadas.

---

## 🚀 Cómo Empezar

### Requisitos
- Python 3.12 o superior
- pip (gestor de paquetes)

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/war-is-coming.git
   cd war-is-coming
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install rich
   ```

4. Ejecuta la aplicación:
   ```bash
   python -m src.interface.main_menu
   ```

5. Sigue las instrucciones en consola.

---

## 📋 Instrucciones de Uso

Al iniciar, verás un panel de bienvenida y un menú con los siguientes comandos:

- **`a` (Agregar evento)**: asistente que te guía paso a paso:
  1. Introduce el nombre y descripción (opcional).
  2. Selecciona el tipo de evento (Asedio, Batalla Naval, Asalto, Defensa, Emboscada, Batalla Campal).
  3. Especifica la ubicación (opcional).
  4. Consulta el listado de recursos disponibles con sus IDs, tipos y casas.
  5. Introduce los IDs de los recursos separados por comas.
  6. Proporciona fecha y hora de inicio y fin (con validación de rangos).
  7. Opcionalmente, pide al sistema que busque el próximo hueco disponible para esos recursos.
  8. Si se encuentra un hueco, se muestra y se pregunta si se desea usar; en caso contrario, se notifica.
  9. El evento se valida (restricciones y conflictos) y se agrega.

- **`l` (Listar eventos)**: muestra una tabla con todos los eventos planificados, incluyendo ID, nombre, fechas, tipo y recursos asignados.

- **`v` (Ver detalles)**: solicita el ID de un evento y muestra toda su información (nombre, descripción, fechas, tipo, ubicación, recursos, estado).

- **`d` (Eliminar evento)**: pide el nombre o ID del evento y lo elimina, liberando sus recursos.

- **`s` (Salir)**: cierra la aplicación.

Todos los comandos manejan errores de entrada y muestran mensajes claros en rojo o verde.

---

## 🚫 Restricciones del Dominio

El sistema implementa cuatro tipos de restricciones que reflejan la lógica del universo de *Game of Thrones* y las tácticas militares:

### 🚩 Exclusión Mutua entre Recursos
- **Infantería Lannister** no puede coincidir con **Infantería Stark**.
- **Caballería Lannister** no se alía con **Caballería Stark**.
- **Maquinaria Lannister** no se usa junto a **Caballería Stark**.
- **Fuego Valyrio** no se combina con **maquinaria de asedio** por seguridad.

### 🚩 Co‑requisito (Inclusión)
- **Maquinaria de asedio** siempre requiere **infantería pesada**.
- **Fuego Valyrio** necesita un **Piromante**.
- **Maestre de Guerra** exige **infantería pesada** y **maquinaria de asedio**.

### 🚩 Por Tipo de Evento
**Inclusiones forzosas**:
- *Asedio* → debe incluir maquinaria de asedio.
- *Batalla Naval* → debe incluir Fuego Valyrio.
- *Asalto* → debe incluir infantería y caballería.
- *Defensa* → debe incluir infantería y arqueros.

**Exclusiones obligatorias**:
- *Emboscada* → no puede usar maquinaria.
- *Batalla Naval* → no puede usar caballería.
- *Asedio* → no puede usar caballería.
- *Defensa* → no puede usar caballería.

### 🚩 Enemistades entre Casas
- **Lannister** enemiga de *Martell*, *Stark*, *Targaryen* y *Tully*.
- **Stark** enemiga de *Lannister*, *Bolton* y *Greyjoy*.
- **Targaryen** enemiga de *Baratheon* y *Lannister*.
- **Tully** enemiga de *Lannister* y *Frey*.
- **Martell** enemiga de *Lannister*.
- **Greyjoy** enemiga de *Stark*.
- **Bolton** enemiga de *Stark*.
- **Frey** enemiga de *Stark* y *Tully*.

Todas estas reglas se validan automáticamente al agregar un evento y durante la búsqueda de huecos, garantizando que ningún planificador pueda violarlas.

---

## 🔑 Licencia

Distribuido bajo licencia MIT. Ver el archivo `LICENSE` para más detalles.
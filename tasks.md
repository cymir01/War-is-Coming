# ToDo:
- 4.Requisitos Técnicos y Entregables
- Cada función debería llevar un comentario que explique con concisión lo que hace. El comentario debería aparecer inmediatamente después de la definición de la función y emplear el formato de la cadena de documentación
- hacer menus de seleccion siempre que pueda para que el usuario no tenga que ingresar manualmente la informacion y evitar errores y asi tener que gestionar menos errores... si no usar un while True como en main para que itere hasta que se ingrese bien la info, por ejemplo con las fechas
- Función que compare un evento con una lista de eventos y vea si se interesctan
- Agregar a Evento el atributo tipo de evento y además agregarle ID para manejar la info más cómodo
- Terminar el capítulo sobre OOP del libro de Python
- Estudiarme la cp08 de pro
- Leer el capítulo sobre trabajo con archivos en el libro de Python
- Hacer que las fechas se ingresen por año, mes y dia... ver como mejorar la visual de esa seccion en main
- Terminar de hacer el validador de fechas personalizado para el continente de Poniente

## Restricciones
- poner una restriccion temporal. Como en Google Calendar, cuando el usuario intente crear un evento con una fecha anterior a la fecha actual el programa debe alertar el error y pedi rde nuevo la fecha (esto tiene que ver con lo que escribi en la linea 5 sobre gestioanr el ingreso de fechas con un while true)
- Restriccion entre casas: Agregar en la logica de validacion una cronologia especifica a partir de la cual se establece una restriccion de exclusion entre las casas
- agregarle como atributo a Evento la escala de la batalla para luego agregarle como atributo a la clase Resource la cantidad de unidades segun la escala de la batalla... esa informacion la va utilizar el gestor de restricciones para saber que catnidad de unidades asignar al evento segun su escala
- Otra restrivccion: entre dos eventos proximos debe haber una especie de tiempo de recuperacion, por que un evento belico no puede empezar justo cuando acaba otro, las tropas tienen que desplazarse, hay que reparar las maquinaria, etc.. esa es otra restriccion temporal

## DUDAS
- Preguntarle a los profes si hago opcionales descripcion y demas del evento

# Ideas:
Idea de Antony:
Hacer 3 clases basicas que necesites (eventos, recursos y restricciones)
Sumas cosas
Ver como unirlas (un game manager)

## Interface (opcionales)
- hacer barra de estado o calendario para ver progreso/timeline
- add soundtrack (main theme de GoT, etc)
- Agregar esta funcionalidad: Eliminar un evento existente, liberando sus recursos para que queden disponibles
- Ver Detalles de un evento específico (qué recursos usa, a qué hora) o de un recurso (cuál es su agenda)

Los eventos que se creen deben gauradarse en un archivo json para garantizar la persistencia de los datos y luego aparte, dentro de la logica estara la funcion listar_eventos 

# Doubts

# Bugs:

# Resources:
## Programming part
Standard Colors — Rich 14.1.0 documentation https://rich.readthedocs.io/en/stable/appendix/colors.html
Turtle Programming in Python - GeeksforGeeks https://share.google/GovFICQbQvXuQfdPr

### Revisar:
Top 20 Python Libraries To Know in 2025 - GeeksforGeeks https://share.google/XELxyd3gcEOty7XBY

Python built-in functions
https://docs.python.org/3/library/functions.html

Python Projects - Beginner to Advanced - GeeksforGeeks https://share.google/RpXA54CxO1fXUmCWg

Event Management System Using Python Django - GeeksforGeeks https://share.google/Vowt4rVnY9VzfvwP0

12 python scripts to organize your daily workflow
https://open.substack.com/pub/pythonclcoding/p/12-python-scripts-to-organize-your?utm_source=share&utm_medium=android&r=5ipczn

----------

3.14.0 Documentation Python https://share.google/vNWNmJFRpiW3UchTq
Curso Intensivo de Python
Automate the Boring Stuff with Python
Math Adventures with Python
Using Python datetime to Work With Dates and Times – Real Python https://realpython.com/python-datetime/
Working With JSON Data in Python – Real Python https://share.google/IcL3xCt6OPP9q0rPc
Python píldorasinformaticas https://youtube.com/playlist?list=PLU8oAlHdN5BlvPxziopYZRd55pdqFwkeS&si=YK1tFiP2kI7briX1
Mostly Python https://share.google/kzzpwdhRDjqRVJzRF
CP08 PRO
DeepSeek
GeeksforGeeks | Your All-in-One Learning Portal https://share.google/fkPmb4uxNCVQaHb3Y

Probar la app uv para la gestión de entornos virtuales para próximos proyectos…
https://share.google/0lnp88MOeVPpNTJNq

## About Westeros
Militar Tecnology
https://gameofthrones.fandom.com/wiki/Science_and_technology#Military_technology
https://es.wikipedia.org/wiki/Arma_de_asedio
https://awoiaf.westeros.org/index.php/Battles_of_Westeros
https://awoiaf.westeros.org/index.php/Armament

Houses

Calendar




import datetime
from date_validation import overlap
# from rich.console import Console
# from rich.table import Table
# from rich.panel import Panel
# from rich.prompt import Prompt
# from rich.prompt import Confirm
# from rich.text import Text
# from core import agregar_tarea, listar_tareas
# import turtle

# console = Console()

# panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
# console.print(panel)
# nombre = Prompt.ask("¿Cuál es tu nombre, lord?")

# tabla = Table(title="Ejércitos de Poniente")
# tabla.add_column("Casa", style="cyan")
# tabla.add_column("Líder", style="magenta")
# tabla.add_column("Tropas", justify="right")
# tabla.add_row("Stark", "Robb Stark", "20,000")
# tabla.add_row("Lannister", "Tywin Lannister", "35,000")
# console.print(tabla)

# confirmar = Confirm.ask("¿Iniciar la batalla?")

# console.print("--- Gestor de Tareas ---")

# while True:  
#     cmd = console.input("[bold cyan]Acción (agregar, listar, salir): [/bold cyan]\n")
#     if cmd == 'agregar': 
#         desc = console.input("Descripción de la tarea: \n") 
#         agregar_tarea(desc) 
#     elif cmd == 'listar':
#         tareas = listar_tareas() 
#         if not tareas: 
#             console.print("[yellow]No hay tareas.[/yellow]") 
#         else:
#             table = Table(title="Lista de Tareas") 
#             table.add_column("ID", style="cyan") 
#             table.add_column("Descripción", style="magenta") 
#             table.add_column("Estado", style="green")  
            
#             for id, tarea in tareas.items(): 
#                 table.add_row(str(id), tarea['desc'], tarea['estado'])  
            
#             console.print(table)
#     elif cmd == 'salir': 
#         console.print("Adios") 
#         break 
#     else:
#         console.print("Comando no reconocido\n")

# pen = turtle.Turtle()
# ventana = turtle.Screen()
# ventana.title("Pa mi cosito")

# def curve():
#     for i in range(200):
#         pen.right(1)
#         pen.forward(1)

# def heart():
#     pen.fillcolor('red')
#     pen.begin_fill()
#     pen.left(140)
#     pen.forward(113)
#     curve()
#     pen.left(120)
#     curve()
#     pen.forward(112)
#     pen.end_fill()

# def text():
#     pen.up()
#     pen.setpos(-68, 95)
#     pen.down()
#     pen.color('white')

#     pen.write("Te amo Tobariii", font=("Verdana", 12, "bold"))

# heart()
# text()
# pen.ht()
# ventana.mainloop()

fecha1 = datetime.datetime(2005, 5, 10)
fecha2 = datetime.datetime(2000, 2, 10)
fecha3 = datetime.datetime(2000, 3, 1)
fecha4 = datetime.datetime(2010, 5, 10)

print(overlap([fecha1, fecha2], [fecha3, fecha4]))

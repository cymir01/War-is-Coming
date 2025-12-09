from rich.console import Console

#!agregar la funcion de liberar los recursos que usa el evento
def command_delete():
    events = {'name': "nombre"}
    while True:
        console = Console()
        cmd = console.print("Introduzca el nombre del evento que desea eliminar o presione  ")
        if cmd.lower() == 's':
            break
        if cmd == events[name]:
            del events[name]
            break
        else:
            return "El evento no existe"
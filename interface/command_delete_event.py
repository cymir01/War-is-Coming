from rich.console import Console

#!agregar la funcion de liberar los recursos que usa el evento
#!usar lower y strip para estandarizar los nombres y evitar potenviales errores al comparar
def command_delete():
    events = {'name': "nombre"}
    while True:
        console = Console()
        cmd = console.input("Introduzca el nombre del evento que desea eliminar o presione  ")
        if cmd.lower() == 's':
            break
        #!agregar aqui la funcion de listar eventos por si el usaurio quiere revisar antes de eliminar
        #!ver como manejar el default value de pop y el retorno, puedo usarlo para imprimir notifcaciones al usuario
        if cmd == events["name"]:
            event_deleted = events.pop(cmd, None)
            print(f"El evento {event_deleted} ha sido eliminado satisfactoriamente")
            break
        if event_deleted is not None:
            console.print(f"[green]El evento {event_deleted} ha sido eliminado satisfactoriamente[/green]")
        else:
            return "El evento no existe"
        
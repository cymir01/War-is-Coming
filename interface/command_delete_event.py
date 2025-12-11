from rich.console import Console

#!agregar la funcion de liberar los recursos que usa el evento
#!usar lower y strip para estandarizar los nombres y evitar potenviales errores al comparar
def command_delete():
    events = {'name': "nombre"}
    while True:
        console = Console()
        cmd = console.print("Introduzca el nombre del evento que desea eliminar o presione  ")
        if cmd.lower() == 's':
            break
        #!agregar aqui la funcion de listar eventos por si el usaurio quiere revisar antes de eliminar
        #!ver como manejar el default value de pop y el retorno, puedo usarlo para imprimir mnotifcaciones al usuario
        if cmd == events["name"]:
            event_deleted = events.pop(cmd) #!ponerle un default value
            print(f"El evento {event_deleted} ha sido eliminado satisfacotriamente")
            break
        else:
            return "El evento no existe"
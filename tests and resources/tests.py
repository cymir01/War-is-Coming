# while True:
#     try:
#         events = {
#             "1": {
#                 "desc": "tarea",
#                 "estado": "pendiente"
#             }
#         }
#         cmd = input("id \n")
#         id = events[cmd]
#         print(id)
#         break
#     except Exception:
#         print("mal")

events = {
            "1": {
                "desc": "tarea",
                "estado": "pendiente"
            }
        }
cmd = input("id \n")
id = events.get(cmd, "no existe el evento solicitado")
print(id)

# alumno = {
#     'nombre': 'Ana', #key: value
#     'id_matricula': 12345, 
#     'curso_actual': 'Programación I', 
#     "activa": True
#     }

# nombre = alumno.get('nombre', 'no especificado')

# print(nombre)
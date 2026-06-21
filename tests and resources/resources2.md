para pasarle a las funciones pertinentes los recursos que solicita el usuario para determinado evento debo guardar los recursos solicitados por el usuario en un diccionario que contenga los diccionarios de los recuresos (cada recurso es un diccionario). de modo que tengo que actualizar el inventario de recursos en el json, extrayendo los recursos (diccionarios) que solicite el usuario y pasandoselos a las funciones para luego guardar el diccionario de diccionarios en el diccionario de eventos

(escalable)
resoruces: diccionario con id como llave y diccionarios de recursos como valores
{
    "1": {
        "name": "tal",
        "house": "tal",
        "amount": "tal"
    }
}

el atributo casa sirve para poder hacer las restricciones de exclusion entre casas. Si el ususario quiere usar dos recuross pertencecientes a casas enemistadas el programa dará error

el atributo amount sirve para restricciones de inclusion y exclusion tambien

recursos:
Infanteria pesada 
infanteria ligera
caballeria pesada
caballeria ligera
mercenarios 
arqueros 
maestro de espias 
caballero 
almirante
caballo 
arakh
jinete de sangre valyria
dragon 
maquinaria de asedio 
ingeniero de asedio 
oro
espada de acero valyrio
guerrero de linaje noble



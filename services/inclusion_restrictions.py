
def event_type_inclusion_restriction(type, resources):

    required_resources = {
        "Asedio a Castillo": ["Maquinaria de Asedio", "Arqueros", "Infantería Pesada"],
        "Batalla Naval": ["Almirante", "Armada"],
        "Batalla Campal": ["Infantería Pesada", "Caballería Pesada", "Arqueros"],
        "Torneo de Caballeros": ["Caballeros", "Ca"],
        "Emboscada": ["Infantería Ligera", "Caballería Ligera", "Arqueros"],
        "Misión de Espionaje": ["Maestro de Espías"]
    }

    needed = required_resources[type]
    
    if resources not in needed:
        pass


event_type_inclusion_restriction(type="Asedio a Castillo", resources=["2"])

def inclusion_restriction_special_resources(resources):
    error = False
    if "Mercenario" in resources and "Oro" not in resources:
        error = True
    return error

def atm():
    balance = int(input("What is your current balance? "))
    withdrawal_amount = int(input("Enter the amount to withdraw "))
    error = False

    if withdrawal_amount <= 0:
        error = True
        print("Withdrawal amount cannot be negative or 0")
    if balance < withdrawal_amount:
        error = True
        print("Insufficient balance")
    if withdrawal_amount%10 != 0:
        error = True
        print("Withdrawal amount must be a multiple of 10")
    if not error:
        print("Remaining balance:", balance - withdrawal_amount)
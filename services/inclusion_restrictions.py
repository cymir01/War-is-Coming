
def event_type_inclusion_restriction(type, resources):
    error = False
    required_resouces = {
        "Asedio a Castillo": ["Maquinaria de Asedio", "Arqueros", "Infantería Pesada"],
        "Batalla Naval": ["Almirante", "Armada"]
    }
    # if type == "Asedio a Castillo":
    #     if resource != "Maquinaria de Asedio" or resource != "Arqueros" or resource != "Infantería Pesada":
    #         error = True
    # if type == "Batalla Naval":
    #     if resource != "Almirante" or resource != "Armada":
    #         error = True
    # if type == "Batalla Campal":
    #     if resource != "Infantería Pesada" or resource != ""
    # if type == "Torneo de Caballos":
    #     if resource != "Caballeros" or resource != "Caballos":
    #         error = True
    # if type == "Emboscada":
    #     if resource != "Caballería Ligera" or resource != "Infantería Ligera" or resource != "Arqueros":
    #         error =  True
    # if type == "Misión de Espionaje":
    #     if resource != "Maestro de Espías":
    #         error = True
    # return error

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

event_type_inclusion_restriction(type="4", resources=[4, 3])
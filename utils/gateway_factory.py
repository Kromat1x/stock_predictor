import random

class Gateway:
    def process_transaction(self, amount):
        gateway = get_getway(amount)
        return gateway()

def get_getway(amount):
    if amount <= 20:
        return cheap_gateway
    elif 20 < amount <= 500:
        return expensive_gateway
    elif amount > 500:
        return premium_gateway

def cheap_gateway():
    deciding_value = random.uniform(0, 1)

    if deciding_value > 0.5:
        return True, "Cheap Gateway"
    else:
        return False, "Cheap Gateway"

def expensive_gateway():
    deciding_value = random.uniform(0, 1)

    if deciding_value > 0.5:
        return True, "Expensive Gateway"
    else:
        return cheap_gateway()
    
def premium_gateway():
    for i in range(0, 3):
        deciding_value = random.uniform(0, 1)
        if deciding_value > 0.5:
            return True, "Premium Gateway"
    return False, "Premium Gateway"
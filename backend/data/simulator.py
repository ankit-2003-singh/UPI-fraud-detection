import random

users = ["Amit","Neha","Rahul","Priya","Karan","Sneha","Vikram","Riya"]

def generate_tx():
    return {
        "sender": random.choice(users),
        "receiver": random.choice(users),
        "amount": random.randint(100,50000),
        "freq": random.randint(1,20),
        "hour": random.randint(0,23)
    }

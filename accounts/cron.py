from datetime import datetime

from .models import User

def resetWatered():
    users = User.objects.all()
    for i in range(users.count()):
        users[i].watered = 1
        users[i].save()
    return
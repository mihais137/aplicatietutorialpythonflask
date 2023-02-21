from . import db
from website.models import User
from website.models import Clasament

users=User.query.all()
places=Clasament.query.all()
maxim1=0
maxim2=1000
i=1
for place in places:
    for user in users:
        if user.punctaj>maxim1 and user.punctaj<maxim2:
            maxim1=user.punctaj
    for user in users:
        if user.punctaj==maxim1:
            place.username=user.username
            place.loc=i
    i=i+1
    maxim2=maxim1
    maxim1=0

db.session.commit()

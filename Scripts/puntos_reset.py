import os
import sys
sys.path.append('/home/rewr/AstroBurger')
# sys.path.append('/Users/Rafael/django/REWR')
os.environ['DJANGO_SETTINGS_MODULE'] = 'betc.settings'
import django
django.setup()

from betcnow.models import Profile
from django.utils import timezone
from django.core.mail import EmailMessage

if timezone.now().day == 1:
    ganador = Profile.objects.filter(membresia__tipo_membresia="Member").order_by('-puntos')[0]
    Profile.objects.all().update(puntos=0)
    string = "Ganador: " + ganador + "(" + ganador.address + ")" + ". Todo reseteado ahora"
    print(string)
    email = EmailMessage('Ganador Bitcoin-Race', string, to=['betcnow@gmail.com'])
    email.send()

print("Complete")

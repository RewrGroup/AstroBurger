import os
import sys
sys.path.append('/home/rewr/AstroBurger')
os.environ['DJANGO_SETTINGS_MODULE'] = 'betc.settings'
import django
django.setup()

from betcnow.models import Profile
from django.utils import timezone

if timezone.now().day == 1:
    Profile.objects.all().update(puntos=0)
    print("Reseteado")

print("Complete")

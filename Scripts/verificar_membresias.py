import os
import sys

sys.path.append('/home/rewr/AstroBurger')
# sys.path.append('/Users/Rafael/django/REWR')
os.environ['DJANGO_SETTINGS_MODULE'] = 'betc.settings'
import django

django.setup()

from betcnow.models import Profile
from django.utils import timezone

hoy = timezone.now().date()
Profile.objects.filter(valid_thru=hoy).update(membresia="Free", valid_thru=None)

print("Complete")
from django.utils import timezone
from betcnow.models import Profile

if timezone.now().day == 8:
    Profile.objects.all().update(puntos=0)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sponsor = models.ForeignKey(User, to_field='username', related_name='spn',
                                default='betcnow', on_delete=models.SET_DEFAULT)
    sponsor_revenue = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Pote(models.Model):
    valor_jugada = models.IntegerField()
    STATUS_CHOICES = (
        ('1', 'Abierto'),
        ('0', 'Cerrado'),
        ('-1', 'Pre-Cerrado')
    )
    status = models.CharField(max_length=30, default='1', choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.id)


class Jugada(models.Model):
    pote = models.ForeignKey(Pote, to_field='id')
    numero = models.IntegerField()
    jugador = models.ForeignKey(User, blank=True, null=True)
    STATUS_CHOICES = (
        ('1', 'Libre'),
        ('2', 'Reservado'),
        ('3', 'Pagado'),
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='1')
    RESULTADO_CHOICES = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
    )
    resultado = models.CharField(max_length=30, blank=True, null=True, choices=RESULTADO_CHOICES, default='')

    def __str__(self):
        return str(self.pote.id) + ": " + str(self.numero)


@receiver(post_save, sender=Pote)   # cuando se crea un nuevo pote, se hace un populate de jugadas
def llenar_jugadas(sender, instance, created, **kwargs):
    if created:
        for i in range(1000):
            Jugada.objects.create(pote=instance, numero=i)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import sorteo


class Membership(models.Model):
    tipo_membresia = models.CharField(max_length=30, unique=True)
    precio = models.FloatField()
    porcentaje_jugada = models.FloatField()

    def __str__(self):
        return self.tipo_membresia


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    membresia = models.ForeignKey(Membership, to_field='tipo_membresia', default='Free')
    miembro_hasta = models.DateField(blank=True, null=True)
    sponsor = models.ForeignKey(User, to_field='username', related_name='spn',
                                default='betcnow', on_delete=models.SET_DEFAULT)
    sponsor_revenue = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username


class Pote(models.Model):
    valor_jugada = models.FloatField()
    STATUS_CHOICES = (
        ('1', 'Abierto'),
        ('0', 'Cerrado'),
        ('-1', 'Pre-Cerrado')
    )
    status = models.CharField(max_length=30, default='1', choices=STATUS_CHOICES)
    fecha_sorteo = models.DateField(null=True, blank=True)

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
    orderID = models.CharField(max_length=100, blank=True, null=True)
    RESULTADO_CHOICES = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
        ('R', 'Repechage')
    )
    fecha_jugada = models.DateTimeField(blank=True, null=True)
    resultado = models.CharField(max_length=30, blank=True, null=True, choices=RESULTADO_CHOICES, default='')

    def __str__(self):
        return str(self.pote.id) + ": " + str(self.numero)


class Testimonio(models.Model):
    user = models.ForeignKey(User)
    texto = models.TextField(max_length=140)
    fecha = models.DateField(blank=True, null=True)
    aprobado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.fecha = timezone.now()
        return super(Testimonio, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username + " on " + str(self.fecha)


@receiver(post_save, sender=Pote)   # cuando se crea un nuevo pote, se hace un populate de jugadas
def llenar_jugadas(sender, instance, created, **kwargs):
    if created:
        for i in range(1000):
            Jugada.objects.create(pote=instance, numero=i)


@receiver(post_save, sender=Pote)  # cuando se cierra un pote, se efectua el sorteo inmediatamente
def sorteo_pote(sender, instance, created, **kwargs):
    if instance.status == '0':
        qs = Jugada.objects.filter(status='3', pote=instance)
        cant_jugadas = qs.count()
        lista_jugadas = []
        if cant_jugadas >= 135 and qs.filter(resultado='').count() == 1000:
            for i in qs:
                lista_jugadas.append(i.numero)
            sort = sorteo.Sorteo(cant_jugadas, lista_jugadas)
            sort.sortear()
            podio = [sort.primero, sort.segundo, sort.tercero]
            result_podio = ['1', '2', '3']
            for p in range(3):
                ganador = Jugada.objects.get(pote=instance, numero=podio[p])
                ganador.resultado = result_podio[p]
                ganador.save()
            for g in sort.lista_gold:
                gold = Jugada.objects.get(pote=instance, numero=g)
                gold.resultado = 'G'
                gold.save()
            for s in sort.lista_silver:
                silver = Jugada.objects.get(pote=instance, numero=s)
                silver.resultado = 'S'
                silver.save()
            for b in sort.lista_bronze:
                bronze = Jugada.objects.get(pote=instance, numero=b)
                bronze.resultado = 'B'
                bronze.save()
            for r in sort.lista_repechaje:
                rep = Jugada.objects.get(pote=instance, numero=r)
                rep.resultado = 'R'
                rep.save()
        else:
            print("No se puede sortear")


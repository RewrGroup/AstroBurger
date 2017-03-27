from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from Scripts.sorteo import Sorteo
from django.db.models import F
from django.core.mail import EmailMessage
import random


class Membership(models.Model):
    tipo_membresia = models.CharField(max_length=30, unique=True)
    precio = models.FloatField()
    porcentaje_jugada = models.FloatField()

    def __str__(self):
        return self.tipo_membresia


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name="profile")
    address = models.CharField(max_length=100, blank=True, null=True, default="")
    membresia = models.ForeignKey(Membership, to_field='tipo_membresia', default='Free')
    valid_thru = models.DateField(blank=True, null=True)
    sponsor = models.ForeignKey(User, to_field='username', related_name='spn',
                                default='betcnow', on_delete=models.SET_DEFAULT)
    sponsor_revenue = models.FloatField(blank=True, null=True, default=0)
    puntos = models.IntegerField(blank=True, null=True, default=0)

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
    total_acumulado = models.IntegerField(blank=True, null=True, default=0)
    primero = models.FloatField(blank=True, null=True, default=0)
    segundo = models.FloatField(blank=True, null=True, default=0)
    tercero = models.FloatField(blank=True, null=True, default=0)
    gold = models.FloatField(blank=True, null=True, default=0)
    silver = models.FloatField(blank=True, null=True, default=0)
    bronze = models.FloatField(blank=True, null=True, default=0)
    copper = models.FloatField(blank=True, null=True, default=0)
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
    fecha_jugada = models.DateTimeField(blank=True, null=True)
    PREMIO_CHOICES = (
        ('1', '300pts'),
        ('2', '25pts'),
        ('3', '15pts'),
        ('4', '0.0025Btc+10pts'),
    )
    premio = models.CharField(max_length=30, blank=True, default='', choices=PREMIO_CHOICES)
    RESULTADO_CHOICES = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
        ('R', 'Repechage')
    )
    resultado = models.CharField(max_length=30, blank=True, null=True, choices=RESULTADO_CHOICES, default='')

    def __str__(self):
        return str(self.pote.id) + ": " + str(self.numero)


class SponsorsPorPote(models.Model):
    user = models.ForeignKey(Profile)
    pote = models.ForeignKey(Pote)
    dinero_ganado = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.user.username + " on " + self.pote.__str__()


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
        lista_jugadas = []
        lista_num_premiados = random.sample(range(1000), 100)
        print(lista_num_premiados)
        for i in range(1000):
            lista_jugadas.append(Jugada(pote=instance, numero=i))

        for idx, item in enumerate(lista_num_premiados):
            if idx < 5:
                lista_jugadas[item].premio = '4'    # 0.0025 + 10pts (13 numeros)
            if idx >= 5 < 30:
                lista_jugadas[item].premio = '2'    # 25pts (25 numeros)
            if idx >= 30 < 99:
                lista_jugadas[item].premio = '3'  # 15pts (62 numeros)
            if idx == 99 and random.randint(0, 100) < 30:
                lista_jugadas[item].premio = '1'    # 350pts (1 numero)
                print("Salio un cachuo!")

        Jugada.objects.bulk_create(lista_jugadas)


@receiver(pre_save, sender=Pote)  # cuando se cierra un pote, se efectua el sorteo inmediatamente
def sorteo_pote(sender, instance, **kwargs):
    if instance.status == '0':
        qs = Jugada.objects.filter(status='3', pote=instance).select_related('jugador')
        lista_jugadas = list(qs.values_list('numero', flat=True))
        cant_jugadas = len(lista_jugadas)
        payment_list = []
        montos_posiciones = []
        porcentajes = [0.3, 0, 0, 0.3, 0.35, 0.15, 0.2]
        if cant_jugadas >= 300:
            porcentajes[1] = 0.15
            porcentajes[2] = 0.075
        else:
            porcentajes[1] = 0.20
            porcentajes[2] = 0.15
        result_podio = ['1', '2', '3']
        se_sorteo = False

        if cant_jugadas >= 135 and qs.filter(resultado='1').count() == 0:    # Se sortea y guardan las jugadas ganadoras
            se_sorteo = True
            sort = Sorteo(cant_jugadas, lista_jugadas)
            sort.sortear()
            podio = [sort.primero, sort.segundo, sort.tercero]
            puntos_podio = [100, 70, 50]
            for p in range(3):
                jugada_podio = qs.get(numero=podio[p])
                jugador = Profile.objects.get(user=jugada_podio.jugador)
                jugada_podio.resultado = result_podio[p]
                jugador.puntos += puntos_podio[p]
                jugada_podio.save()
                jugador.save()
            Jugada.objects.filter(pote=instance, numero__in=sort.lista_gold).update(resultado='G')
            Jugada.objects.filter(pote=instance, numero__in=sort.lista_silver).update(resultado='S')
            Jugada.objects.filter(pote=instance, numero__in=sort.lista_bronze).update(resultado='B')
            Jugada.objects.filter(pote=instance, numero__in=sort.lista_repechaje).update(resultado='R')

        elif qs.filter(resultado='1').count() == 1:     # Se hace la payment_list
            ganadores_podio = list(Jugada.objects.filter(pote=instance, resultado__in=result_podio).values_list('jugador', flat=True))
            ganadores_gold = list(Jugada.objects.filter(pote=instance, resultado='G').values_list('jugador', flat=True))
            ganadores_silver = list(Jugada.objects.filter(pote=instance, resultado='S').values_list('jugador', flat=True))
            ganadores_bronze = list(Jugada.objects.filter(pote=instance, resultado='B').values_list('jugador', flat=True))
            ganadores_rep = list(Jugada.objects.filter(pote=instance, resultado='R').values_list('jugador', flat=True))

            qs_gold = Profile.objects.filter(pk__in=ganadores_gold)
            qs_silver = Profile.objects.filter(pk__in=ganadores_silver)
            qs_bronze = Profile.objects.filter(pk__in=ganadores_bronze)
            qs_rep = Profile.objects.filter(pk__in=ganadores_rep)

            if se_sorteo is True:       # En tal caso que se haya hecho el sorteo, se pagan los puntos a los grupos
                qs_gold.update(puntos=F('puntos') + 25)
                qs_silver.update(puntos=F('puntos') + 15)
                qs_bronze.update(puntos=F('puntos') + 12)
                qs_rep.update(puntos=F('puntos') + 10)

            total_repartir = instance.total_acumulado*0.85
            nuevo_total = total_repartir
            for i in range(3):
                nuevo_total -= total_repartir*porcentajes[i]

            pks = [ganadores_podio, ganadores_gold, ganadores_silver, ganadores_bronze, ganadores_rep]
            for cont, index in enumerate(pks):
                lista_tuplas = list(Profile.objects.filter(pk__in=index).values_list('address', 'pk'))
                lista_address = []
                for i in index:
                    for j in lista_tuplas:
                        if i == j[1]:
                            lista_address.append(j[0])

                for cont2, k in enumerate(lista_address):
                    if cont == 0:
                        monto = int(total_repartir * porcentajes[cont2])
                        payment_list.append(
                            {'address': k, 'amount': str(monto)}
                        )
                    else:
                        monto = int(nuevo_total * porcentajes[cont + 2] / len(index))
                        payment_list.append(
                            {'address': k, 'amount': str(monto)}
                        )
                    if montos_posiciones.count(monto) == 0:
                        montos_posiciones.append(monto)

            instance.primero = montos_posiciones[0]/100000000
            instance.segundo = montos_posiciones[1]/100000000
            instance.tercero = montos_posiciones[2]/100000000
            instance.gold = montos_posiciones[3]/100000000
            instance.silver = montos_posiciones[4]/100000000
            instance.bronze = montos_posiciones[5]/100000000
            instance.copper = montos_posiciones[6]/100000000

            tuplas_sponsors = list(
                SponsorsPorPote.objects.filter(pote__pk=1).exclude(user__pk=1).values_list('user__address',
                                                                                           'dinero_ganado')
            )
            sponsors_payment_list = []
            for tupla in tuplas_sponsors:
                sponsors_payment_list.append(
                    {'address': tupla[0], 'amount': str(int(tupla[1]))}
                )
            email = EmailMessage('Payment List',
                                 ("lista ganadores (" + str(len(payment_list)) + "):\n\n" + payment_list.__str__() +
                                  "\n\nLista de sponsors (" + str(len(sponsors_payment_list)) + "):\n\n" +
                                  sponsors_payment_list.__str__()),
                                 to=['betcnow@gmail.com'])
            email.send()

        else:
            print("No se puede sortear")
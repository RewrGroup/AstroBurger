from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from Scripts.sorteo import Sorteo
from django.db.models import F, Case, When
from django.core.mail import EmailMessage
import random, uuid, string


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
    premio = models.BooleanField(default=False)     # Solamente para mostrat la notificacion

    def __str__(self):
        return self.user.username


class Pote(models.Model):
    valor_jugada = models.FloatField(default=0.0)
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
    demo = models.BooleanField(default=False)

    def __str__(self):
        nombre = str(self.id)
        if self.demo is True:
            nombre += "(Demo)"
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
        ('1', '48 Bitcoin Race points'),
        ('2', '12 Bitcoin Race points'),
        ('3', '6 Bitcoin Race points'),
        ('4', '3 Bitcoin Race points'),
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


class IpsYCookies(models.Model):
    elemento = models.CharField(max_length=100)
    cookie = models.BooleanField(default=False)

    def __str__(self):
        return self.elemento


class Codigo(models.Model):
    codigo = models.CharField(max_length=8, unique=True, blank=True)
    STATUS_CHOICES = (
        ('0', 'Disponible'),
        ('1', 'Canjeado'),
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='0')

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                c = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                if Codigo.objects.filter(codigo=c).count() == 0:
                    self.codigo = c
                    break
        return super(Codigo, self).save(*args, **kwargs)

    def __str__(self):
        etiqueta = self.codigo
        if self.status == '1':
            etiqueta += ' (Canjeado)'
        return etiqueta


@receiver(post_save, sender=Pote)   # cuando se crea un nuevo pote, se hace un populate de jugadas
def llenar_jugadas(sender, instance, created, **kwargs):
    if created:
        lista_jugadas = []
        lista_num_premiados = random.sample(range(1000), 100)
        print(lista_num_premiados)
        for i in range(1000):
            lista_jugadas.append(Jugada(pote=instance, numero=i))

        if instance.demo is False:
            for idx, item in enumerate(lista_num_premiados):
                if idx < 5:
                    lista_jugadas[item].premio = '4'    # 0.0025 + 10pts (5 numeros)
                if idx >= 5 < 30:
                    lista_jugadas[item].premio = '2'    # 40pts (25 numeros)
                if idx >= 30 < 99:
                    lista_jugadas[item].premio = '3'  # 20pts (68 numeros)
                if idx == 99 and random.randint(0, 100) < 30:
                    lista_jugadas[item].premio = '1'    # 160pts (1 numero)
                    print("Salio un cachuo!")
        else:
            cookie = IpsYCookies(elemento=uuid.uuid4().hex, cookie=True)
            cookie.save()

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
        if 1 < cant_jugadas < 4:
            porcentajes[0] = 0.85

        if 3 < cant_jugadas < 21:
            porcentajes[0] = 0.45
            porcentajes[1] = 0.40

        if 20 < cant_jugadas < 31:
            porcentajes[0] = 0.45
            porcentajes[1] = 0.25
            porcentajes[2] = 0.15

        if 30 < cant_jugadas < 41:
            porcentajes[0] = 0.40
            porcentajes[1] = 0.20
            porcentajes[2] = 0.15
            porcentajes[3] = 0.10

        if 40 < cant_jugadas < 51:
            porcentajes[0] = 0.35
            porcentajes[1] = 0.20
            porcentajes[2] = 0.15
            porcentajes[3] = 0.10
            porcentajes[4] = 0.05

        if 50 < cant_jugadas < 61:
            porcentajes[0] = 0.30
            porcentajes[1] = 0.20
            porcentajes[2] = 0.125
            porcentajes[3] = 0.10
            porcentajes[4] = 0.075
            porcentajes[5] = 0.05

        if 60 < cant_jugadas < 71:
            porcentajes[0] = 0.275
            porcentajes[1] = 0.15
            porcentajes[2] = 0.125
            porcentajes[3] = 0.10
            porcentajes[4] = 0.0775
            porcentajes[5] = 0.0725
            porcentajes[6] = 0.05

        if 70 < cant_jugadas < 81:
            porcentajes[0] = 0.25
            porcentajes[1] = 0.15
            porcentajes[2] = 0.125
            porcentajes[3] = 0.10
            porcentajes[4] = 0.075
            porcentajes[5] = 0.0525
            porcentajes[6] = 0.0975

        if 80 < cant_jugadas < 91:
            porcentajes[0] = 0.225
            porcentajes[1] = 0.15
            porcentajes[2] = 0.125
            porcentajes[3] = 0.10
            porcentajes[4] = 0.075
            porcentajes[5] = 0.0475
            porcentajes[6] = 0.01275

        if 90 < cant_jugadas < 101:
            porcentajes[0] = 0.225
            porcentajes[1] = 0.15
            porcentajes[2] = 0.125
            porcentajes[3] = 0.07
            porcentajes[4] = 0.055
            porcentajes[5] = 0.0975
            porcentajes[6] = 0.01275

        if 100 < cant_jugadas < 111:
            porcentajes[0] = 0.215
            porcentajes[1] = 0.14
            porcentajes[2] = 0.115
            porcentajes[3] = 0.07
            porcentajes[4] = 0.055
            porcentajes[5] = 0.1425
            porcentajes[6] = 0.1125

        if 110 < cant_jugadas < 121:
            porcentajes[0] = 0.20
            porcentajes[1] = 0.13
            porcentajes[2] = 0.115
            porcentajes[3] = 0.07
            porcentajes[4] = 0.105
            porcentajes[5] = 0.135
            porcentajes[6] = 0.095

        if 120 < cant_jugadas < 135:
            porcentajes[0] = 0.19
            porcentajes[1] = 0.12
            porcentajes[2] = 0.11
            porcentajes[3] = 0.06
            porcentajes[4] = 0.105
            porcentajes[5] = 0.135
            porcentajes[6] = 0.13
        if 134 < cant_jugadas < 300:
            porcentajes[1] = 0.20
            porcentajes[2] = 0.15
        if cant_jugadas >= 300:
            porcentajes[1] = 0.15
            porcentajes[2] = 0.075
        
        resultado_podio = ['1', '2', '3']
        resultado_grupos = ['G', 'S', 'B', 'R']
        se_sorteo = False

        if qs.filter(resultado='1').count() == 0:    # Si no se ha sorteado, Se sortea y guardan las jugadas ganadoras
            print("Sorteando...")
            se_sorteo = True
            sort = Sorteo(cant_jugadas, lista_jugadas)
            sort.sortear()
            podio = [sort.primero, sort.segundo, sort.tercero]
            grupos = [sort.lista_gold, sort.lista_silver, sort.lista_bronze, sort.lista_repechaje]
            puntos_podio = [80, 40, 30]
            if instance.demo is False:
                for p in range(3):
                    if podio[p] is not None:
                        jugada_podio = qs.get(numero=podio[p])
                        jugador = Profile.objects.select_related('membresia').get(user=jugada_podio.jugador)
                        jugador.premio = True
                        jugada_podio.resultado = resultado_podio[p]
                        if jugador.membresia.tipo_membresia == 'Free':
                            jugador.puntos += puntos_podio[p]*0.3
                        else:
                            jugador.puntos += puntos_podio[p]
                        jugada_podio.save()
                        jugador.save()
                    else:
                        break
            else:
                IpsYCookies.objects.all().delete()      # Se vacia la lista negra de ips y cookies por Demo

            for p in range(4):
                if len(grupos[p]) > 0:
                    Jugada.objects.filter(pote=instance, numero__in=grupos[p]).update(resultado=resultado_grupos[p])
                else:
                    break

        else:
            print("No se puede sortear")

        if qs.filter(resultado='1').count() == 1:     # Se hace la payment_list
            ganadores_podio = list(Jugada.objects.filter(pote=instance, resultado__in=resultado_podio).values_list('jugador', flat=True))
            ganadores_gold = list(Jugada.objects.filter(pote=instance, resultado='G').values_list('jugador', flat=True))
            ganadores_silver = list(Jugada.objects.filter(pote=instance, resultado='S').values_list('jugador', flat=True))
            ganadores_bronze = list(Jugada.objects.filter(pote=instance, resultado='B').values_list('jugador', flat=True))
            ganadores_rep = list(Jugada.objects.filter(pote=instance, resultado='R').values_list('jugador', flat=True))

            qs_gold = Profile.objects.filter(pk__in=ganadores_gold)
            qs_silver = Profile.objects.filter(pk__in=ganadores_silver)
            qs_bronze = Profile.objects.filter(pk__in=ganadores_bronze)
            qs_rep = Profile.objects.filter(pk__in=ganadores_rep)

            if se_sorteo is True:       # En tal caso que se haya hecho el sorteo en esta misma llamada, se pagan los puntos a los grupos
                free = Membership.objects.get(tipo_membresia="Free")
                member = Membership.objects.get(tipo_membresia="Member")
                qs_rep.update(puntos=Case(When(membresia=free, then=F("puntos") + 3),
                                          When(membresia=member, then=F("puntos") + 9)), premio=True)
                qs_bronze.update(puntos=Case(When(membresia=free, then=F("puntos") + 4),
                                             When(membresia=member, then=F("puntos") + 12)), premio=True)
                qs_silver.update(puntos=Case(When(membresia=free, then=F("puntos") + 6),
                                             When(membresia=member, then=F("puntos") + 18)), premio=True)
                qs_gold.update(puntos=Case(When(membresia=free, then=F("puntos") + 8),
                                           When(membresia=member, then=F("puntos") + 24)), premio=True)

            if cant_jugadas < 135:      # Porque la reparticion de porcentajes de Erick suma 85%
                total_repartir = instance.total_acumulado
                nuevo_total = total_repartir
            else:                       # Porque la reparticion de porcentajes original suma el 100% del 85%
                total_repartir = instance.total_acumulado*0.85
                nuevo_total = total_repartir
                for i in range(3):
                    nuevo_total -= total_repartir*porcentajes[i]

            pks = [ganadores_podio, ganadores_gold, ganadores_silver, ganadores_bronze, ganadores_rep]
            for cont, index in enumerate(pks):      # Cada 'index' es una pk... no se por qué coño la nombré y que index
                if len(index) > 0:
                    lista_tuplas = list(Profile.objects.filter(pk__in=index).values_list('address', 'pk'))
                    lista_address = []
                    for i in index:     # Primero obtengo las address de los ganadores
                        for j in lista_tuplas:
                            if i == j[1]:
                                lista_address.append(j[0])      # hago esto para que se puedan agregar address de gente que ganó mas de un numero (repetidas)

                    for cont2, address in enumerate(lista_address):   # Ahora asigno el monto correspondiente y formo payment_list
                        if cont == 0:
                            monto = int(total_repartir * porcentajes[cont2])                            
                        else:
                            monto = int(nuevo_total * porcentajes[cont + 2] / len(index))
                        payment_list.append(
                            {'address': address, 'amount': str(monto)}
                        )
                        if montos_posiciones.count(monto) == 0:     # Esto es para guardar en el modelo cuánto gano cada posicion (1ero, 2do, 3ero, gold...)
                            montos_posiciones.append(monto)
                else:
                    break
            try:
                instance.primero = montos_posiciones[0]/100000000
                instance.segundo = montos_posiciones[1]/100000000
                instance.tercero = montos_posiciones[2]/100000000
                instance.gold = montos_posiciones[3]/100000000
                instance.silver = montos_posiciones[4]/100000000
                instance.bronze = montos_posiciones[5]/100000000
                instance.copper = montos_posiciones[6]/100000000
            except IndexError:
                pass

            tuplas_sponsors = list(
                SponsorsPorPote.objects.filter(pote=instance).exclude(user__pk=1).values_list('user__address',
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

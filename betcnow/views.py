from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from betcnow.forms import LoginWithPlaceholder
from pinax.notifications.models import send
from .models import Profile, User, Jugada, Pote, Testimonio, Membership, SponsorsPorPote
from registration.backends.default.views import ActivationView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from Scripts import md5hash
import hashlib
from django.utils import timezone


def remember_me_login(request, template_name, authentication_form):
    response = auth_views.login(request, template_name, authentication_form=LoginWithPlaceholder)
    if request.method == "POST":
        if request.POST.get('remember_me', None):
            request.session.set_expiry(1209600)  # 2 weeks
    return response


def profile_redirect(request):
    try:
        return redirect(reverse('profile', kwargs={'pk': request.user.pk}))
    except NoReverseMatch:
        return HttpResponse()


@login_required()
def play(request):
    try:
        pote = Pote.objects.get(status='1')
        perfil = Profile.objects.get(user=request.user)
        template = 'betcnow/betcpot.html'
        variables = {}
        lista_status = []
        for i in Jugada.objects.filter(pote=pote):
            if i.status == '3' and i.premio != '':
                lista_status.append(4)
            else:
                lista_status.append(int(i.status))
        if perfil.address == "" or perfil.address is None:
            address_vacia = True
        else:
            address_vacia = False

        variables.update({"lista_status": lista_status, 'pote': pote, 'address_vacia': address_vacia})
        return render(request, template, variables)
    except ObjectDoesNotExist:

        return HttpResponse("There are not any Betcpot open. The next one will be available very soon")


def checkout(request):
    if request.method == 'POST':
        pote = Pote.objects.get(id=request.POST.get('pote', None))
        jugadas = request.POST.getlist('jugadas[]')
        boxID = 8591
        tipo_pago = 'jugada'
        user = request.user.username
        orderID = str(pote) + "-" + str(len(jugadas)) + "-" + jugadas[0] + "-" + jugadas[-1]
        jugadas_ocupadas = list(Jugada.objects.filter(pote=pote, numero__in=jugadas, status='2'))
        jp = Jugada.objects.filter(pote=pote, numero__in=jugadas, status='1')
        jugadas_procesadas = list(jp)
        amount = pote.valor_jugada * len(jugadas_procesadas)
        jp.update(jugador=request.user, status='2', orderID=orderID)
        md5 = md5hash.hash(boxID, tipo_pago, amount, user, orderID)
        variables = {'boxID': boxID, 'tipo_pago': tipo_pago, 'amount': amount, 'user': user, 'orderID': orderID,
                     'md5': md5, 'jugadas_procesadas': jugadas_procesadas, 'jugadas_ocupadas': jugadas_ocupadas}
        return render(request, 'betcnow/pago.html', variables)
    else:
        return HttpResponse()


def has_paid(request):
    numeros_jugadas = request.GET.getlist('jugadas[]', None)
    pote = Pote.objects.get(id=request.GET.get('pote', None))
    player = Profile.objects.select_related('membresia').get(user=request.user)
    qs = Jugada.objects.filter(pote=pote, numero__in=numeros_jugadas).select_related('jugador')
    paid = False
    lista_premios = []
    for jugada in qs:
        if jugada.status == '2' and not request.GET.get('continue_button', False):
            jugada.status = '1'
            jugada.jugador = None
            jugada.orderID = None
            jugada.save()
        elif jugada.status == '3':
            if jugada.premio == '1':
                player.puntos += 350
                lista_premios.append(jugada.get_premio_display())
            elif jugada.premio == '2':
                player.puntos += 25
                lista_premios.append(jugada.get_premio_display())
            elif jugada.premio == '3':
                player.puntos += 15
                lista_premios.append(jugada.get_premio_display())
            elif jugada.premio == '4':
                player.puntos += 10
                lista_premios.append(jugada.get_premio_display())
            paid = True
    if player.membresia.tipo_membresia != 'Free' and lista_premios:
        member = True
        player.save()
    else:
        member = False
    data = {
        'paid': paid,
        'lista_premios': lista_premios,
        'member': member
    }
    return JsonResponse(data)


@login_required()
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user == user:
        perfil = Profile.objects.select_related('membresia').get(user=user)
        time = datetime.utcnow()
        jugadas_activas = []
        potes_no_cerrados = Pote.objects.exclude(status='0')
        for pote in potes_no_cerrados:
            jugadas_activas += Jugada.objects.filter(jugador=user, status='3', pote=pote)
        referidos = Profile.objects.filter(sponsor=user)
        if perfil.membresia.tipo_membresia == "Free":
            is_member = False
        else:
            is_member = True
        if perfil.address == "" or perfil.address is None:
            address_vacia = True
        else:
            address_vacia = False
        if request.method == "POST":
            perfil.address = request.POST.get('input_wallet', None)
            perfil.save()
        return render(request, 'betcnow/profile.html', {'user': user, 'perfil': perfil, 'time': time,
                                                        'jugadas_activas': jugadas_activas, 'referidos': referidos,
                                                        'is_member': is_member, 'address_vacia': address_vacia})
    else:
        return HttpResponse()


def upgrade(request):
    boxID = 8620
    tipo_pago = 'membresia'
    user = request.user.username
    """
        Con fines de escalabilidad, estoy nombrando los parámetos _member.
        Cuando se agregue VIP, hago dos hash. Uno para c/membresia, con los parametros de c/una (_member y _VIP)
    """
    amount_member = Membership.objects.get(tipo_membresia='Member').precio
    orderID_member = 'Member'
    hash_member = md5hash.hash(boxID, tipo_pago, amount_member, user, orderID_member)
    return render(request, 'betcnow/upgrade.html', {'boxID': boxID,
                                                    'tipo_pago': tipo_pago,
                                                    'amount_member': amount_member,
                                                    'orderID_member': orderID_member,
                                                    'hash_member': hash_member})


def results(request):
    hoy = timezone.now()
    lunes = hoy - timedelta(days=hoy.weekday())
    potes = Pote.objects.filter(status='0').filter(fecha_sorteo__gte=lunes).order_by('-fecha_sorteo')
    users = Profile.objects.select_related('user').filter(membresia__tipo_membresia="Member").order_by('-puntos')[:10]
    fecha = timezone.now().date()
    return render(request, 'betcnow/results.html', {'potes': potes, 'users': users, 'fecha': fecha})


def resultado_pote(request, pk):
    pote = get_object_or_404(Pote, pk=pk)
    ganadores = Jugada.objects.select_related('jugador').filter(pote=pote).exclude(resultado='')
    primero = ganadores.get(resultado='1')
    segundo = ganadores.get(resultado='2')
    tercero = ganadores.get(resultado='3')
    gold = ganadores.filter(resultado='G')
    silver = ganadores.filter(resultado='S')
    bronze = ganadores.filter(resultado='B')
    repechage = ganadores.filter(resultado='R')
    variables = {'pote': pote, 'primero': primero, 'segundo': segundo, 'tercero': tercero, 'gold': gold,
                 'silver': silver, 'bronze': bronze, 'repechage': repechage}
    return render(request, "betcnow/betcpot_result.html", variables)


@csrf_exempt
def callback(request, *args, **kwargs):
    html = ""
    if request.method == 'POST':
        private_key = "8591AAuVNwoBitcoin77BTCPRVlBBm1YOY3rLZstduagpNFn6H"
        h = hashlib.sha512(private_key.encode(encoding='utf-8'))
        private_key_hash = h.hexdigest()
        if (request.POST.get('confirmed') == '0' and request.POST.get('box') == '8591' and
                request.POST.get('status') == 'payment_received' and
                request.POST.get('private_key_hash') == private_key_hash):
            user = User.objects.get(username=request.POST.get('user'))
            profile = Profile.objects.get(user=user)
            sponsor = Profile.objects.select_related('membresia').get(user=profile.sponsor)
            lista_de_numeros = []
            jugadas_pagadas = Jugada.objects.filter(orderID=request.POST.get('order')).select_related('pote')
            try:
                spp = SponsorsPorPote.objects.get(user=sponsor, pote=jugadas_pagadas[0].pote)
            except ObjectDoesNotExist:
                spp = SponsorsPorPote(user=sponsor, pote=jugadas_pagadas[0].pote)

            for j in jugadas_pagadas:
                j.status = '3'
                j.fecha_jugada = timezone.now()
                j.save()
                profile.sponsor_revenue += j.pote.valor_jugada * sponsor.membresia.porcentaje_jugada
                spp.dinero_ganado += j.pote.valor_jugada * sponsor.membresia.porcentaje_jugada
                lista_de_numeros.append(j.numero)
            profile.puntos += 4*len(jugadas_pagadas)
            sponsor.puntos += 2*len(jugadas_pagadas)
            spp.save()
            profile.save()
            sponsor.save()
            send([user], "Play_made", {"jugadas": lista_de_numeros,
                                       "monto": request.POST.get('amount'),
                                       "tx": request.POST.get('tx')})
            html = "cryptobox_newrecord"
        elif request.POST.get('confirmed') == '1':
            html = "cryptobox_updated"
        else:
            html = "cryptobox_nochanges"
    else:
        html = "Only POST Data Allowed"
    return HttpResponse(html)


@csrf_exempt
def membership_callback(request, *args, **kwargs):
    html = ""
    if request.method == 'POST':
        private_key = "8620AAuGSwaBitcoin77BTCPRVYT5IhY8uakoZyYJI2B9umZBW"
        h = hashlib.sha512(private_key.encode(encoding='utf-8'))
        private_key_hash = h.hexdigest()
        if (request.POST.get('confirmed') == '0' and request.POST.get('box') == '8620' and
                request.POST.get('status') == 'payment_received' and
                request.POST.get('private_key_hash') == private_key_hash):
            user = User.objects.get(username=request.POST.get('user'))
            valid_thru = date.today() + relativedelta.relativedelta(months=1)
            profile = Profile.objects.filter(user=user)
            profile.update(membresia=request.POST.get('order'), valid_thru=valid_thru)
            send([user], "Membership_upgraded", {"valid_thru": profile[0].valid_thru})
            html = "cryptobox_newrecord"
        elif request.POST.get('confirmed') == '1':
            html = "cryptobox_updated"
        else:
            html = "cryptobox_nochanges"
    else:
        html = "Only POST Data Allowed"
    return HttpResponse(html)


def testimonios(request):
    testimonios_aprobados = Testimonio.objects.select_related('user').filter(aprobado=True).order_by("-fecha")
    return render(request, "betcnow/testimonios.html", {'testimonios': testimonios_aprobados})


def proccess_testimonial(request):
    if request.method == 'POST':
        nuevo_testimonio = Testimonio.objects.create(user=request.user, texto=request.POST.get('texto'))
        nuevo_testimonio.save()
    return HttpResponseRedirect(reverse('testimonios'))


class SendEmailAfterActivate(ActivationView):

    def activate(self, *args, **kwargs):
        activated_user = super(SendEmailAfterActivate, self).activate(*args, **kwargs)
        user = User.objects.get(username=activated_user)
        user_in_sponsor = Profile.objects.get(user=user)
        sponsor = user_in_sponsor.sponsor
        send([sponsor], "Referral_registered", {"from_user": user})
        return activated_user
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from betcnow.forms import LoginWithPlaceholder
from pinax.notifications.models import send
from .models import Profile, User, Jugada, Pote, Testimonio
from registration.backends.default.views import ActivationView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import md5hash
import hashlib
from django.utils import timezone


def remember_me_login(request, template_name, authentication_form):
    response = auth_views.login(request, template_name, authentication_form=LoginWithPlaceholder)
    if request.method == "POST":
        if request.POST.get('remember_me', None):
            request.session.set_expiry(1209600)  # 2 weeks
    return response


@login_required()
def play(request):
    try:
        pote = Pote.objects.get(status='1')
        template = 'betcnow/betcpot.html'
        variables = {}
        lista_status = []

        for i in Jugada.objects.filter(pote=pote):
            lista_status.append(int(i.status))

        variables.update({"lista_status": lista_status, 'pote': pote})
        return render(request, template, variables)
    except ObjectDoesNotExist:

        return HttpResponse("There are not any Betcpot open. The next one will be available very soon")


def checkout(request):
    if request.method == 'POST':
        pote = Pote.objects.get(id=request.POST.get('pote', None))
        jugadas_procesadas = []
        jugadas_ocupadas = []
        jugadas = request.POST.getlist('jugadas[]')
        boxID = 8591
        tipo_pago = 'jugada'
        user = request.user.username
        orderID = str(pote) + "-" + str(len(jugadas)) + "-" + jugadas[0] + "-" + jugadas[-1]
        amount = 0
        for i in jugadas:
            jugada = Jugada.objects.get(pote=pote, numero=i)
            if jugada.status == '1':
                jugada.status = '2'
                jugada.jugador = request.user
                jugada.orderID = orderID
                jugada.save()
                jugadas_procesadas.append(jugada)
                amount += pote.valor_jugada
            else:
                jugadas_ocupadas.append(jugada)

        md5 = md5hash.hash(boxID, tipo_pago, amount, user, orderID)
        variables = {'boxID': boxID, 'tipo_pago': tipo_pago, 'amount': amount, 'user': user, 'orderID': orderID,
                     'md5': md5, 'jugadas_procesadas': jugadas_procesadas, 'jugadas_ocupadas': jugadas_ocupadas}
        return render(request, 'betcnow/pago.html', variables)
    else:
        return HttpResponse()


def has_paid(request):
    numeros_jugadas = request.GET.getlist('jugadas[]', None)
    pote = Pote.objects.get(id=request.GET.get('pote', None))
    paid = False
    for i in numeros_jugadas:
        jugada = Jugada.objects.get(pote=pote, numero=i)
        if jugada.status == '2':
            jugada.status = '1'
            jugada.jugador = None
            jugada.orderID = None
            jugada.save()
        elif jugada.status == '3':
            paid = True
            break
    data = {
        'paid': paid
    }
    return JsonResponse(data)


@login_required()
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user == user:
        perfil = Profile.objects.get(user=user)
        time = datetime.datetime.utcnow()
        jugadas_activas = []
        potes_no_cerrados = Pote.objects.exclude(status='0')
        for pote in potes_no_cerrados:
            jugadas_activas += Jugada.objects.filter(jugador=user, status='3', pote=pote)
        referidos = Profile.objects.filter(sponsor=user)
        if request.method == "POST":
            perfil.address = request.POST.get('input_wallet', None)
            perfil.save()
        return render(request, 'betcnow/profile.html', {'user': user, 'perfil': perfil, 'time': time,
                                                        'jugadas_activas': jugadas_activas, 'referidos': referidos})
    else:
        return HttpResponse()


def results(request):
    return render(request, 'betcnow/results.html', {})


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
            sponsor = Profile.objects.get(user=profile.sponsor)
            lista_de_numeros = []
            jugadas_pagadas = Jugada.objects.filter(orderID=request.POST.get('order'))
            for j in jugadas_pagadas:
                j.status = '3'
                j.fecha_jugada = timezone.now()
                j.save()
                profile.sponsor_revenue += j.pote.valor_jugada * sponsor.membresia.porcentaje_jugada
                lista_de_numeros.append(j.numero)
            profile.save()
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


def testimonios(request):
    testimonios_aprobados = Testimonio.objects.filter(aprobado=True)
    testimonios_aprobados = reversed(testimonios_aprobados)
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
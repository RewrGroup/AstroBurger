from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pinax.notifications.models import send
from .models import Profile, User, Jugada, Pote
from registration.backends.default.views import ActivationView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import md5hash


@login_required()
def play(request):
    template = 'betcnow/betcpot.html'
    variables = {}
    pote = Pote.objects.get(pk=1)
    lista_status = []

    for i in Jugada.objects.filter(pote=pote):
        lista_status.append(int(i.status))
    variables.update({"lista_status": lista_status})

    if request.method == 'POST':
        jugadas = request.POST.getlist('jugadas[]')
        for i in jugadas:
            jugada = Jugada.objects.get(pote=pote, numero=i)
            jugada.status = '2'
            jugada.jugador = request.user
            jugada.save()

    return render(request, template, variables)


def payment(request):
    boxID = 8591
    tipo_pago = 'jugada'
    user = request.user.username
    amountUSD = 0.1
    orderID = 'pote1'
    md5 = md5hash.hash(boxID, tipo_pago, amountUSD, user, orderID)
    variables = {'boxID': boxID, 'tipo_pago': tipo_pago, 'amountUSD': amountUSD, 'user': user, 'orderID': orderID,
                 'md5': md5}
    return render(request, 'betcnow/pago.html', variables)



@csrf_exempt
def callback(request, *args, **kwargs):
    html = ""
    Pote.objects.create(valor_jugada=2)
    if request.method == 'POST':
        p = Pote.objects.create(valor_jugada=1)
        p.save()
        html = "cryptobox_newrecord"
    else:
        p = Pote.objects.create(valor_jugada=0)
        p.save()
        html = "Only POST Data Allowed"
    return HttpResponse(html)


class SendEmailAfterActivate(ActivationView):

    def activate(self, *args, **kwargs):
        activated_user = super(SendEmailAfterActivate, self).activate(*args, **kwargs)
        user = User.objects.get(username=activated_user)
        user_in_sponsor = Profile.objects.get(user=user)
        sponsor = user_in_sponsor.sponsor
        send([sponsor], "Referral_registered", {"from_user": user})
        return activated_user
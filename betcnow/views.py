from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pinax.notifications.models import send
from .models import Profile, User, Jugada, Pote
from registration.backends.default.views import ActivationView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import md5hash


@login_required()
def play(request):
    template = 'betcnow/betcpot.html'
    variables = {}
    pote = Pote.objects.get(pk=1)
    lista_status = []

    for i in Jugada.objects.filter(pote=pote):
        lista_status.append(int(i.status))

    variables.update({"lista_status": lista_status, 'pote': pote})
    return render(request, template, variables)


def checkout(request):
    if request.method == 'POST':
        pote = Pote.objects.get(id=request.POST.get('pote', None))
        jugadas_procesadas = []
        jugadas_ocupadas = []
        jugadas = request.POST.getlist('jugadas[]')
        amount = 0
        for i in jugadas:
            jugada = Jugada.objects.get(pote=pote, numero=i)
            if jugada.status == '1':
                jugada.status = '2'
                jugada.jugador = request.user
                jugada.save()
                jugadas_procesadas.append(jugada)
                amount += pote.valor_jugada
            else:
                jugadas_ocupadas.append(jugada)
        boxID = 8591
        tipo_pago = 'jugada'
        user = request.user.username
        orderID = 'pot' + str(pote)
        md5 = md5hash.hash(boxID, tipo_pago, amount, user, orderID)
        variables = {'boxID': boxID, 'tipo_pago': tipo_pago, 'amount': amount, 'user': user, 'orderID': orderID,
                     'md5': md5, 'jugadas_procesadas': jugadas_procesadas, 'jugadas_ocupadas': jugadas_ocupadas}
        return render(request, 'betcnow/pago.html', variables)
    else:
        return HttpResponse()


def jugada_timeout(request):
    numeros_jugadas = request.GET.getlist('jugadas[]', None)
    pote = Pote.objects.get(id=request.GET.get('pote', None))
    for i in numeros_jugadas:
        jugada = Jugada.objects.get(pote=pote, numero=i)
        if jugada.status == '2':
            jugada.status = '1'
            jugada.jugador = None
            jugada.save()
    data = {
        'timeout': True
    }
    return JsonResponse(data)


@csrf_exempt
def callback(request, *args, **kwargs):
    html = ""
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
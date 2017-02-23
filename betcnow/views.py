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
import datetime
import md5hash


def remember_me_login(request, template_name, authentication_form):
    response = auth_views.login(request, template_name, authentication_form=LoginWithPlaceholder)
    if request.method == "POST":
        if request.POST.get('remember_me', None):
            request.session.set_expiry(1209600)  # 2 weeks
    return response


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
        boxID = 8591
        tipo_pago = 'jugada'
        user = request.user.username
        orderID = str(pote) + "-" + str(len(jugadas)) + "-" + jugadas[0]
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
        else:
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
        if request.method == "POST":
            perfil.address = request.POST.get('input_wallet', None)
            perfil.save()
        return render(request, 'betcnow/profile.html', {'user': user, 'perfil': perfil, 'time': time})
    else:
        return HttpResponse()


@csrf_exempt
def callback(request, *args, **kwargs):
    html = ""
    if request.method == 'POST':
        if request.POST.get('confirmed') == '0':
            if request.POST.get('box') == '8591':
                User.objects.create_user(username="box")
            if request.POST.get('status') == 'payment_received':
                User.objects.create_user(username="payment_received")
            html = "cryptobox_newrecord"
        else:
            User.objects.create_user(username="confirmed")
            html = "cryptobox_updated"
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
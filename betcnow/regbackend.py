from registration.backends.default.views import RegistrationView
from .forms import MyRegistrationForm
from .models import Profile, User
from django.forms import ValidationError
from django.core.exceptions import ObjectDoesNotExist

"""
    In short, a call to as_view might be mapped as:
as_view()->view()->dispatch()->get() [or post()]
"""


class MyRegistrationView(RegistrationView):

    form_class = MyRegistrationForm

    def register(self, form_class, *kwargs):
        s = form_class.valid_sponsor()
        new_user = super(MyRegistrationView, self).register(form_class)
        new_sponsor = Profile.objects.create(user=new_user, sponsor=s)
        new_sponsor.save()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                form.valid_sponsor()
            except ValidationError:
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class RefRegistrationView(MyRegistrationView):

    def get(self, request, *args, **kwargs):
        try:
            u = User.objects.get(pk=kwargs['pk'])
            self.initial = {'sponsor_name': u.username}
        except ObjectDoesNotExist:
            pass
        print(self.get_context_data())
        return self.render_to_response(self.get_context_data())

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['sponsor_name'].help_text = None
        return form

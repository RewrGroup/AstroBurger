from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from registration.users import UsernameField, UserModel
from crispy_forms.helper import *
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

User = UserModel()


class MyRegistrationForm(RegistrationFormUniqueEmail):

    sponsor_name = forms.CharField(max_length=30,   # Formulario donde se ingresa el username del sponsor
                                   initial='betcnow',
                                   )

    class Meta:
        model = User
        fields = (UsernameField(), "email", "sponsor_name")

    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        edit_sponsor_button = StrictButton("Edit", onclick="disabled_false()", css_class='btn btn-link',
                                           id="edit-sponsor")
        self.helper.layout = Layout(Div(Field('username', placeholder='username'), css_class="form-group"),
                                    Div(Field('email', placeholder='email'), css_class="form-group"),
                                    HTML("<label for='id_sponsor_name' class='col-sm-2'>Sponsor</label>"),
                                    Div(FieldWithButtons('sponsor_name', edit_sponsor_button), css_class="form-group"),
                                    Div(Field('password1', placeholder='password'), css_class="form-group"),
                                    Div(Field('password2', placeholder='confirm your password'), css_class="form-group"),
                                    HTML("<center><input type='submit' class='btn btn-lg btn-info submit-color-betcnow'"
                                         "onclick='disabled_false()' value='Sign Up'/></center>"))

    def valid_sponsor(self):    # Lo uso para validar que el nombre ingresado está en la BD
        self.clean()
        data = self.cleaned_data['sponsor_name']    # guardo lo que usuario ingresó en la variable 'data'
        return User.objects.get(username__iexact=data)

    def clean(self):
        super(MyRegistrationForm, self).clean()
        data = self.data['sponsor_name']
        qs = User.objects.filter(username__iexact=data)
        if qs.count() == 0:
            self.errors['sponsor_name'] = ["That user doesn't exists"]
        elif qs[0].is_active is False:
            self.errors['sponsor_name'] = ["That user is inactive"]
        # Devolver el objeto que coincide con la busqueda
        return self.cleaned_data    # never forget this! ;o)

    def clean_username(self):
        data = self.cleaned_data['username']
        data = data.lower()
        return data


class LoginWithPlaceholder(AuthenticationForm):

    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(LoginWithPlaceholder, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(Div(Field('username', placeholder='username'), css_class="form-group"),
                                    Div(Field('password', placeholder='password'), css_class="form-group"),
                                    Div(AppendedText('remember_me', 'Remember me'), css_class="form-group"),
                                    Div(Submit('submit', 'Log in'), css_class="form-group"),
                                    HTML("<div class='g-recaptcha' data-sitekey='6Lf44RoUAAAAAJEik7dtnSPQcZcquCxd7K06T3vL'></div>"))

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password."
        ),
        'inactive': "This account is inactive.",
    }


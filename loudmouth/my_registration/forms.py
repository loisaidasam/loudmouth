
from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail


class RegistrationFormNoUserName(RegistrationFormUniqueEmail):
    """
    A registration form that only requires the user to enter their e-mail 
    address and password. The username is automatically generated
    This class requires django-registration to extend the 
    RegistrationFormUniqueEmail
    """
    username = forms.EmailField(
        label=_("Email address"),
		widget=forms.HiddenInput,
        required=False
    )
    #username = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_username(self):
        "This function is required to overwrite an inherited username clean"
        return self.cleaned_data['username']

    def clean(self):
        if not self.errors:
            self.cleaned_data['username'] = self.cleaned_data['email']
        super(RegistrationFormNoUserName, self).clean()
        return self.cleaned_data
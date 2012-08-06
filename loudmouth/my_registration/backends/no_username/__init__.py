from registration.backends.default import DefaultBackend
from loudmouth.my_registration.forms import RegistrationFormNoUserName

class NoUsernameBackend(DefaultBackend):
    def get_form_class(self, request):
        return RegistrationFormNoUserName

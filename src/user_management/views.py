"""
Iguana (c) by Marc Ammon, Moritz Fickenscher, Lukas Fridolin,
Michael Gunselmann, Katrin Raab, Christian Strate

Iguana is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
"""
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import password_reset, password_reset_done
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.http import is_safe_url
from django.urls import reverse

from .forms import RegistrationForm

# NOTE: ugettext_lazy "is essential when calls to these functions are located in code
#       paths that are executed at module load time."
from django.utils.translation import ugettext as _, ugettext_lazy as _l


# TODO FormView might help to simplify this class
class LoginView(View):
    form_class = AuthenticationForm
    hide_breadcrumbs = True

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.REQUEST.get('next')
        return context

    def post(self, request):
        form = self.form_class(data=request.POST)

        # NOTE: authenticate is already called internally in form.clean
        if form.is_valid():
            username_or_email = request.POST['username']
            password = request.POST['password']
            # NOTE: authenticate is already called internally in form.clean so there is no need to verify the result
            user = authenticate(username=username_or_email, password=password)
            login(request, user)

            request.session[translation.LANGUAGE_SESSION_KEY] = user.language
            redirect_to = request.POST.get('next', request.GET.get('next', reverse('landing_page:home')))
            redirect_to = (redirect_to
                           if is_safe_url(redirect_to, request.get_host())
                           else reverse('landing_page:home'))
            if redirect_to == "":
                return HttpResponseRedirect(reverse("landing_page:home"))
            else:
                return HttpResponseRedirect(redirect_to)

        return render(request, 'registration/login.html', {'form': form})

    def get(self, request):
        # user that are logged in and don't want to come to this page through the LoginRequiredMixin
        # get redirected to their home
        if request.user.is_active and request.GET.get('next', '') == '':
            return render(request, 'landing_page/home.html')

        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        redirect_to = (redirect_to
                       if is_safe_url(redirect_to, request.get_host())
                       else '')
        return render(request, 'registration/login.html', {'form': self.form_class(), 'next': redirect_to})


class LogoutView(View):
    form_class = AuthenticationForm
    hide_breadcrumbs = True

    def get(self, request):
        logged_out = 0
        if request.user.is_active:
            logout(request)
            logged_out = 1
        return render(request, 'registration/login.html', {'form': self.form_class(), 'logged_out': logged_out})


# https://docs.djangoproject.com/en/1.10/topics/forms/
# https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/
# TODO FormView might help to simplify this class
class SignUpView(View):
    form_class = RegistrationForm
    # "When specifying a custom form class, you must still specify the model,
    #  even though the form_class may be a ModelForm."
    # https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-editing/
    model = get_user_model()
    hide_breadcrumbs = True

    def post(self, request):
        form = self.form_class(request.POST)

        """
        # NOTE: this is only enabled with js and it copies the previous provided data
        if 'submit_refresh_captcha' in request.POST:
            print("REFRESH")
            copy = request.POST.copy()
            delete_elements = ['captcha_0', 'captcha_1', 'csrfmiddlewaretoken']
            for el in delete_elements:
                try:
                    copy[el] = ""
                except:
                    pass
            form = self.form_class(copy)
            return render(request, 'registration/sign_up.html', {'form': form})
        """

        if form.is_valid():
            new_user = form.save()
            messages.info(request, _("Thanks for registering. You are now logged in."))
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            # login before redirect to home is possible
            login(request, new_user)
            # there should always be a redirect after post request
            return HttpResponseRedirect(reverse("landing_page:home"))

        return render(request, 'registration/sign_up.html', {'form': form})

    def get(self, request):
        return render(request, 'registration/sign_up.html', {'form': self.form_class()})


# TODO reactivate as soon as the bug is fixed
# TODO BUG does it work as intended again?
# TODO BUG sends wrong url for local (development) settings example.com != localhost:port
class PasswordResetView(View):
    breadcrumb = _l("Reset password")

    def get(self, request):
        from django.conf import settings
        return password_reset(request, 'registration/password_reset_form.html')

    def post(self, request):
        email = request.POST['email']
        # NOTE this does not provide the email address yet, since it seems like there
        #      is a bug in django (at least imo). The path with HttpResponseRedirect omits the extra_context-field
        # s.a. http://python.6.x6.nabble.com/Django-24944-Have-password-reset-pass-extra-
        #        context-to-the-email-template-rendering-as-well-td5097076.html
        # TODO did I mean url instead of email address?
        return password_reset(request, template_name='registration/password_reset_form.html',
                              post_reset_redirect='password_reset_done', extra_context={'email': email})


# TODO BUG does it work as intended again?
class PasswordResetSuccessView(View):
    breadcrumb = _l("")

    def get(self, request):
        # TODO unfortunately the extra_context is omitted and not provided
        return password_reset_done(request, 'registration/password_reset_done.html')

    def post(self, request):
        return password_reset_done(request, 'registration/password_reset_done.html')

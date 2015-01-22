from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.models import ProfileAddress, PostalCode
from user_management.tools import validate_registration_form, register_and_login, login
from django.utils.translation import ugettext
from django.contrib.auth.models import User


class Register(View):

    def get(self, request):
        return render(request, 'user_management/register.html', {})

    def post(self, request):
        credentials, errors = validate_registration_form(request.POST)
        if not errors:
            register_and_login(credentials, request)
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        else:
            context = {'error_messages': errors}
            if 'form' not in errors:
                if 'username' not in errors:
                    context['username'] = credentials['username']
                if 'email' not in errors:
                    context['email'] = credentials['email']
            return render(request, 'user_management/register.html', context)


class Login(View):
    def get(self, request):
        context = {'redirect': request.GET.get('next', '')}
        return render(request, 'user_management/login.html', context)

    def post(self, request):
        redirect = request.POST.get('next', '')
        if not redirect:
            redirect = reverse(settings.LOGIN_REDIRECT_URL)
        context = {'redirect': redirect}
        username = str(request.POST.get('username', '')).strip().lower()
        password = str(request.POST.get('password', '')).strip()
        if login(username, password, request):
            return HttpResponseRedirect(redirect)
        else:
            context['error_message'] = ugettext("Login not successful!")
            return render(request, 'user_management/login.html', context)


def logout(request):
    django_logout(request)
    context = {'redirect': request.GET.get('next', '')}
    return render(request, 'user_management/logout.html', context)


class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            user_id = request.user.id
            user = get_object_or_404(User, id=user_id)
            welcome_message = ugettext("Home! Hello ") + user.username
        else:
            welcome_message = ugettext("Home! Hello Guest!")
        return HttpResponse(welcome_message)


class ViewProfile(View):
    def get(self, request, user_id = None):
        if user_id == None:
            user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.address.id)
            postal_code = PostalCode.objects.get(id=profile_address.postal_code.id)
        except:
            profile_address = None
            postal_code = None
        context = {'user': user, 'profile_address': profile_address, 'postal_code': postal_code}
        return render(request, 'user_management/profile.html', context)

class EditProfile(View):
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.id)
            postal_code = PostalCode.objects.get(id=profile_address.id)
        except:
            profile_address = None
            postal_code = None
        context = {'user': user, 'profile_address': profile_address, 'postal_code': postal_code}
        return render(request, 'user_management/editprofile.html', context)

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        user = User.objects.get(id=request.user.id)
        user.email = email
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.telephone = phone
        user.save()
        user.profile.save()

        return HttpResponseRedirect(reverse('user_management:profile'))
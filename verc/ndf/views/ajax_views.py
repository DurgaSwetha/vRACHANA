"""
A two-step (registration followed by activation) workflow, implemented
by emailing an HMAC-verified timestamped activation token to the user
on signup.

"""

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import reverse
from ndf.signals import user_activated
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator 
#from django_registration import signals
from ndf.exceptions import ActivationError
from ndf.models import User
from django.http import HttpResponseRedirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from verc.settings import EMAIL_HOST_USER
    
#success_url = reverse_lazy("django_registration_complete")

def register(request):
    print("inside ajax register")
    if request.is_ajax() and request.method == 'POST':
        print("user details:",request.POST.get('firstname',''),request.POST.get('role',''),request.POST.get('repassword',''))
        new_user = User.objects.create()
        new_user.first_name = request.POST.get('firstname','')
        new_user.last_name = request.POST.get('lastname','')
        new_user.username = request.POST.get('username','')
        new_user.email = request.POST.get('useremail','')
        new_user.set_password(request.POST.get('repassword',''))
        new_user.fullname = new_user.first_name + ' ' + new_user.last_name
        new_user.role = request.POST.get('role','')
        new_user.dob = datetime(year=int(request.POST.get('year',1)),month=int(request.POST.get('month',1)),day=1)
        #new_user.has_subscribed = request.POST.get('subscrptn','')
        new_user = create_inactive_user(new_user)
        send_activation_email(request,new_user)
        
    return HttpResponse("Register successful!", content_type="text/plain")

def create_inactive_user(usr):
    """
    Create the inactive user account and send an email containing
    activation instructions.

    """
    #new_user = usr.save()
    usr.is_active = False
    usr.save()
    return usr

def get_activation_key(user):
    """
    Generate the activation key which will be emailed to the user.

    """
    return signing.dumps(obj=user.get_username(), salt='registration')

def get_email_context(request,activation_key):
    """
    Build the template context used for the activation email.

    """
    scheme = "https" if request.is_secure() else "http"
    return {
        "scheme": scheme,
        "activation_key": activation_key,
        "expiration_days": 2,
        "site": get_current_site(request),
    }

def send_activation_email(request,user):
    """
    Send the activation email. The activation key is the username,
    signed using TimestampSigner.

        new_user.is_Moderator = False
        new_user.is_admin = False
    """
    from django.core.mail import send_mail
    activation_key = get_activation_key(user)
    print("activation key:", activation_key)
    context = get_email_context(request,activation_key)
    context["user"] = user
    subject = render_to_string(
        template_name='activation_email_subject.txt',
        context=context,
        request=request,
    )
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = "".join(subject.splitlines())
    message = render_to_string(
        template_name='activation_email_body.txt',
        context=context,
        request=request,
    )
    print("message:",message)
    send_mail(subject, message, EMAIL_HOST_USER,[user.email])
    print("befre httpresponse")
    

ALREADY_ACTIVATED_MESSAGE = _(
    "The account you tried to activate has already been activated."
)
BAD_USERNAME_MESSAGE = _("Thedocker exec -it psql_verc psql docker exec -it psql_verc psql -d verc_psql  -U vrachana-d verc_psql  -U vrachana account you attempted to activate is invalid.")
EXPIRED_MESSAGE = _("This account has expired.")
INVALID_KEY_MESSAGE = _("The activation key you provided is invalid.")
#success_url = reverse_lazy("django_registration_activation_complete")

def activate(request,*args, **kwargs):
    
    username = validate_key(kwargs.get("activation_key"))
    user = get_user(username)
    print("post verfication:",user.is_active)
    user.is_active = True
    user.save()
    print("post save:",user.is_active)
    user_activated.send(sender = 'User', user=user)
    return HttpResponseRedirect(reverse('activation_complete'))

def validate_key(activation_key):
    """
    Verify that the activation key is valid and within the
    permitted activation time window, returning the username if
    valid or raising ``ActivationError`` if not.

    """
    try:
        username = signing.loads(
            activation_key,
            salt='registration',
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
        )
        return username
    except signing.SignatureExpired:
        raise ActivationError(EXPIRED_MESSAGE, code="expired")
    except signing.BadSignature:
        raise ActivationError(
            INVALID_KEY_MESSAGE,
            code="invalid_key",
            params={"activation_key": activation_key},
        )

def get_user(username):
    """
    Given the verified username, look up and return the
    corresponding user account if it exists, or raising
    ``ActivationError`` if it doesn't.

    """
    User = get_user_model()
    try:
        user = User.objects.get(**{User.USERNAME_FIELD: username})
        if user.is_active:
            raise ActivationError(
                ALREADY_ACTIVATED_MESSAGE, code="already_activated"
            )
        return user
    except User.DoesNotExist:
        raise ActivationError(BAD_USERNAME_MESSAGE, code="bad_username")

def user_login(request):
    #return HttpResponse("login!", content_type="text/plain")
        
    
    from django.contrib.auth import authenticate, login
    if request.is_ajax() and request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        uname = request.POST.get('username')
        pwrd = request.POST.get('password')
        
        if uname and pwrd:
            print("credentials:",uname,pwrd)
            user = authenticate(username=uname, password=pwrd)
            print("auth",user.fullname)
            if user is not None:
                login(request, user)
                #return HttpResponse("login successful!", content_type="text/plain")

                return HttpResponseRedirect(reverse('landing_page'))
                #return HttpResponseRedirect(reverse('homepage', kwargs={"group_id": "verc-home"}))
            
            else:
                # Bad login details were provided. So we can't log the user in.
                print ("Invalid login details: {0}, {1}".format(uname, pwrd))
                return HttpResponse("Invalid login details supplied.")
            

def pwrd_reset(request):
    from allauth.account.utils import user_pk_to_url_str
    default_token_generator = EmailAwarePasswordResetTokenGenerator()
    subject_template_name="password_reset_email_subject.txt",
    email_template_name="password_reset_email.html",
    token_generator=default_token_generator,
    from_email=EMAIL_HOST_USER,
    html_email_template_name=None,
    extra_email_context=None,
    
    def _unicode_ci_compare(s1, s2):
        """
        Perform case-insensitive comparison of two identifiers, using the
        recommended algorithm from Unicode Technical Report 36, section
        2.11.2(B)(2).
        """
        import unicodedata
            
        return (
            unicodedata.normalize("NFKC", s1).casefold()
            == unicodedata.normalize("NFKC", s2).casefold()
        )
    
    def _get_users(u_email):
        active_users = get_user_model()._default_manager.filter(
            **{
                "email": u_email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(u_email, getattr(u, 'email'))
        )

    def _send_mail(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        
        msg = render_to_string(email_template_name, context)
        print("body:", msg)
        print("To email IDs:",from_email[0], to_email)
        email_message = EmailMultiAlternatives(subject, msg, from_email[0], [to_email])
        
        email_message.send()
    """
    Generate a one-use only link for resetting password and send it to the
    user.
    """
    user_email = request.POST.get("resetemail")
    
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    print("received params:",current_site, site_name, domain)
    print("default token generator:",default_token_generator)
    for user in _get_users(user_email):
        user_email = getattr(user, 'email')
        context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": user_pk_to_url_str(user),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if False else "http"
                
        }
        print("inside for loop bfr send mail:", user.fullname, user_email, context)
        _send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email
            )
    return HttpResponse("Password reset mail sent successfully!", content_type="text/plain")

def chg_pwrd(request):
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import logout_on_password_change
    if request.is_ajax() and request.method == 'POST':
        cur_pwrd = request.POST.get("currentpassword")
        cfrm_pwrd = request.POST.get("confirmpassword")
        print("inside change password:", cfrm_pwrd, request.user.id)
        print(request.user.check_password(cur_pwrd))
        #request.user.set_password()
        get_adapter().set_password(request.user,cfrm_pwrd)
        logout_on_password_change(request,request.user)
    
    return HttpResponse("Password change done successfully!", content_type="text/plain")  
    

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('landing_page'))




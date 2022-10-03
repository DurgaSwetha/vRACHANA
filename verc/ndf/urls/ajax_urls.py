from django.conf import settings
from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve
from ndf.views.ajax_views import chg_pwrd, custom_logout, register, user_login, pwrd_reset
from verc.settings import GSTUDIO_SITE_NAME, GSTUDIO_OER_GROUPS 
urlpatterns = [
                        #url(r'^accounts/login/', include('captcha.urls')),
                        url(r'^account/register/', register, name='custom_register'), 
                        url(r'^account/login/',user_login,name = 'custom_login'),
                        url(r'^account/logout/',custom_logout,name = 'auth_logout'),
                        url(r'^accounts/password-reset/',pwrd_reset,
                                    name='password_reset'),
                        url(r'^accounts/password-chg/',chg_pwrd,
                                    name='password_chg'),
                        
              ]
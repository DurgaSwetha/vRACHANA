from django.conf import settings
from django.conf.urls import include, url
#from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve

from ndf.forms import *
from verc.settings import GSTUDIO_SITE_NAME, GSTUDIO_OER_GROUPS
from ndf.views.home import homepage, landing_page
from ndf.views.dashboard import userprofile, change_password
login_template = 'login.html'
#logout_template = "landidjango.template.exceptidjango.template.exceptidjango.template.exceptions.TemplateDoesNotExist: registration/login.htmlons.TemplateDoesNotExist: registration/login.htmlons.TemplateDoesNotExist: registration/login.htmlng_page_clix_oer.html"

if settings.DEBUG:
      urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
]
      
#from ndf.views.es_queries import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.contrib import admin
from ndf.views.ajax_views import activate,pwrd_reset
urlpatterns += [
                        url(r'^$', homepage, {"group_id": "verc-home"}, name="homepage"),
                        url(r'^welcome/$', landing_page,  name="landing_page"),
                        
                        url(r'^i18n/', include('django.conf.urls.i18n')),
                        
                        # gstudio admin url's
                        url(r'^admin/', admin.site.urls),
                        url('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('ndf/images/favicon/favicon.ico'))),

                        #ajax URLS
                        url(r'^/ajax/', include('ndf.urls.ajax_urls')),
                        url(r'myDashboard/profile', userprofile, name='user_profile'),
                        url(r'myDashboard/change_password', change_password, name='change_password'),
                        url("accounts/activate/complete/",TemplateView.as_view(
                            template_name="activation_complete.html"),
                                name="activation_complete",
                            ),
                        url(
                            "accounts/activate/(?P<activation_key>[^/]+)/",
                            activate,
                            name="custom_activate",
                        ),
                        #url("^accounts/login/$", login, name ='login'),
                        url("accounts/", include('allauth.urls')),

]

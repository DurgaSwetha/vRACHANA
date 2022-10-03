''' -- imports from installed packages -- '''
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import RequestContext
from django.views.generic import RedirectView

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId


def userprofile(request):
    print("in user profile")
    return render(request,'user-profile.html',
                                {
                                   # "group_id": "grp_id", 'groupid':"verc-home",
                                    'title': 'Profile'
                                })

def change_password(request):
    print("in change password")
    return render(request,'change_password.html',
                                {
                                   # "group_id": "grp_id", 'groupid':"verc-home",
                                    'title': 'Change Passord'
                                })
                
    
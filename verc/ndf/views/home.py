''' -- imports from python libraries -- '''
# import os -- Keep such imports here

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

''' -- imports from application folders/files -- '''
from verc.settings import GAPPS, GSTUDIO_SITE_LANDING_PAGE, GSTUDIO_SITE_NAME, GSTUDIO_SITE_LANDING_TEMPLATE, GSTUDIO_OER_GROUPS
from ndf.models import Group
from ndf.models import node_collection
from ndf.gstudio_es.es import *
from ndf.gstudio_es.paginator import Paginator ,EmptyPage, PageNotAnInteger

###################################################
#   V I E W S   D E F I N E D   F O R   H O M E   #
###################################################
index = 'nodes'
#@get_execution_time
def homepage(request, group_id):

    print("Entered home.py")
    #print("in home:",group_id,GSTUDIO_SITE_LANDING_PAGE)
    return HttpResponseRedirect( reverse('landing_page') )

#@get_execution_time
def landing_page(request):
    '''
    Method to render landing page after checking variables in local_settings/settings file.
    '''
    grp_id = node_collection.find_one({'_cls': u'GSystem.Group', 'name': u'verc-home'})['_id']
    
    '''
    grp_id1 = Search(using=es, index=index,doc_type="node").query(q)
    grp_id2 = grp_id1.execute()
    print("response:",grp_id2)
    group_id = grp_id2[0].id
    '''
    print("landingpage:",request.COOKIES)
    return render(request,'index.html',
                                {
                                    "group_id": grp_id, 'groupid':"verc-home",
                                    'title': 'verc-home'
                                })
    

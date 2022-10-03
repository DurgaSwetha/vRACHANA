from django.contrib.auth.signals import user_logged_in, user_logged_out
from ndf.models import *
from ndf.signals import user_activated
from django.dispatch import receiver

'''
# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])


from django.contrib.auth.signals import user_login_failed

from django.core.mail import send_mail

@receiver(user_login_failed)
def login_fail(sender, credentials, **kwargs):
    print "\n\n LOGIN FAILED"
    print "sender == ", sender
    print "credentials == ", credentials
    send_mail('Login Failed ', 'credentials'+ str(credentials), 'from@example.com',
    ['to@example.com'], fail_silently=False)

'''
@receiver(user_activated)
def create_auth_grp(sender,user,**kwargs):
    '''
    user_activated signal is received when the registered user activates his/her account
    using email confirmation/verification link sent.
    '''
    print("\n\n coming here user_activated----",user.username)

    user_id = user.id
    auth = Author._get_collection().find_one({'_cls': "GSystem.Author", 'created_by': int(user_id)})

    # This will create user document in Author collection to behave user as a group.
    if auth is None:
        auth_gst = Author._get_collection().find_one({'_cls': u'GSystemType', 'name': u'Author'})
        auth = Author()
        # print "\n Creating new Author"
        auth.name = str(user.fullname)
        auth.email = str(user.email)
        auth.password = u""
        auth.member_of.append(auth_gst['_id'])
        auth.submitted_by = user_id
        auth.created_date = datetime.datetime.now()
        auth.authors = [user_id]
        auth_id = ObjectId()
        auth.modified_by = user_id
        auth.user_type = user.role
        auth.id = auth_id
        auth.save()
        # print "\n\n auth===", auth

        # as on when user gets register on platform make user member of two groups:
        # 1: his/her own username group. 2: "home" group
        # adding user's id into author_set of "home" group.
        home_group_obj = Group.objects().get(_cls = 'GSystem.Group' , name = str("verc-home"))
        # being user is log-in for first time on site after registration,
        # directly add user's id into author_set of home group without anymore checking overhead.
        if user_id not in home_group_obj.author_set:
            # print "\n\n adding in home_group_obj"
            Group._get_collection().update({'_id': home_group_obj.id}, {'$push': {'authors': user_id }}, upsert=False, multi=False)
            home_group_obj.reload()
            print('update home grp object:',home_group_obj.to_json())
    return


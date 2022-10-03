from email.policy import default
from .base_imports import *
from .gsystem import *

def _val_agency_type(val):                                                                                                                                             
        if val not in GSTUDIO_AUTHOR_AGENCY_TYPES:                                                                                                                     
                raise ValidationError('agency_type values should be one of predefined')   

class Author(GSystem):
    """Author class to store django user instances
    """
    email=StringField()                                                                                                                                               
    password=StringField()                                                                                                                                             
    preferred_languages=DictField()                                                                                                                                
    language_proficiency=ListField()                                                                                                                                   
    subject_proficiency=ListField() 
    bookmarks_list = ListField(ObjectIdField(),default=list)                                                                                                                             
    user_type = StringField()
    meta = {
    'collection' : 'nodes',
    }
    '''
    @property
    def id(self):
        return self.name
    '''
    def password_crypt(self, password):
        password_salt = str(len(password))
        crypt = hashlib.sha1(password[::-1].upper() + password_salt).hexdigest()
        PASSWORD = str(crypt, 'utf-8')
        return PASSWORD

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    @staticmethod
    def get_author_by_userid(user_id):
        return node_collection.find_one({'_cls': 'GSystem.Author', 'submitted_by': user_id})

    @staticmethod
    def get_user_id_list_from_author_oid_list(author_oids_list=[]):
        all_authors_cur = node_collection.find({'_id': {'$in': [ObjectId(a) for a in author_oids_list]} },
                                                {'_id': 0, 'submitted_by': 1} )
        return [user['submitted_by'] for user in all_authors_cur]

    @staticmethod
    def get_author_obj_from_name_or_id(username_or_userid_or_authid):
        try:
            return node_collection.find_one({'_cls': u'GSystem.Author', 'submitted_by': int(username_or_userid_or_authid)})
        except Exception as e:
            return Group.get_group_name_id(username_or_userid_or_authid, get_obj=True)

    @staticmethod
    def extract_username(request, kwargs):
        if kwargs.get('user_name'):
            return kwargs['user_name']
        elif kwargs.get('username'):
            return kwargs['username']
        elif request:
            return request.user.username
        else:
            return ''

    @staticmethod
    def extract_userid(request, kwargs):
        if kwargs.get('user_id'):
            return kwargs['user_id']
        elif kwargs.get('userid'):
            return kwargs['userid']
        elif request and request.user.id:
            return request.user.id

        try:
            username = Author.extract_username(request, kwargs)
            return User.objects.get(username=username).id
        except Exception as e:
            print(e)            
        # elif:
        #     return 0

    @staticmethod
    def get_author_oid_list_from_user_id_list(user_ids_list=[], list_of_str_oids=False):
        all_authors_cur = node_collection.find({
                                            '_cls': 'GSystem.Author',
                                            'submitted_by': {'$in': [int(uid) for uid in user_ids_list]}
                                        }, {'_id': 1})
        if list_of_str_oids:
            return [str(user['_id']) for user in all_authors_cur]
        else:
            return [user['_id'] for user in all_authors_cur]


    @staticmethod
    def get_author_usernames_list_from_user_id_list(user_ids_list=[]):
        all_authors_cur = node_collection.find({
                                            '_cls': 'GSystem.Author',
                                            'submitted_by': {'$in': [int(uid) for uid in user_ids_list]}
                                        }, {'name': 1})

        result_list = auth_result_list = [user['name'] for user in all_authors_cur]
        user_ids_len = len(user_ids_list)

        # following to address objects inconsistency(if any) in mongo and sql db
        if all_authors_cur.count() != user_ids_len:
            user_result_list = User.objects.values_list('username', flat=True).filter(id__in=user_ids_list)
            if user_ids_len == user_result_list:
                result_list = user_result_list
            else:
                result_list = max(auth_result_list, user_result_list, key=len)

        return result_list


    @staticmethod
    def create_author(user_id_or_obj, agency_type='Student', **kwargs):

        user_obj = None

        if isinstance(user_id_or_obj, int):
            user_obj = User.objects.filter(id=user_id_or_obj)
            if len(user_obj) > 0:
                user_obj = user_obj[0]

        elif isinstance(user_id_or_obj, User):
            user_obj = user_id_or_obj

        if not user_obj:
            raise Exception("\nUser with provided user-id/user-obj does NOT exists!!")

        auth = node_collection.find_one({'_cls': u'GSystem.Author', 'submitted_by': int(user_obj.id)})

        if auth:
            return auth

        auth_gst = node_collection.find_one({'_cls': u'GSystemType', 'name': u'Author'})

        print("\n Creating new Author obj for user id (django): ", user_obj.id)
        auth = Author()
        auth.name = str(user_obj.username)
        auth.email = str(user_obj.email)
        auth.password = u""
        auth.member_of.append(auth_gst._id)
        auth.group_type = u"PUBLIC"
        auth.submitted_by = user_obj.id
        auth.modified_by = user_obj.id
        auth.authors.append(user_obj.id)
        auth.group_admin.append(user_obj.id)
        auth.preferred_languages = {'primary': ('en', 'English')}

        auth.agency_type = "Student"
        auth_id = ObjectId()
        auth['_id'] = auth_id
        auth.save(groupid=auth_id)
        return auth


    @staticmethod
    def get_total_comments_by_user(user_id, return_cur=False, site_wide=False, group_id=None):

        reply_gst = node_collection.find_one({'_type': "GSystemType", 'name': "Reply"}, {'_id': 1})

        comments_query = {'member_of': reply_gst._id,'created_by': user_id}

        if not site_wide:
            group_id = group_id | ObjectId()
            comments_query.update({'group_set': group_id})

        users_replies_cur = node_collection.find(comments_query)

        if users_replies_cur:
            if return_cur:
                return users_replies_cur
            return users_replies_cur.count()
        else:
            return 0


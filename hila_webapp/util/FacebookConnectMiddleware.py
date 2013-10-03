# FacebookConnectMiddleware.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

import md5
import urllib
import time
from django.utils import simplejson
from datetime import datetime

from hila import roundup_utils
import hila.auth.backends

# These values could be placed in Django's project settings
API_KEY = settings.FACEBOOK_API_KEY
API_SECRET = settings.FACEBOOK_SECRET_KEY

REST_SERVER = 'http://api.facebook.com/restserver.php'

# You can get your User ID here: http://developers.facebook.com/tools.php?api
MY_FACEBOOK_UID = settings.FACEBOOK_UID

NOT_FRIEND_ERROR = 'You must be my Facebook friend to log in.'
PROBLEM_ERROR = 'There was a problem. Try again later.'
ACCOUNT_DISABLED_ERROR = 'Your account is not active.'
ACCOUNT_PROBLEM_ERROR = 'There is a problem with your account.'


SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'

fb_prep  = "fb_"

class FacebookConnectMiddleware(object):
    
    delete_fb_cookies = False
    facebook_user_is_authenticated = False
    
    def process_request(self, request):
        
            print "facebook middleware doing something! (process_request)"
 
               
#        try:
             # Set the facebook message to empty. This message can be used to dispaly info from the middleware on a Web page.
            request.facebook_message = None
            # Don't bother trying FB Connect login if the user is already logged in
            if not request.user.is_authenticated():
#            if not request.session.has_key('_auth_user_id'):


#                print "user not authenticated"
#                print "Cookies:" + str(len(request.COOKIES))

                # FB Connect will set a cookie with a key == FB App API Key if the user has been authenticated
                if API_KEY in request.COOKIES:

                    print "Yes cookie!"

                    signature_hash = self.get_facebook_signature(request.COOKIES, True)
                
                    # The hash of the values in the cookie to make sure they're not forged
                    if(signature_hash == request.COOKIES[API_KEY]):

                        print "Hash check ok!"
                
                        # If session hasn't expired
                        if(datetime.fromtimestamp(float(request.COOKIES[API_KEY+'_expires'])) > datetime.now()):

                            print "Datetime check ok!"

                            # Make a request to FB REST(like) API to see if current user is my friend
#                            are_friends_params = {
#                                'method':'Friends.areFriends',
#                                'api_key': API_KEY,
#                                'session_key': request.COOKIES[API_KEY + '_session_key'],
#                                'call_id': time.time(),
#                                'v': '1.0',
#                                'uids1': MY_FACEBOOK_UID,
#                                'uids2': request.COOKIES[API_KEY + '_user'],
#                                'format': 'json',
#                            }
 
#                            print are_friends_params['uids1']
#                            print are_friends_params['uids2']
 
                
 #                           are_friends_hash = self.get_facebook_signature(are_friends_params)

 #                           print "one"
    
 #                           are_friends_params['sig'] = are_friends_hash

 #                           print "two"
                
 #                           are_friends_params = urllib.urlencode(are_friends_params)
                
 #                           print "three"

 #                           are_friends_response  = simplejson.load(urllib.urlopen(REST_SERVER, are_friends_params))
                        
 #                           print "four"

                        
                            # If we are friends
#                            if (str(are_friends_params['uids1']) == str(are_friends_params['uids2'] )) or ( are_friends_response[0]['are_friends'] is True):
                            if 1==1:
                    
#                                user = roundup_utils.get_user_by_name(request.COOKIES[API_KEY + '_user'])

                                print "Authenticating user..."
                                pwd = 'aaaa'+request.COOKIES[API_KEY + '_user']

                                roundup_user = authenticate(username=fb_prep +request.COOKIES[API_KEY + '_user'], password=pwd)

                                userinfo = {
                                                'username': fb_prep + request.COOKIES[API_KEY + '_user'],
                                                'screenname': user_info_response[0]['first_name'] + " " + \
                                                            user_info_response[0]['last_name'],
                                                'address':  request.COOKIES[API_KEY + '_user']+"@facebook.message.sys",
                                                'password':  pwd,

                                                }
                                print "FB debugging!"
                                print userinfo                                
                                if roundup_user is None:
                                    print "we'd like to create some users now."

                                    user_info_params = {
                                        'method': 'Users.getInfo',
                                        'api_key': API_KEY,
                                        'call_id': time.time(),
                                        'v': '1.0',
                                        'uids': request.COOKIES[API_KEY + '_user'],
                                        'fields': 'first_name,last_name',
                                        'format': 'json',
                                    }

                                    user_info_hash = self.get_facebook_signature(user_info_params)
                                    user_info_params['sig'] = user_info_hash
                                    user_info_params = urllib.urlencode(user_info_params)
                                    user_info_response  = simplejson.load(urllib.urlopen(REST_SERVER, user_info_params))
                    
                                    userinfo = {
                                                'username': fb_prep + request.COOKIES[API_KEY + '_user'],
                                                'screenname': user_info_response[0]['first_name'] + " " + \
                                                            user_info_response[0]['last_name'],
                                                'address':  request.COOKIES[API_KEY + '_user']+"@facebook.message.sys",
                                                'password':  pwd,

                                                }
                                    # Create user
                                    user = hila.auth.backends.RoundupUser(roundup_utils.create_user(username=userinfo['username'], screenname=userinfo['screenname'], address=userinfo['address'], passwd=userinfo['password']))
                                    
                                    print "user_id: " +fb_prep +request.COOKIES[API_KEY + '_user']
                                    #roundup_user = hila.auth.backends.RoundupUser(user)
#                                    roundup_user = authenticate(username=fb_prep +request.COOKIES[API_KEY + '_user'], password=pwd)


                                if roundup_user is not None:
                                    print "logging in:"
                                    login(request, roundup_user)
                                    self.facebook_user_is_authenticated = True
                                    print "login done, continuing..."

                                else:
                                    print "logging out and deleting cookies, because user vould not be found!"
                                    logout(request)
                                    self.delete_fb_cookies = True


                                    
#                                try:
#                                    # Try to get Django account corresponding to friend
#                                    # Authenticate then login (or display disabled error message)
#                                    django_user = User.objects.get(username=request.COOKIES[API_KEY + '_user'])
#                                    user = authenticate(username=request.COOKIES[API_KEY + '_user'], 
#                                                        password=md5.new(request.COOKIES[API_KEY + '_user'] + settings.SECRET_KEY).hexdigest())
#                                    if user is not None:
#                                        if user.is_active:
#                                            login(request, user)
#                                            self.facebook_user_is_authenticated = True
#                                        else:
#                                            request.facebook_message = ACCOUNT_DISABLED_ERROR
#                                            self.delete_fb_cookies = True
#                                    else:
#                                       request.facebook_message = ACCOUNT_PROBLEM_ERROR
#                                       self.delete_fb_cookies = True
#                                except User.DoesNotExist:
#                                    # There is no Django account for this Facebook user.
#                                    # Create one, then log the user in.
#                    
#                                    # Make request to FB API to get user's first and last name
#                                    user_info_params = {
#                                        'method': 'Users.getInfo',
#                                        'api_key': API_KEY,
#                                        'call_id': time.time(),
#                                        'v': '1.0',
#                                        'uids': request.COOKIES[API_KEY + '_user'],
#                                        'fields': 'first_name,last_name',
#                                        'format': 'json',
#                                    }
#
#                                    user_info_hash = self.get_facebook_signature(user_info_params)
#
#                                    user_info_params['sig'] = user_info_hash
#                    
#                                    user_info_params = urllib.urlencode(user_info_params)
#
#                                    user_info_response  = simplejson.load(urllib.urlopen(REST_SERVER, user_info_params))
#                    
#                    
#                                    # Create user
#                                    user = User.objects.create_user(request.COOKIES[API_KEY + '_user'], '', 
#                                                                    md5.new(request.COOKIES[API_KEY + '_user'] + 
#                                                                    settings.SECRET_KEY).hexdigest())
#                                    user.first_name = user_info_response[0]['first_name']
#                                    user.last_name = user_info_response[0]['last_name']
#                                    user.save()
#                    
#                                    # Authenticate and log in (or display disabled error message)
#                                    user = authenticate(username=request.COOKIES[API_KEY + '_user'], 
#                                                        password=md5.new(request.COOKIES[API_KEY + '_user'] + settings.SECRET_KEY).hexdigest())
#                                    if user is not None:
#                                        if user.is_active:
#                                            login(request, user)
#                                            self.facebook_user_is_authenticated = True
#                                        else:
#                                            request.facebook_message = ACCOUNT_DISABLED_ERROR
#                                            self.delete_fb_cookies = True
#                                    else:
#                                       request.facebook_message = ACCOUNT_PROBLEM_ERROR
#                                       self.delete_fb_cookies = True

                            
                            # Not my FB friend
#                            else:
#                                print "not a friend!"
#                                request.facebook_message = NOT_FRIEND_ERROR
#                                self.delete_fb_cookies = True
                            
                        # Cookie session expired
                        else:
                            print "cookies expired - logging out?"
                            logout(request)
                            self.delete_fb_cookies = True
                        
                   # Cookie values don't match hash
                    else:
                        print "cookies bad - logging out?"
                        logout(request)
                        self.delete_fb_cookies = True
                    
            # Logged in
            else:
                # If FB Connect user
                if API_KEY in request.COOKIES:
                    # IP hash cookie set
                    if 'fb_ip' in request.COOKIES:
                        
                        try:
                            real_ip = request.META['HTTP_X_FORWARDED_FOR']
                        except KeyError:
                            real_ip = request.META['REMOTE_ADDR']
                        
                        # If IP hash cookie is NOT correct
                        if request.COOKIES['fb_ip'] != md5.new(real_ip + API_SECRET + settings.SECRET_KEY).hexdigest():
                             logout(request)
                             self.delete_fb_cookies = True
                    # FB Connect user without hash cookie set
                    else:
                        logout(request)
                        self.delete_fb_cookies = True
                        
        # Something else happened. Make sure user doesn't have site access until problem is fixed.
#        except:
#            request.facebook_message = PROBLEM_ERROR
#            logout(request)
#            self.delete_fb_cookies = True
        
    def process_response(self, request, response):        
        
        # Delete FB Connect cookies
        # FB Connect JavaScript may add them back, but this will ensure they're deleted if they should be
        if self.delete_fb_cookies is True:
            response.delete_cookie(API_KEY + '_user')
            response.delete_cookie(API_KEY + '_session_key')
            response.delete_cookie(API_KEY + '_expires')
            response.delete_cookie(API_KEY + '_ss')
            response.delete_cookie(API_KEY)
            response.delete_cookie('fbsetting_' + API_KEY)
    
        self.delete_fb_cookies = False
        
        if self.facebook_user_is_authenticated is True:
            try:
                real_ip = request.META['HTTP_X_FORWARDED_FOR']
            except KeyError:
                real_ip = request.META['REMOTE_ADDR']
            response.set_cookie('fb_ip', md5.new(real_ip + API_SECRET + settings.SECRET_KEY).hexdigest())
        
        # process_response() must always return a HttpResponse
        return response
                                
    # Generates signatures for FB requests/cookies
    def get_facebook_signature(self, values_dict, is_cookie_check=False):

        signature_keys = []
        for key in sorted(values_dict.keys()):
            if (is_cookie_check and key.startswith(API_KEY + '_')):
                signature_keys.append(key)
            elif (is_cookie_check is False):
                signature_keys.append(key)

        if (is_cookie_check):
            signature_string = ''.join(['%s=%s' % (x.replace(API_KEY + '_',''), values_dict[x]) for x in signature_keys])
        else:
            signature_string = ''.join(['%s=%s' % (x, values_dict[x]) for x in signature_keys])
        signature_string = signature_string + API_SECRET

        return md5.new(signature_string).hexdigest()
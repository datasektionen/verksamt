import json
import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth.models import User


class DAuth(object):

    @staticmethod
    def authenticate(token=None):

        url = 'http://login2.datasektionen.se/verify/' + str(token) + '.json?api_key=' + settings.AUTH_API_KEY
        req = requests.get(url)
        if req.status_code == 200:
            data = req.json()

            try:
                user = User.objects.get(username=data["user"])
            except User.DoesNotExist:
                user = User(
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    username=data["user"],
                    email=data["emails"]
                )
                user.save()
            return user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def get_permissions(user):
    return json.loads(urllib.parse.unquote(requests.get(
        'http://pls.datasektionen.se/api/user/' + user.username + '/verksamt/'
    ).content.decode('utf-8')))


def has_permission(permission, request):
    if 'permissions' not in request.session:
        # Fetch permissions from pls and store timestamp
        response = requests.get(
                'http://pls.datasektionen.se/api/user/' + request.user.username + '/verksamt/'
        )

        request.session['permissions'] = json.loads(urllib.parse.unquote(response.content.decode('utf-8')))

    return permission in request.session['permissions']

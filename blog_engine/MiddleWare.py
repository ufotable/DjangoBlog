# coding:utf-8
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

def login_user(request, username):
    if request.user.username == "":
        from django.contrib.auth import login
        from django.contrib.auth.models import User
        # from accounts.models import MainUser
        if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if ip in ['127.0.0.1', 'localhost']:
            login(request, User.objects.all().filter(username=username)[0])
            # else:
            #     login(request, User.objects.all().filter(is_superuser=True)[1])

def login_author(request):
    from django.contrib.auth import login
    from django.contrib.auth.models import User

    login(request, User.objects.all().filter(username="author")[0])


def login_superuser(request):
    if request.user.username == "":
        from django.contrib.auth import login
        from django.contrib.auth.models import User
        login(request, User.objects.all().filter(is_staff=True)[0])


# 取消CSRF的中间件
class DisableCSRFCheck(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

from .settings import DEBUG
## 1.11 中间件
# https://docs.djangoproject.com/en/1.11/topics/http/middleware/
# https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering
class SiteMainMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ## 中间件响应前
        # 增加自己的中间件
        if DEBUG:
            # login_author(request)
            login_user(request, "admin")

        response = self.get_response(request) # 上一个中间件进行串联
        ## 访客权限中间件
        #response = visitor_permission_response(request=request, response=response)

        return response
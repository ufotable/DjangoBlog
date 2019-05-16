# coding:utf-8

import os, sys, django

def start_django():
    DjangoModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(DjangoModulePath)
    os.chdir(DjangoModulePath)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_engine.settings")
    django.setup()

if __name__ == '__main__':
    start_django()

    from accounts.models import UserProfileInfo
    from django.contrib.auth.models import User

    _user = User.objects.create_superuser(username="admin", password="112233..", email="test@actanble.com")
    UserProfileInfo.objects.create(user=_user, )

    for x in UserProfileInfo.objects.all():
        print(x)


"""
WSGI config for harikart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'harikart.settings')

application = get_wsgi_application()


"""
WSGI (Web Server Gateway Interface) is a specification that defines how web servers communicate with Python web applications, 
allowing them to be hosted and served efficiently. It acts as a bridge between web servers and frameworks like Django or Flask,
 enabling consistent application deployment across different servers.

 Note: option_settings namespace aws:elasticbeanstalk:container:python 
 This setting, WSGIPath specifies the location of the WSGI script that Elastic Beanstalk uses to start your application.
"""
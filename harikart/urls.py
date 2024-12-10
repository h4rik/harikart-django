"""
URL configuration for harikart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), 
    path('securelogin/', admin.site.urls), # changed from admin to securelogin
    path('', views.home, name='home'),
    path('store/', include('store.urls')), 
    # when user clicks on stores, it should redirect to stores - urls.py
    path('carts/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# chnaged admin to securelogin because if someone knows it is a django application and if the admin pannel url is admin then they can hack with 
# using differnet passwords and they can steal data
# there is something called honey pot 

"""
### Summary:

To enhance the security of the Django admin panel, you can take two steps:

1. **Change the Default Admin URL**:
   - By default, the Django admin panel is accessible via `/admin`. Attackers may attempt to access this page using various combinations of usernames and passwords.
   - To prevent such attempts, change the `/admin` URL to a custom name, like `/secure-login`, in the `urls.py` file. This makes it harder for attackers to guess the admin panel's location.

2. **Implement Django Admin Honeypot**:
   - The **Django admin honeypot** is a fake admin panel that appears to be the real login page. When attackers attempt to log in, it records their IP address, login attempts, and other details, allowing you to track and block them if necessary.
   - To set it up:
     - Install the honeypot package: `pip install django-admin-honeypot`. (this did not worked so install using pip install django-admin-honeypot-updated-2021)
     - Add `admin_honeypot` to `INSTALLED_APPS` in `settings.py`.
     - In `urls.py`, add a new path that redirects `/admin` to the honeypot
    and also migrate it after adding url 
    python manage.py migrate

   When attackers try to access the fake `/admin` page, it logs their IP address and login attempts, helping you identify and block malicious users.

This way, you enhance your Django application's security by making the admin panel harder to find and logging suspicious access attempts.
"""
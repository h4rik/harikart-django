from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
"""We want to create a custom user model to override the default login system that currently uses a username. 
Additionally, we will create a model specifically for the Superadmin role. 
This will allow us to customize the login process, enabling Superadmin users to log in with an email address instead of a username. 
The custom user model will handle both regular users and Superadmins with the desired authentication setup."""

# the below is for creating normal user
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')
        
        #normalize_email means it will convert all the capital letters entered by user into small letters
        user = self.model( 
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        # set_password is used for setting the password
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # create_superuser will take all the attributes and create a user using create_user and set permissions of superuser 
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name= first_name,
            last_name=last_name,
        )
        # the below settings are for making or creating superuser
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
    
# After doing all these we need to tell settings.py that we are going to use custom user model.
# also delete all the existing tables that are created.
"""
This is custom User Model (Accounts App)

In the project, the default Django authentication system requires using a username for login. 
However, since most modern applications use an email address for login instead, we will create a custom user model. 
This custom model will override Django's default behavior, allowing us to use email addresses for authentication while still retaining Django's built-in functionality. 
The custom user model will give us the flexibility to tailor the authentication system to our needs.
"""


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # From this part till the end of the file all are required and mandatory when we creating a custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # we want login credentials to be email address not username so we are changing that now
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # we need to tell this account that we are using the my account manager for creating normal and superuser 
    objects = MyAccountManager()

    #This just means that when we return the account object inside the template. So this should return the email address.
    def __str__(self):
        return self.email

    #If the user is admin, user has all the permissions to do all the changes
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    

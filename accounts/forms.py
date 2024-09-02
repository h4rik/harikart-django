# instead of using normal or manual forms, we can use djnago model forms
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
        
#form contorl is actually a class of bootstrap
# the __init_function is to add all the fields in the registration from page, a bootstrap class(form-control) so that it looks good 
# and also to add place holders for fields
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # the clean method is used to check the password and confirm password entered by the user are both same or not
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password != confirm_password:
            raise  forms.ValidationError(
                "Password does not match!"
            )

            # the above error when raised is printed in templates as {{ form.non_field_errors }} which is a non-field error
"""
super class will actually allow you to change the way it it is saved.
So even if you don't use this all these functions,  then then also the super class will get executed from the Django side.
So we are explicitly using this super class because we want to do something .So we want to modify the things what the Django is giving. 
So that's why we are taking the super class and we are modifying it.


cleaned_data:

    cleaned_data is a dictionary that contains the form data after it has been cleaned and validated by the default clean() method of Django's Form class.
    This dictionary includes the form fields and their validated values.

super().clean():

    super().clean() calls the clean() method of the parent class (Form in this case).
    This ensures that any default cleaning and validation logic provided by Django is executed before you add your own custom logic.


There are actuallu 2 types of errors:
1, field error (when are raised when there are any errors in the fields)
2. Non field error (in the above raised when we submit the registration form )
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('email', 'password1','password2')
        model = User

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].label = "Email Address"

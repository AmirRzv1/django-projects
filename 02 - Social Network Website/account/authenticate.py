from django.contrib.auth.models import User
# this file and this class is for overwriting the
# built-in authenticate so the process work with email too

class EmailBackend:
    # we set these default arguments
    # these username and password are the one which we sent to the
    # authenticate function before
    def authenticate(self, request, username=None, password=None):
        # we use try for the situation that the email belong to no one
        # so we can handle the error
        try:
            # username comes from the user
            # tip -> this username is just a variable and its value comes from the user
            # and here we use it as email for example and we are sending the value only
            user = User.objects.get(email=username)
            # check_password is a method for the user which check both password to be correct
            if user.check_password(password):
                return user
            return None
        # this exception will raise from the django it self for a model that we try
        # to get but it is no exist in our database
        except User.DoesNotExist :
            return None

    # this method get the user with user_id
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
from dj_rest_auth.registration.views import ConfirmEmailView


class CustomConfirmEmailView(ConfirmEmailView):

    def post(self, *args, **kwargs):
        result = super().post(*args, **kwargs)
        print(result)
        return result



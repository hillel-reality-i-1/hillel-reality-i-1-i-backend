from dj_rest_auth.registration.views import ConfirmEmailView


class CustomConfirmEmailView(ConfirmEmailView):

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        return result

    def post(self, *args, **kwargs):
        print(kwargs)
        result = super().post(*args, **kwargs)
        print('result')
        return result

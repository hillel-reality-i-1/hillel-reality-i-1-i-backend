import requests


class AlphaSMSAPI:
    def __init__(self, api_key, from_addr):
        self.base_url = 'https://alphasms.ua/api/http.php'
        self.api_key = api_key
        self.from_addr = from_addr

    def send_sms(self, to_addr, message):
        params = {
            'version': 'http',
            'key': self.api_key,
            'from': self.from_addr,
            'to': to_addr,
            'message': message,
            'command': 'send'
        }
        response = requests.get(self.base_url, params=params)
        return response.text

    def get_message_status(self, message_id):
        params = {
            'version': 'http',
            'key': self.api_key,
            'command': 'receive',
            'id': message_id
        }
        response = requests.get(self.base_url, params=params)
        return response.text

    def delete_message_from_queue(self, message_id):
        params = {
            'version': 'http',
            'key': self.api_key,
            'command': 'delete',
            'id': message_id
        }
        response = requests.get(self.base_url, params=params)
        return response.text

    def get_message_price(self, to_addr):
        params = {
            'version': 'http',
            'key': self.api_key,
            'command': 'price',
            'to': to_addr
        }
        response = requests.get(self.base_url, params=params)
        return response.text

    def check_balance(self):
        params = {
            'version': 'http',
            'key': self.api_key,
            'command': 'balance'
        }
        response = requests.get(self.base_url, params=params)
        return response.text


if __name__ == "__main__":
    ALPHA_SMS_API_KEY = 'a92530f959f8e8fec9fe01ff9589045d6617a8cd'
    ALPHA_SMS_ALPHA_NAME = 'IT-Hillel'
    a = AlphaSMSAPI(ALPHA_SMS_API_KEY, ALPHA_SMS_ALPHA_NAME)
    print(a.check_balance())

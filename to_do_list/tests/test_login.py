from .setup_login import TestLoginSetUp
from django.contrib.auth.models import User

class TestLogin(TestLoginSetUp):
    def test_if_user_logged(self):
        self.login_data = {'username': self.test_user.username, 'password': self.test_user.password}
        self.response = self.c.post('http://127.0.0.1:8000/api-auth/login/', 
        self.login_data, 
        content_type='application/json',
        follow=True)
        print(self.response.context['user'].is_authenticated)
        #self.log = self.c.login(username=self.test_user.username, password=self.test_user.password)
        #self.assertTrue(self.log)
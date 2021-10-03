from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from oauth2_provider.models import AccessToken
from django.utils import timezone
# Test if slack user is redirected to integration page upon check in/out
PAYLOAD = {"token":"gIkuvaNzQIHg97ATvDxqgjtO",
        "team_id":"T0001",
        "team_domain":"example",
        "enterprise_id":"E0001",
        "enterprise_name":"Globular%20Construct%20Inc",
        "channel_id":"C2147483705",
        "channel_name":"test",
        "user_id":"U2147483697",
        "user_name":"Steve",
        "command":"/in",
        "text":"94070",
        "response_url":"https://hooks.slack.com/commands/1234/5678",
        "trigger_id":"13345224609.738474920.8088930838d88f008e0",
        "api_app_id":"A123456"}

User = get_user_model()

class SimpleTest1(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload = PAYLOAD

    def test_wrong_payload(self):
        response = self.client.post(reverse('timesheet'))
        self.assertIn(b'Oops', response.content)
    
    def test_with_slack_payload(self):
        redirect_link = "slackintegration.hivecorelimited.com/slack/"
        payload = self.payload
        
        response = self.client.post(reverse('timesheet'), payload)

        self.assertIn( redirect_link, str(response.content, 'utf-8'))

        payload['command'] = '/nope'

        response = self.client.post(reverse('timesheet'), payload)

        self.assertIn(b'wrong command', response.content)

# Test if user can integrate
class SimpleTest2(TestCase):
    def setUp(self):

        self.payload = PAYLOAD
        self.client = APIClient()
        self.test_user = User.objects.create_user("test_user", "test@example.com", "123456")
        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            scope="read write",
            expires=timezone.now() + timezone.timedelta(seconds=300),
            token="secret-access-token-key",
            application=None,
        )
        self.client.credentials(Authorization='Bearer {}'.format(self.access_token))
        
    def test_authenticated_user_integration(self):
        
        self.assertTrue(self.client.login(username= 'test_user', password='123456'))
        response = self.client.post(reverse('slack-integration'), data={"id": self.payload['user_id']})
        self.assertEquals(response.status_code, 200)
        self.client.logout()

        # Test if user can check in
        payload = self.payload
        payload['command'] = "/in"
        response = self.client.post(reverse('timesheet'), payload)
        self.assertIn( b'punched in', response.content)
        
        # Test if user can check out
        payload['command'] = "/out"
        response = self.client.post(reverse('timesheet'), payload)
        self.assertIn( b'punched out', response.content)



    # Test if user can check out before checking in
    
    def test_authenticated_user_integration(self):
       
        self.assertTrue(self.client.login(username= 'test_user', password='123456'))
        response = self.client.post(reverse('slack-integration'), data={"id": self.payload['user_id']})
        self.assertEquals(response.status_code, 200)
        self.client.logout()
       
        # Test if user can check in
        payload = self.payload
        payload['command'] = "/out"
        response = self.client.post(reverse('timesheet'), payload)
        self.assertIn( b'Timesheet not saved', response.content)
        
        # Test if user can check out
        payload['command'] = "/in"
        response = self.client.post(reverse('timesheet'), payload)
        self.assertIn( b'punched in', response.content)

        # Test if user can check in before checking out

        payload['command'] = "/in"
        response = self.client.post(reverse('timesheet'), payload)
        self.assertIn( b'Timesheet not saved', response.content)

from django.urls import reverse

from hackademic.hcapp import views
from hackademic.hcapp.models import DbUser
from hackademic.hcapp.tests.baset_test import BaseTest


class TestUserView(BaseTest):

    def setUp(self):
        super.setUp()
        #setup one user
        self.user = DbUser.objects.create_user('test_user', 'test@em.ail', 'testpassword')
        self.user.save()

    def test_get(self):
        '''Test the GET /user/ request'''
        self.client.post(reverse(views.UserView.get),{}),
    def test_post(self):
        self.fail()

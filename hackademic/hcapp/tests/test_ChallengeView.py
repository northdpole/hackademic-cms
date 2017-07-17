import pprint

from hcapp.views import ArticleView
from hcapp.models import DbUser, DbChallenge
from .baset_test import BaseTest
from django.urls import reverse


class TestChallengeView(BaseTest):
    def setUp(self):
        # setup one user
        self.user = DbUser.objects.create_user('test_user', 'test@em.ail', 'testpassword', type=0)
        self.user.save()

        self.challenge1 = DbChallenge(title='test_title', description='test_content', author=self.user, category='test',
                                      pkg_name='test',)
        self.challenge1.save()

        self.challenge2 = DbChallenge(title='test_title2', description='test_content2', author=self.user, category='test',
                                      pkg_name='test')
        self.challenge2.save()

    def test_get(self):
        """
        Test the GET hcapp/challenge/ request
            the GET /challenge/ should return a list of all article titles
            so we make sure that we can see the two articles inserted above

            if we want to be thorough we use a tool such as selenium to also make sure that the platform
            only returns the two articles inserted above and they're links and visible but for now let's
             write only unit tests that test the view unit. frontend tests that make sure that the ui doesn't
             break could come later
        """
        response = self.client.get('/hcapp/challenges')
        # pprint.pprint(response.content)
        self.assertContains(response, self.challange1.title)
        self.assertContains(response, self.challenge2.title)

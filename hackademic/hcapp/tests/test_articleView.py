import pprint

from hcapp.views import ArticleView
from hcapp.models import DbUser, DbArticle
from .baset_test import BaseTest
from django.urls import reverse


class TestArticleView(BaseTest):
    def setUp(self):
        # setup one user
        self.user = DbUser.objects.create_user('test_user', 'test@em.ail', 'testpassword', type=0)
        self.user.save()

        self.article1 = DbArticle(title='test_title', content='test_content', created_by=self.user,
                                  last_modified_by=self.user)
        self.article1.save()
        self.article2 = DbArticle(title='test_title2', content='test_content2', created_by=self.user,
                                  last_modified_by=self.user)
        self.article2.save()

    def test_get(self):
        """
        Test the GET hcapp/article/ request
            the GET /article/ should return a list of all article titles
            so we make sure that we can see the two articles inserted above

            if we want to be thorough we use a tool such as selenium to also make sure that the platform
            only returns the two articles inserted above and they're links and visible but for now let's
             write only unit tests that test the view unit. frontend tests that make sure that the ui doesn't
             break could come later
        """
        response = self.client.get('/hcapp/articles')
        # pprint.pprint(response.content)
        self.assertContains(response, self.article1.title)
        self.assertContains(response, self.article2.title)

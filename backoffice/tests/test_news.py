from mock import patch

from django.core.urlresolvers import reverse

from student.models import UserProfile
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from fun.tests.utils import skipUnlessLms
from newsfeed.tests.factories import ArticleFactory


def set_instance_id_to_42(this):
    this.instance.id = 42


@skipUnlessLms
class TestNews(ModuleStoreTestCase):

    def setUp(self):
        super(TestNews, self).setUp()
        self.user.is_superuser = True
        self.user.save()
        UserProfile.objects.create(user=self.user)
        self.client.login(username=self.user.username, password=self.user_password)

    @patch("backoffice.forms.ArticleForm.is_valid")
    @patch("backoffice.forms.ArticleForm.save")
    def test_update_news(self, mock_form_save, mock_form_is_valid):
        news = ArticleFactory.create()
        url = reverse("backoffice:news-detail", kwargs={"news_id": news.id})
        mock_form_is_valid.return_value = True
        response = self.client.post(url)

        self.assertEqual(200, response.status_code)

    @patch("backoffice.forms.ArticleForm.is_valid")
    @patch("backoffice.forms.ArticleForm.save", new=set_instance_id_to_42)
    def test_create_valid_news_redirects_to_news_page(self, mock_form_is_valid):
        url = reverse("backoffice:news-create")
        mock_form_is_valid.return_value = True
        response = self.client.post(url)

        self.assertEqual(302, response.status_code)
        self.assertTrue(response['Location'].endswith(reverse('backoffice:news-detail', kwargs={'news_id': 42})))

from django.core.urlresolvers import reverse

from student.models import UserProfile
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from fun.tests.utils import skipUnlessLms


@skipUnlessLms
class GlobalViewsTestCase(ModuleStoreTestCase):

    def setUp(self):
        super(GlobalViewsTestCase, self).setUp()
        self.user.is_staff = True
        self.user.save()
        UserProfile.objects.create(user=self.user)
        self.client.login(username=self.user.username, password=self.user_password)

    def test_home(self):
        url = reverse('course-dashboard-global:home')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_enrollment_stats(self):
        url = reverse('course-dashboard-global:enrollment-stats')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_student_map(self):
        url = reverse('course-dashboard-global:student-map')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_logged_out_user_is_not_allowed(self):
        self.client.logout()
        url = reverse('course-dashboard-global:home')
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

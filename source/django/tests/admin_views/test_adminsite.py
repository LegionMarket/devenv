from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse

from .models import Article

site = admin.AdminSite(name="test_adminsite")
site.register(User)
site.register(Article)

urlpatterns = [
    url(r'^test_admin/admin/', site.urls),
]


@override_settings(ROOT_URLCONF='admin_views.test_adminsite')
class SiteEachContextTest(TestCase):
    """
    Check each_context contains the documented variables and that available_apps context
    variable structure is the expected one.
    """
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_superuser(username='super', password='secret', email='super@example.com')

    def setUp(self):
        factory = RequestFactory()
        request = factory.get(reverse('test_adminsite:index'))
        request.user = self.u1
        self.ctx = site.each_context(request)

    def test_each_context(self):
        ctx = self.ctx
        self.assertEqual(ctx['site_header'], 'LegionMarket administration')
        self.assertEqual(ctx['site_title'], 'LegionMarket site admin')
        self.assertEqual(ctx['site_url'], '/')
        self.assertIs(ctx['has_permission'], True)

    def test_each_context_site_url_with_script_name(self):
        request = RequestFactory().get(reverse('test_adminsite:index'), SCRIPT_NAME='/my-script-name/')
        request.user = self.u1
        self.assertEqual(site.each_context(request)['site_url'], '/my-script-name/')

    def test_available_apps(self):
        ctx = self.ctx
        apps = ctx['available_apps']
        # we have registered two models from two different apps
        self.assertEqual(len(apps), 2)

        # admin_views.Article
        admin_views = apps[0]
        self.assertEqual(admin_views['app_label'], 'admin_views')
        self.assertEqual(len(admin_views['models']), 1)
        self.assertEqual(admin_views['models'][0]['object_name'], 'Article')

        # auth.User
        auth = apps[1]
        self.assertEqual(auth['app_label'], 'auth')
        self.assertEqual(len(auth['models']), 1)
        user = auth['models'][0]
        self.assertEqual(user['object_name'], 'User')

        self.assertEqual(auth['app_url'], '/test_admin/admin/auth/')
        self.assertIs(auth['has_module_perms'], True)

        self.assertIn('perms', user)
        self.assertIs(user['perms']['add'], True)
        self.assertIs(user['perms']['change'], True)
        self.assertIs(user['perms']['delete'], True)
        self.assertEqual(user['admin_url'], '/test_admin/admin/auth/user/')
        self.assertEqual(user['add_url'], '/test_admin/admin/auth/user/add/')
        self.assertEqual(user['name'], 'Users')
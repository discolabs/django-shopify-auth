from django.test import TestCase


class ViewsTestCase(TestCase):

    def test_create_super_user(self):
        User.objects.create_superuser(username='admin', password='adminadmin', email='')
        

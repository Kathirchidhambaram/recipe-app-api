from django.test import SimpleTestCase

class Viewstest(SimpleTestCase):

    def test_duplicate(self):
        lst = [1, 2, 2, 3, 4, 4]
        res = set(lst)
        self.assertEqual(4, len(res))
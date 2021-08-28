from django.test import TestCase
from quotes.models import Quote


class QuoteTestCase(TestCase):
    def test_split(self):
        q = Quote(added_by='test runner', quote='Foo|Bar|Baz')
        self.assertEqual(list(q.lines), ['Foo', 'Bar', 'Baz'])

    def test_strip_whitespace(self):
        q = Quote(added_by='test runner', quote='Foo | Bar | Baz')
        self.assertEqual(list(q.lines), ['Foo', 'Bar', 'Baz'])

    def test_handle_escape(self):
        q = Quote(added_by='test runner', quote='Foo\\|Bar|Baz')
        self.assertEqual(list(q.lines), ['Foo|Bar', 'Baz'])

    def test_strip_escape(self):
        q = Quote(added_by='test runner', quote='I guess !qsay is broken :\\|')
        self.assertEqual(list(q.lines), ['I guess !qsay is broken :|'])

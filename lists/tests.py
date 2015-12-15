from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template.context_processors import csrf

from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		#print (repr(response.content))
		#self.assertTrue(response.content.startswith(b'<html>'))
		#self.assertTrue(response.content.endswith(b'</html>'))
		
		# http://s1n4.github.io/2013/05/12/django-csrf_token-when-using-render_to_string/
		c = {'new_item_text': 'A new list item'}
		# nothing in the `request`. so there is no need to replace the `new_item_text`
		c = {}
		c.update(csrf(request))
		expected_html = render_to_string(
			'home.html',
			c
		)
		#print("content:\n %s\n" % response.content.decode())
		#print(expected_html)
		#self.assertIn('A new list item', response.content.decode())
		self.assertEqual(response.content.decode(), expected_html)
	
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		self.assertIn('A new list item', response.content.decode())
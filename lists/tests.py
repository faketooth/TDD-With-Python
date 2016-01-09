from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template.context_processors import csrf

from lists.models import Item
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
		self.assertEqual(response.content.decode(), expected_html)
		
	
	
class ItemModelTest(TestCase):
	
	def test_saving_and_retriving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')
		

class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')
	
	def test_displays_all_item(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')
		
		response = self.client.get('/lists/the-only-list-in-the-world/')
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

		
class NewListTest(TestCase):
	
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new', # no slash after database modification operation.
			data={'item_text': 'A new list item'})
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
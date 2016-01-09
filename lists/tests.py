from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template.context_processors import csrf

from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		
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
		
	
	
class ListAndItemModelsTest(TestCase):
	
	def test_saving_and_retriving_items(self):
		list_=List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		dir(first_item)
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)
		

class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		#response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')
	
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

		
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)
	
	
		
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
		new_list = List.objects.first()
		self.assertEqual(response['location'], '/lists/%d/' % (new_list.id,))
		
		
		
class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
			)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
		
	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
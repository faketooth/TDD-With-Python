from __future__ import unicode_literals

from django.db import models

class List(models.Model):
	pass

	
		
class Item(models.Model):
	text = models.TextField(default='')
	#django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
	#list = models.ForeignKey(List, null=True, default=None)
	list = models.ForeignKey(List, default=None)


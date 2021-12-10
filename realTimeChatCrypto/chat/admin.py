from django.contrib import admin

from . import models

admin.site.register(models.SuggestionModel)
admin.site.register(models.CommentModel)

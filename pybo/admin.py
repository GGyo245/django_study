from django.contrib import admin

# Register your models here.
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sbject',
        'content',
        'create_date'
    )
    search_fields = ['sbject']

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content',
        'create_date'
    )
    search_fields = ['content']
    

admin.site.register(Question, QuestionAdmin)        
admin.site.register(Answer, AnswerAdmin)
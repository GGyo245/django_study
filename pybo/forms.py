from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['sbject', 'content']
        # 질문 등록 화면의 클래스 적용(폼이 자동 생성 되기에 지정해야함)
        # 자동 생성을 포기하고 수작업으로 폼을 작성하면 이러한 문제 X
        widgets = {
            'sbject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
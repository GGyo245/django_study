from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Question
from .models import Hot_issue
from django.utils import timezone
from .forms import QuestionForm

from django.core.paginator import Paginator

# 크롤링
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Create your views here.


def index(request):
    '''
    pybo 목록 출력
    '''

    '''
    크롤링
    '''
    html = urlopen('https://www.daum.net/')
    bsObject = BeautifulSoup(html, 'html.parser')
    favor_length = bsObject.find(class_='slide_favorsch')
    keyword = favor_length.text.split('\n\n\n')
    result = []
    
    # 쓸모없는 정보 지우기
    for value in keyword:
        if len(value) != 0:
            result.append(value.replace('\n\n',''))
    

    # url 
    url_str = str(favor_length)
    href_temp = url_str.split('href=')
    del href_temp[0]
    href = []
    fina = []
    for idx in range(len(href_temp)):
        href.append(href_temp[idx][href_temp[idx].index('https'):href_temp[idx].index('">')])

    # 크롤링 한 실시간 검색어 정보 클래스에 삽입 (실시간 키워드, url)
    for idx in range(len(result)):
        p = Hot_issue()
        p.set_info(result[idx],href[idx].replace('amp;','&'))
        fina.append(p)
    
    page = request.GET.get('page', '1') # 페이지
    question_list = Question.objects.order_by('-create_date') # - 는 역순을 의미


    
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개
    page_obj = paginator.get_page(page)
    
    context = {'question_list' : page_obj,
                'issue' : fina,}

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    '''    
    pybo 내용 출력
    '''
    question = Question.objects.get(id=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    '''
    pybo 답변등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    
    return redirect('pybo:detail', question_id=question_id)

def question_create(request):
    '''
    pybo 질문등록
    '''

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # False 는 임시저장을 의미 (날짜 저장을 위해)
            # form.save(commit=False) 대신 form.save()를 수행하면 create_date 속성값이 없다는 오류 메시지가 나타난다.
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

    # form = QuestionForm()
    # return render(request, 'pybo/question_form.html', {'form':form})



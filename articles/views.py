from django.shortcuts import render, redirect

from .models import Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles' : articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    new_title = request.GET.get('title')
    new_content = request.GET.get('content')
    article = Article(title=new_title, content=new_content)
    article.save()
    context = {
        'article': article
    }
    # return render(request, 'articles/create.html', context)
    return redirect('/articles/')
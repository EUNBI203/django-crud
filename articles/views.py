from django.shortcuts import render, redirect
# from IPython import embed
from django.views.decorators.http import require_POST
from .models import Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles' : articles
    }
    # embed()
    return render(request, 'articles/index.html', context)

# def new(request):
#     if request.method == 'GET':
#         return render(request, 'articles/new.html')
#     else: #'POST'
#         new_title = request.POST.get('title')
#         new_content = request.POST.get('content')
#         article = Article(title=new_title, content=new_content)
#         article.save()
#         return redirect('articles:detail', article.pk )

def create(request):
    # 저장 로직
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')
        article = Article(title=new_title, content=new_content)
        article.save()
        return redirect('articles:detail', article.pk )
    else:
        return render(request, 'articles/new.html')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # if request.method == "POST":
    article.delete()
    return redirect('articles:index')
    # else:
    #     return redirect('articles:derail', article_pk)

# def edit(request, article_pk):
#     if request.method == 'GET':
#         article = Article.objects.get(pk=article_pk)
#         context = {
#             'article': article
#         }
#         return render(request, 'articles/edit.html', context)
#     else:
#         article = Article.objects.get(pk=article_pk)
#         article.title = request.POST.get('title')
#         article.content = request.POST.get('content')
#         article.save()
#         return redirect('articles:detail', article.pk)

def update(request, article_pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_pk)
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect('articles:detail', article.pk)
    else:
        article = Article.objects.get(pk=article_pk)
        context = {
            'article': article
        }
        return render(request, 'articles/edit.html', context)
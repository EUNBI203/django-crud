from django.shortcuts import render, redirect, get_object_or_404
# from IPython import embed
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
# from accounts.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse

# Create your views here.
@require_GET
def index(request):
    articles = Article.objects.all()
    # embed()
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

@login_required
def create(request):
    # if request.user.is_authenticated:
    # 저장 로직
    if request.method == 'POST':
    # POST 요청 -> 검증 및 저장
        article_form = ArticleForm(request.POST, request.FILES)
        
        # embed()
        if article_form.is_valid():
        # 검증에 성공하면 저장하고,
            # new_title = article_form.cleaned_data.get('title')
            # new_content = article_form.cleaned_data.get('content')
            # article = Article(title=new_title, content=new_content)
            # article.save()
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            # redirect
            return redirect('articles:detail', article.pk )
    else:
    # GET요청 -> Form
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패시 에러메세지와 입력값 채워진 Form context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
    # else:
    #     return redirect('accounts:login')

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'articles/detail.html', context)
    
@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        # article = Article.objects.get(pk=article_pk)
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
        # if request.method == "POST":
            article.delete()
            return redirect('articles:index')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponse('Unauthorized', status=401)

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
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, instance=article)
            # article = Article.objects.get(pk=article_pk)
            # article.title = request.POST.get('title')
            # article.content = request.POST.get('content')
            # article.save()
            if article_form.is_valid():
                article = article_form.save()
                return redirect('articles:detail', article.pk )
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        return HttpResponseForbidden()

@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        # 1. modelform에 사용자 입력값 넣고
        comment_form = CommentForm(request.POST)
        # 2. 검증하고,
        if comment_form.is_valid():
        # 3. 맞으면 저장!
        # 3-1. 사용자 입력값으로 comment instance 생성 (저장은 X)
            comment = comment_form.save(commit=False)
            # 3-2. FK 넣고 저장
            comment.article = article
            comment.user = request.user
            comment.save()
        # 4. return redirect
        else:
            messages.info(request, '댓글 형식이 맞지 않습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('Unauthorized', status=401)

    # comment = Comment()
    # comment.content = request.POST.get('content')
    # comment.article_id = article_pk
    # comment.save()
    # messages.info(request, '댓글이 등록되었습니다.')
    # return redirect('articles:detail', article_pk)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
    # article_pk = comment.article_id
        comment.delete()
    # messages.error(request, '댓글이 삭제되었습니다.')
        messages.add_message(request, messages.INFO, '댓글이 삭제되었습니다.' )
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponseForbidden()

@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)
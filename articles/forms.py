from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=140)
    content = forms.CharField()
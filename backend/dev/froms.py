from django import forms


class CreateArticleForm(forms.Form):
    title = forms.CharField(max_length=64)
    content = forms.CharField(widget=forms.Textarea, max_length=1024)

class SetNameForm(forms.Form):
    your_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder':'Enter your name'}))
from django import forms


class HomeForm(forms.Form):
    GitUserName = forms.CharField(label='Git User Name', max_length=288)



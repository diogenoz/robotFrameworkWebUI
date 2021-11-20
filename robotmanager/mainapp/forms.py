from django import forms
from .models import *


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ('name', 'description', 'test_case_category', 'keywords')

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 20}))


class ArgumentSetForm(forms.ModelForm):
    class Meta:
        model = ArgumentSet
        fields = ('name', 'test_case')

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 20}))


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('name', 'description', 'keyword_group')

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 20}))


class TestRunAddForm(forms.ModelForm):
    class Meta:
        model = TestRun
        fields = ('test_case', 'argument_set', 'environment')


class TestCaseCategoryForm(forms.ModelForm):
    class Meta:
        model = TestCaseCategory
        fields = ('name', 'description', 'parent')


class KeywordGroupForm(forms.ModelForm):
    class Meta:
        model = TestCaseCategory
        fields = ('name', 'description', 'parent')


class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ('name',)

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 20}))

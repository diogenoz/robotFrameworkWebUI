from django.contrib import admin
from .models import TestCase, TestCaseCategory, Keyword, KeywordGroup, TestRun, ArgumentSet
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html


@admin.register(TestCaseCategory)
class TestCaseCategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    mptt_indent_field = "name"
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id', 'name')


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'test_case_category')
    list_display_links = ('id', 'name')


@admin.register(ArgumentSet)
class ArgumentSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'test_case')
    list_display_links = ('id', 'name')


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_case', 'argument_set', 'create_datetime', 'start_datetime', 'stop_datetime', 'status')
    list_display_links = ('id', 'argument_set', 'argument_set')


@admin.register(KeywordGroup)
class KeywordGroupAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id', 'name')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'keyword_group')
    list_display_links = ('id', 'name')

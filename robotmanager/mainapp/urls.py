
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testcasecategories/add', views.test_case_category_form, name='test_case_category_add'),
    path('testcasecategories/<int:test_case_category_id>/edit', views.test_case_category_form, name='test_case_category_edit'),
    path('testcases', views.index, name='test_cases_index'),
    path('testcases/add', views.test_case_form, name='test_case_add'),
    path('testcases/<int:test_case_id>', views.test_case_index, name='test_case_index'),
    path('testcases/<int:test_case_id>/edit', views.test_case_form, name='test_case_edit'),
    path('testcases/<int:test_case_id>/args', views.argument_set_index, name='argument_set_index'),
    path('testcases/<int:test_case_id>/args/add', views.argument_set_form, name='argument_set_add'),
    path('testcases/<int:test_case_id>/args/<int:arg_set_id>/edit', views.argument_set_form, name='argument_set_edit'),
    path('testcases/<int:test_case_id>/runs', views.test_run_index, name='test_run_index'),
    path('testcases/<int:test_case_id>/runs/add', views.test_run_add, name='test_run_add'),
    path('keywords/', views.keywords_index, name='keywords_index'),
    path('keywords/add', views.keyword_form, name='keyword_add'),
    path('keywords/<int:keyword_id>', views.keyword_index, name='keyword_index'),
    path('keywords/<int:keyword_id>/edit', views.keyword_form, name='keyword_edit'),
    path('keywordgroups/add', views.keyword_form, name='keyword_group_add'),
    path('keywordgroups/<int:keyword_group_id>/edit', views.keyword_group_form, name='keyword_group_edit'),
    path('environments/', views.environments_index, name='environments_index'),
    path('environments/add', views.environment_form, name='environment_add'),
    path('environments/<int:environment_id>/edit', views.environment_form, name='environment_edit'),
]

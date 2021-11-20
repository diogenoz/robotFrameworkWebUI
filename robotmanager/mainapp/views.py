from django.shortcuts import render, redirect
from .forms import *


def index(request):
    return render(request
                  , 'index.html'
                  , {'test_case_categories': TestCaseCategory.objects.all()
                      , 'test_cases': TestCase.objects.all()}
                  )


def test_case_index(request, test_case_id):
    test_case = TestCase.objects.get(id=test_case_id)
    content = test_case.get_content_from_file()
    return render(request
                  , 'test_case/index.html'
                  , {'test_case': test_case, 'content': content}
                  )


def test_case_form(request, test_case_id=None):
    if request.method == 'POST':
        form = TestCaseForm(request.POST)

        if form.is_valid():
            try:
                test_case = form.save(commit=False)
                test_case.set_content(form.cleaned_data.get('content'), test_case_id, form.cleaned_data.get('keywords'))
                form.save()
                return redirect('test_case_index', test_case.id)
            except Exception as e:
                form.add_error(None, f'error in update test case:{e}')
                print(e)
    else:
        if test_case_id:
            test_case = TestCase.objects.get(id=test_case_id)
            form = TestCaseForm(instance=test_case,
                                initial={'content': test_case.get_content_from_file, 'id': test_case_id})
        else:
            form = TestCaseForm()

    return render(request, 'test_case/form.html', {'form': form, 'test_case_id': test_case_id})


def argument_set_index(request, test_case_id):
    return render(request
                  , 'test_case/argument_set/index.html'
                  , {'argument_sets': ArgumentSet.objects.filter(test_case_id=test_case_id),
                     'test_case_id': test_case_id}
                  )


def argument_set_form(request, test_case_id, arg_set_id=None):
    if request.method == 'POST':
        form = ArgumentSetForm(request.POST)

        if form.is_valid():
            try:
                argument_set = form.save(commit=False)
                argument_set.set_content(form.cleaned_data.get('content'), arg_set_id)
                form.save()
                return redirect('test_case_index', test_case_id)
            except Exception as e:
                form.add_error(None, f'error in update test case:{e}')
                print(e)
    else:
        test_case = TestCase.objects.get(id=test_case_id)
        if arg_set_id:
            argument_set = ArgumentSet.objects.get(id=arg_set_id)
            form = ArgumentSetForm(instance=argument_set,
                                   initial={'content': argument_set.get_content_from_file, 'id': arg_set_id,
                                            'test_case': test_case})
        else:
            form = ArgumentSetForm(initial={'test_case': test_case, 'content': test_case.get_example_arg_set()})

    return render(request, 'test_case/argument_set/form.html',
                  {'form': form, 'test_case_id': test_case_id, 'arg_set_id': arg_set_id})


def test_run_index(request, test_case_id):
    return render(request
                  , 'test_case/test_run/index.html'
                  , {'test_runs': TestRun.objects.filter(test_case_id=test_case_id),
                     'test_case_id': test_case_id}
                  )


def test_run_add(request, test_case_id):
    if request.method == 'POST':
        form = TestRunAddForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('test_case_index', test_case_id)
            except Exception as e:
                form.add_error(None, 'error in add test run')
                print(e)
    else:
        test_case = TestCase.objects.get(id=test_case_id)
        form = TestRunAddForm(initial={'test_case': test_case})
    return render(request, 'test_case/test_run/form.html', {'form': form, 'test_case_id': test_case_id})


def keywords_index(request):
    return render(request
                  , 'keyword/index.html'
                  , {'keyword_groups': KeywordGroup.objects.all()
                      , 'keywords': Keyword.objects.all()}
                  )


def keyword_index(request, keyword_id):
    return render(request
                  , 'keyword/keyword.html'
                  , {'keyword': Keyword.objects.get(id=keyword_id)}
                  )


def keyword_add(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)

        if form.is_valid():
            try:
                keyword = form.save(commit=False)
                keyword.set_content(form.data.get('content'))
                form.save()
                return redirect('keywords_index')
            except Exception as e:
                form.add_error(None, 'error in add test case')
                print(e)
    else:
        form = KeywordForm()
    return render(request, 'keyword/form.html', {'form': form})


def keyword_form(request, keyword_id=None):
    if request.method == 'POST':
        form = KeywordForm(request.POST)

        if form.is_valid():
            try:
                keyword = form.save(commit=False)
                keyword.set_content(form.cleaned_data.get('content'), keyword_id)
                form.save()
                return redirect('keywords_index')
            except Exception as e:
                form.add_error(None, f'error in update keyword:{e}')
                print(e)
    else:
        if keyword_id:
            keyword = Keyword.objects.get(id=keyword_id)
            form = KeywordForm(instance=keyword, initial={'content': keyword.get_content_from_file, 'id': keyword_id})
        else:
            form = KeywordForm()

    return render(request, 'keyword/form.html', {'form': form, 'keyword_id': keyword_id})


def test_case_category_form(request, test_case_category_id=None):
    if request.method == 'POST':
        form = KeywordForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except Exception as e:
                form.add_error(None, f'error in update test case category:{e}')
                print(e)
    else:
        if test_case_category_id:
            test_case_category = TestCaseCategory.objects.get(id=test_case_category_id)
            form = TestCaseCategoryForm(instance=test_case_category)
        else:
            form = TestCaseCategoryForm()

    return render(request, 'test_case_category/form.html',
                  {'form': form, 'test_case_category_id': test_case_category_id})


def keyword_group_form(request, keyword_group_id=None):
    if request.method == 'POST':
        form = KeywordForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('keywords_index')
            except Exception as e:
                form.add_error(None, f'error in update keyword group:{e}')
                print(e)
    else:
        if keyword_group_id:
            keyword_group = KeywordGroup.objects.get(id=keyword_group_id)
            form = KeywordGroupForm(instance=keyword_group)
        else:
            form = KeywordGroupForm()

    return render(request, 'keyword_group/form.html', {'form': form, 'keyword_group_id': keyword_group_id})


def environments_index(request):
    return render(request
                  , 'environment/index.html'
                  , {'environments': Environment.objects.all()}
                  )


def environment_add(request):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST)

        if form.is_valid():
            try:
                environment = form.save(commit=False)
                environment.set_content(form.data.get('content'))
                form.save()
                return redirect('environments_index')
            except Exception as e:
                form.add_error(None, 'error in add environment')
                print(e)
    else:
        form = EnvironmentForm()
    return render(request, 'environment/form.html', {'form': form})


def environment_form(request, environment_id=None):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST)

        if form.is_valid():
            try:
                environment = form.save(commit=False)
                environment.set_content(form.cleaned_data.get('content'), environment_id)
                form.save()
                return redirect('environments_index')
            except Exception as e:
                form.add_error(None, f'error in update environment:{e}')
                print(e)
    else:
        if environment_id:
            environment = Environment.objects.get(id=environment_id)
            form = EnvironmentForm(instance=environment,
                                   initial={'content': environment.get_content_from_file, 'id': environment_id})
        else:
            form = EnvironmentForm()

    return render(request, 'environment/form.html', {'form': form, 'environment_id': environment_id})

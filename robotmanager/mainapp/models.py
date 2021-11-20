import re

from django.db.models.functions import Now
import os
from django.core.files import move as django_move
from datetime import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify

from .services import *


def archive_old_file(file_path):
    date_str = datetime.today().strftime('%Y%m%d%H%M%S')
    archive_dir_path = os.path.join(os.path.dirname(file_path), 'archive')
    if not os.path.exists(archive_dir_path):
        os.makedirs(archive_dir_path)

    archive_file_path = os.path.join(archive_dir_path, f'{date_str}_{os.path.basename(file_path)}')
    django_move.file_move_safe(file_path, archive_file_path)


class KeywordGroup(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, default=None, blank=True,
                            related_name='children')

    def __str__(self):
        return f'[{self.id}] {self.name}'


class Keyword(models.Model):
    content = ''
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    keyword_group = models.ForeignKey(KeywordGroup, on_delete=models.PROTECT)
    slug = models.SlugField(db_index=True, max_length=255, verbose_name="Slug name", unique=False)
    file_path = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'[{self.id}] {self.name}'

    def get_content_from_file(self):
        path = os.path.join(settings.MEDIA_ROOT, self.file_path)
        storage = FileSystemStorage()
        return storage.open(name=path, mode='r').read()

    def get_dir_name(self):
        return 'keywords'

    def set_content(self, content: str, id: int = None):
        slug = slugify(self.name)
        content_file = ContentFile(content)
        storage = FileSystemStorage()

        file_path = os.path.join(self.get_dir_name(), slug, slug + '.robot')
        abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if storage.exists(abs_file_path):
            if id is None:
                raise FileExistsError('File is exists')
            archive_old_file(abs_file_path)

        storage.save(abs_file_path, content_file)
        if self.slug is None:
            self.slug = slug
        if id:
            self.id = id
        self.file_path = file_path


class TestCaseCategory(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, default=None, blank=True,
                            related_name='children')

    def __str__(self):
        return f'[{self.id}] {self.name}'


def replace_keyword_links(content, keywords):
    # clear old links
    content_without_links: str = ''
    contents = content.split('\n')
    for line in contents:
        resource_match = re.findall(r'\W*resource\W*', line, re.IGNORECASE)
        if not resource_match:
            content_without_links += str(line) + '\n'
    # add new links
    content_with_links: str = ''
    for content_line in content_without_links.split('\n'):
        test_case_match = re.findall(r'.+/*/*/*.+test.+cases.+/*/*/*.+', content_line, re.IGNORECASE)
        if test_case_match:
            for keyword in keywords:
                content_with_links += f'Resource \t{os.path.join(settings.MEDIA_ROOT, keyword.file_path)}  \n'
        content_with_links += content_line + '\n'
    return content_with_links


def replace_library_links(content):
    # clear old links
    contents = content.split('\n')
    is_library_exists = False
    for line in contents:
        resource_match = re.findall(r'Library.+SeleniumLibrary', line, re.IGNORECASE)
        if resource_match:
            is_library_exists = True
            break
    content_with_links: str = ''
    if is_library_exists:
        content_with_links = content
    else:
        # add new links
        for content_line in content.split('\n'):
            test_case_match = re.findall(r'.+/*/*/*.+test.+cases.+/*/*/*.+', content_line, re.IGNORECASE)
            if test_case_match:
                content_with_links += 'Library SeleniumLibrary\n'
            content_with_links += content_line + '\n'
    return content_with_links


class TestCase(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    description = models.CharField(max_length=300, verbose_name="Description")
    slug = models.SlugField(db_index=False, max_length=255, verbose_name="Slug name", unique=False)
    test_case_category = models.ForeignKey(TestCaseCategory, on_delete=models.PROTECT, verbose_name="Category")
    file_path = models.CharField(blank=True, max_length=255, verbose_name="Path")
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name="Keywords")

    def __str__(self):
        return f'[{self.id}] {self.name}'

    def get_content_from_file(self):
        path = os.path.join(settings.MEDIA_ROOT, self.file_path)
        storage = FileSystemStorage()
        return storage.open(name=path, mode='r').read()

    def get_absolute_url(self):
        return reverse('testcases', kwargs={'id': self.id})

    def get_dir_name(self):
        return 'test_cases'

    def set_content(self, content: str, id: int = None, keywords=[]):
        slug = slugify(self.name)
        if self.slug is None:
            self.slug = slug

        if id:
            self.id = id

        content = replace_library_links(content)
        content = replace_keyword_links(content, keywords)
        content_file = ContentFile(content)
        storage = FileSystemStorage()

        file_path = os.path.join(self.get_dir_name(), slug, slug + '.robot')
        abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if storage.exists(abs_file_path):
            # if exists file when add new case, then raise
            if id is None:
                raise FileExistsError('File is exists')
            archive_old_file(abs_file_path)
        storage.save(abs_file_path, content_file)
        self.file_path = file_path

    def get_example_arg_set(self):
        content = self.get_content_from_file()
        args = re.findall(r'\$\{(\w+)\}\W', content)
        result_str = ''
        for arg in args:
            if re.search('ENV_'.lower(), arg.lower()):
                continue
            result_str += f'{arg}: \n'
        return result_str


class ArgumentSet(models.Model):
    name = models.CharField(max_length=50)
    test_case = models.ForeignKey(TestCase, on_delete=models.PROTECT)
    slug = models.SlugField(db_index=True, max_length=255, verbose_name="Slug name", unique=False)
    file_path = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'[{self.id}] {self.name}'

    def get_content_from_file(self):
        path = os.path.join(settings.MEDIA_ROOT, self.file_path)
        storage = FileSystemStorage()
        return storage.open(name=path, mode='r').read()

    def get_dir_name(self):
        return os.path.join(os.path.dirname(self.test_case.file_path), 'args')

    def set_content(self, content: str, id: int = None):
        slug = slugify(self.name)
        content_file = ContentFile(content)
        storage = FileSystemStorage()

        file_path = os.path.join(self.get_dir_name(), slug, slug + '.yaml')
        abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if storage.exists(abs_file_path):
            # if exists file when add new case, then raise
            if id is None:
                raise FileExistsError('File is exists')
            archive_old_file(abs_file_path)

        storage.save(abs_file_path, content_file)
        if self.slug is None:
            self.slug = slug
        if id:
            self.id = id
        self.file_path = file_path


class Environment(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(db_index=True, max_length=255, verbose_name="Slug name", unique=False)
    file_path = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'[{self.id}] {self.name}'

    def get_content_from_file(self):
        path = os.path.join(settings.MEDIA_ROOT, self.file_path)
        storage = FileSystemStorage()
        return storage.open(name=path, mode='r').read()

    def get_dir_name(self):
        return 'Environments'

    def set_content(self, content: str, id: int = None):
        slug = slugify(self.name)
        content_file = ContentFile(content)
        storage = FileSystemStorage()

        file_path = os.path.join(self.get_dir_name(), slug, slug + '.yaml')
        abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if storage.exists(abs_file_path):
            # if exists file when add new case, then raise
            if id is None:
                raise FileExistsError('File is exists')
            archive_old_file(abs_file_path)

        storage.save(abs_file_path, content_file)
        if self.slug is None:
            self.slug = slug
        if id:
            self.id = id
        self.file_path = file_path


class TestRun(models.Model):
    class TestRunStatus(models.IntegerChoices):
        INIT = 0
        RUN = 1
        COMPLETED = 2
        FAILED = 3

    create_datetime = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    stop_datetime = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=TestRunStatus.choices)
    test_case = models.ForeignKey(TestCase, on_delete=models.PROTECT)
    argument_set = models.ForeignKey(ArgumentSet, on_delete=models.PROTECT)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    report_file_path = models.CharField(blank=True, max_length=255)
    test_log_file_path = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return f'{self.id}'

    def get_dir_name(self):
        return os.path.join(os.path.dirname(self.test_case.file_path), 'runs')

    def save(self):
        self.create_datetime = Now()
        self.status = self.TestRunStatus.INIT
        super(TestRun, self).save()
        self.execute()

    def execute(self):
        self.start_datetime = Now()
        output_dir = os.path.join(self.get_dir_name(), str(self.id))
        storage = FileSystemStorage()

        test_case_content = self.test_case.get_content_from_file()
        content_file = ContentFile(test_case_content)
        test_case_file_path = os.path.join(output_dir, 'sources', 'test_case.robot')
        abs_test_case_file_path = os.path.join(settings.MEDIA_ROOT, test_case_file_path)
        storage.save(abs_test_case_file_path, content_file)

        argument_set_content = self.argument_set.get_content_from_file()
        environment_set_content = self.environment.get_content_from_file()

        content_file = ContentFile(argument_set_content + '\n' + environment_set_content)
        argument_set_file_path = os.path.join(output_dir, 'sources', 'argument_set.yaml')
        abs_argument_set_file_path = os.path.join(settings.MEDIA_ROOT, argument_set_file_path)
        storage.save(abs_argument_set_file_path, content_file)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        abs_output_dir = os.path.join(settings.MEDIA_ROOT, output_dir)

        try:
            robot_exec(test_case_file=abs_test_case_file_path, argument_file=abs_argument_set_file_path,
                       output_directory=abs_output_dir)
            self.report_file_path = os.path.join(output_dir, 'report.html')
            self.test_log_file_path = os.path.join(output_dir, 'log.html')
            self.status = self.TestRunStatus.COMPLETED
        except Exception as e:
            print(f'Error in run test case: {e}')
            self.status = self.TestRunStatus.FAILED
        finally:
            self.stop_datetime = Now()
        super(TestRun, self).save()

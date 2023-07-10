from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

# new
class Post(models.Model):
    title = models.CharField(max_length=30) # Post 제목
    hook_text = models.CharField(max_length=100, blank=True) # 요약본
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자는 추후 작성예정

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):  # 페이지 생성시 페이지 번호 매기는 함수
        return f'[{self.pk}]{self.title}::{self.author}'

    def get_absolute_url(self): # 상세페이지 접속 시 번호를 찾아주는 함수
        return f'/blog/{self.pk}/'

    def get_file_name(self):    # 파일 이름 가져오기
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): # 파일 맨뒤에 있는 확장자 가져오기
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    # 게시글이 지워지면 같이 지우기
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글을 입력했을 때 당시의 시간을 기록
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
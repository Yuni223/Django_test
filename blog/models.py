from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# new
class Post(models.Model):
    title = models.CharField(max_length=30) # Post 제목
    hook_text = models.CharField(max_length=100, blank=True) # 요약본
    content = models.TextField() # Post 내용

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자는 추후 작성예정
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):  # 페이지 생성시 페이지 번호 매기는 함수
        return f'[{self.pk}]{self.title}::{self.author}'

    def get_absolute_url(self): # 상세페이지 접속 시 번호를 찾아주는 함수
        return f'/blog/{self.pk}/'

    def get_file_name(self):    # 파일 이름 가져오기
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): # 파일 맨뒤에 있는 확장자 가져오기
        return self.get_file_name().split('.')[-1]
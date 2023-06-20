from django.db import models

# Create your models here.

# new
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자는 추후 작성예정

    def __str__(self):  # 페이지 생성시 페이지 번호 매기는 함수
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self): # 상세페이지 접속 시 번호를 찾아주는 함수
        return f'/blog/{self.pk}/'

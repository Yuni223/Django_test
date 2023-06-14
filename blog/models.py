from django.db import models

# Create your models here.

# new
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자는 추후 작성예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'

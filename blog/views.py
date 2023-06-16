from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'    # 최신 글을 맨 위로
    # template_name = 'blog/index.html'
    # index.html 을 지정못해서 template_name 을 통해서 강제로 주소 지정

# def index(request):
#     posts = Post.objects.all().order_by('-pk')    # 최신 글을 맨 위로
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )


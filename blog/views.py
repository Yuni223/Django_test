from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'    # 최신 글을 맨 위로
    
    def get_context_data(self, **keargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    # template_name = 'blog/index.html'
    # index.html 을 지정못해서 template_name 을 통해서 강제로 주소 지정
    # return render와 같은 의미

# def index(request):
#     posts = Post.objects.all().order_by('-pk')    # 최신 글을 맨 위로
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )

class PostDetail(DetailView):
    model = Post

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
#

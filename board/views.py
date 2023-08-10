from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Board
from .forms import BoardForm

# Create your views here.

class BoardCreate(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(BoardCreate, self).form_valid(form)

            return response
        else:
            return redirect('/board/')


class BoardDetail(DetailView):
    model = Board


class BoardList(ListView):
    model = Board
    ordering = '-pk'
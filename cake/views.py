from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, Category, Tag
from django.db.models import F
from django.core.mail import send_mail
from .forms import ContactForm


class Home(ListView):
    model = Post
    template_name = 'cake/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Торты на заказ'
        return context


class PostsByCategory(ListView):
    template_name = 'cake/index.html'
    context_object_name = 'posts'
    paginate_by = 6
    allow_empty = False  # при запросе путстой категории выдает ошибку 404

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'cake/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False  # при запросе путстой категории выдает ошибку 404

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'cake/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):  # чтобы увеличить количество просмотров
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()  # берем данные views из бд т.к. в переменной выражение
        return context


class Search(ListView):
    template_name = 'cake/search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):  # чтобы увеличить количество просмотров
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"  # передаем еще одну переменную для пагинации
        return context


class AboutDostavka(TemplateView):
    template_name = 'cake/dostavka.html'
    context_object_name = 'dostavka'


def ContactForms(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'testmysited@rambler.ru',
                      ['mihavxd@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('/contactforms/')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'cake/contact.html/', {"form": form})

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View, generic
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_app.serializers import PostSerializer
from .forms import *
from django.contrib import messages
from .models import *
from test_check import parser_crypto

class HomeView(View):

    # Данные по ценам крипты приходят в файле test_check.py
    def get(self, request):
        data = parser_crypto()
        return render(request, 'blog_app/home.html', context={'data': data})


def cryptocurrency_prices(request):
    cryptocurrency_data = parser_crypto()
    return JsonResponse(cryptocurrency_data)


class PostView(View):
    template_name = 'blog_app/posts.html'
    form_class = FilterPostForm

    def get(self, request):
        form = self.form_class
        posts = Post.objects.all()
        return render(request, self.template_name, context={'posts': posts, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            astronomy = form.cleaned_data.get('astronomy')
            philosophy = form.cleaned_data.get('philosophy')
            marketing = form.cleaned_data.get('marketing')
            data = {'form': form}

            z = {Post.objects.filter(cat_id=1): astronomy, Post.objects.filter(cat_id=2): philosophy, Post.objects.filter(cat_id=3): marketing}
            check_true = []
            for key, val in z.items():
                check_true.append(val)
                if val:
                    data['posts'].append(key)  # не понимаю блять как раскрыть список состоящий из QuerySet
                    # Ниже рабочий вариант, но не правильный
                    #data['posts'] = key  # значение просто перезаписывается, а нужно чтобы добавлялось
                    #data[f'{key.cat.cat_name}'] = key
                else:
                    continue
            if all(x == False for x in check_true):  # если ничего не отмечено, то возвращаются все посты!
                data['posts'] = Post.objects.all()
            print(data)

            """if astronomy:
                posts = Post.objects.filter(cat_id=1)
                data['posts'] = posts
            elif marketing:
                posts = Post.objects.filter(cat_id=3)
                data['posts'] = posts
            elif philosophy:
                posts = Post.objects.filter(cat_id=2)
                data['posts'] = posts
            else:
                posts = Post.objects.all()
                data['posts'] = posts"""
            return render(request, self.template_name, context=data)




# УДАЛИТЬ ЭТУ НАДПИСЬ
# В итоге разобрался с тем, что все представления кроме регистрации уже
# определены в django.contrib.auth.views там же и находится модель к которой нужно обращатся

class RegisterView(View):
    template_name = 'registration/register.html'
    form_class = CustomRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_home')
        # если условие не выполняется, то вызываем метод dispatch, который изначально определен во View
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():  # также тут проверяется есть ли пользователь с таким же email
            user = form.save()
            # после успешного сохранения используем функцию login
            # она устанавливает сеанс пользователя позволяя быть аутентифицированным на сайте
            login(request, user)
            return redirect('login')
        return render(request, self.template_name, context={'form': form})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)



#--------------------Настройка API проекта ------------------------------------------------------------
class BlogAPIView(APIView):

    def get(self, request, pk=None, format=None):
        if pk:
            post = Post.objects.get(pk=pk)
            return Response({'post': PostSerializer(post).data})
        else:
            lst = Post.objects.all()
            return Response({'posts': PostSerializer(lst, many=True).data})

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        transformer = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(transformer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        transformer = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(transformer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transformer = get_object_or_404(Post, pk=pk)
        transformer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



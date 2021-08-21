from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transcript, Meeting

from .tasks import video2audio


class MainView(LoginRequiredMixin, View):
    login_url = '/auth'
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        meetings = Meeting.objects.all()

        return render(request, self.template_name, {'meetings': meetings})


class AutenticationView(View):
    template_name = 'core/auth.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template_name, context={'username': username, 'error_message': 'Неверный логин и пароль'})


class UploadVideoView(View):
    template_name = 'core/upload.html'

    def get(self, request, *args, **kwargs):
        print("GET UPLOAD")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print("POST UPLOAD")
        print(request.FILES)
        print(request.POST)
        file = request.FILES.get('file', None)
        if file:
            trans = Transcript(video_file=file, name=file._get_name()[:-4])
            trans.save()
            video2audio.apply_async(args=[trans.id])
        return render(request, self.template_name)

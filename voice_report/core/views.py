from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Meeting, User, EmployeeRolesInMeeting
from .tasks import video2audio
import uuid


class MainView(LoginRequiredMixin, View):
    login_url = '/auth'
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        meetings = Meeting.objects.all().order_by('-date')
        users = User.objects.all()
        return render(request, self.template_name, {'meetings': meetings, 'users': users})


class NotFoundView(View):
    template_name = 'core/404.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        redirect('auth')

    def get(self, request):
        logout(request)
        return redirect('auth')


class MeetingPrintView(LoginRequiredMixin, View):
    template_name = 'core/print.html'

    def get(self, request, meeting_id):
        meeting = Meeting.objects.get(pk=meeting_id)
        return render(request, self.template_name, {'meeting': meeting})


class MeetingPrintExtView(View):
    template_name = 'core/print.html'

    def get(self, request, uid):
        roles = EmployeeRolesInMeeting.objects.filter(report_url='/meeting_print_ext/'+uid)[0]
        roles.report_read = True
        roles.save()
        meeting = roles.meeting
        user = roles.employee
        return render(request, self.template_name, {'meeting': meeting, 'user': user})


class MeetingDetailView(LoginRequiredMixin, View):
    template_name = 'core/meetingDetail.html'

    def get(self, request, meeting_id):
        meeting = Meeting.objects.get(pk=meeting_id)
        users = User.objects.all()
        return render(request, self.template_name, {'meeting': meeting, 'users': users})


class MeetingSend(LoginRequiredMixin, View):
    def get(self, request, meeting_id):
        # эмуляция отрпавки писем
        roles_meeting = Meeting.objects.get(pk=meeting_id).roles_in_meeting.all()
        for role in roles_meeting:
            role.report_send = True;
            role.save()
        return redirect('main')


class AddMeettingView(LoginRequiredMixin, View):
    login_url = '/auth'

    def post(self, request, *args, **kwargs):
        date = request.POST.get('date', None)
        meeting = Meeting(
            status=0,
            theme=request.POST.get('theme', ''),
            date=request.POST.get('date', None),
            agenda='',
        )
        meeting.save()
        meeting_employee = EmployeeRolesInMeeting(
            meeting=meeting,
            role=2,
            employee=User.objects.get(pk=int(request.POST.get('memberPred', 1))),
            report_url='/meeting_print_ext/'+str(uuid.uuid1())
        )
        meeting_employee.save()
        meeting_employee = EmployeeRolesInMeeting(
            meeting=meeting,
            role=1,
            employee=User.objects.get(pk=int(request.POST.get('memberSekret', 1))),
            report_url='/meeting_print_ext/'+str(uuid.uuid1())
        )
        meeting_employee.save()
        members = request.POST.getlist('members', None)
        for member_id in members:
            meeting_employee = EmployeeRolesInMeeting(
                meeting=meeting,
                role=0,
                employee=User.objects.get(pk=int(member_id)),
                report_url='/meeting_print_ext/'+str(uuid.uuid1())
            )
            meeting_employee.save()
        file = request.FILES.getlist('record', None)[0]
        if file:
            meeting.video_file = file
            meeting.save()
            video2audio.apply_async(args=[meeting.id])
        return redirect('main')


class AutenticationView(View):
    template_name = 'core/auth.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template_name, context={'username': username, 'error_message': 'Неверный логин и пароль'})

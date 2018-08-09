# coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import json
from .forms import UpdateImageForm
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, UserInfoForm
from .models import UserProfile, Banner
from utils.send_email import send_register_email
from users.models import EmailVerityCode
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import CourseOrg, Course
from organization.models import Teacher
from pure_pagination import PageNotAnInteger, Paginator


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户或密码错误'})
    elif request.method == 'GET':
            return render(request, 'login.html')

    """实现用户账号或密码错误分别提醒"""
    #   try:
    #       user_is_existed = UserProfile.objects.get(Q(username=username) | Q(email=username))
    #       user = authenticate(username=username, password=password)
    #       if user:
    #           login(request, user)
    #           return render(request, 'index.html')
    #       else:
    #           return render(request, 'login.html', {'msg': '密码错误'})
    #       except Exception as e:
    #           return render(request, 'login.html', {'msg': '用户不存在'})
    #   elif request.method == 'GET':
    #       return render(request, 'login.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerityCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# class SendEmailView(View):
#     def post(self, request):
#         return render(request, 'send_active_email.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {'msg': '用户不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        records = EmailVerityCode.objects.filter(code=reset_code)
        if records:
            for record in records:
                email = record.email
            return render(request, 'password_reset.html', {'email': email})


class ModiftyView(View):
    def post(self, request):
        reset_form = ModifyForm(request.POST)
        if reset_form.is_valid():
            email = request.POST.get('email', '')
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'user_info'
        return render(request, 'usercenter-info.html', {
            'current_page': current_page,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UpdateImageView(LoginRequiredMixin, View):
    """
    修改用户头像
    """
    def post(self, request):
        image_form = UpdateImageForm(request.POST, request.FILES, instance=request.user)
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdatePWDView(LoginRequiredMixin, View):
    """
    个人中心修改密码
    """
    def post(self, request):
        reset_form = ModifyForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')
        else:
            send_register_email(email, send_type='update_email')
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_record = EmailVerityCode(email=email, code=code, send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCoursesView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'mycourses'
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
            "current_page": current_page,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_records = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_records:
            org_id = fav_org.fav_id
            org_list.append(CourseOrg.objects.get(id=int(org_id)))
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_records = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_org in fav_records:
            course_id = fav_org.fav_id
            course_list.append(Course.objects.get(id=int(course_id)))
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_records = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_org in fav_records:
            teacher_id = fav_org.fav_id
            teacher_list.append(Teacher.objects.get(id=int(teacher_id)))
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyMessageView(View):
    def get(self, request):
        current_page = 'mymessage'
        user_messages = UserMessage.objects.filter(user=request.user.id)
        for user_message in user_messages:
            user_message.has_read = True
            user_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_messages, 1, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'current_page': current_page,
            'messages': messages,

        })


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

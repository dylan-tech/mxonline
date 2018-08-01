# coding:utf-8

from django.shortcuts import render

# Create your views here.
from .models import Course, CourseResource
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator
from django.http import HttpResponse
from operation.models import UserFavorite, CourseComments, UserCourse
from courses.models import Video
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CoursesView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        sort = request.GET.get('sort', '')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        objects = all_courses
        p = Paginator(objects, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tags = course.tags
        if tags:
            relate_courses = Course.objects.filter(tags__contains=tags, )[:2]
        else:
            relate_courses = []

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        course_users = UserCourse.objects.filter(course=course)
        all_user_ids = [usercourse.id for usercourse in course_users]
        all_relate_courses = UserCourse.objects.filter(user_id__in=all_user_ids)
        course_ids = [relate_course.course.id for relate_course in all_relate_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        all_recourse = CourseResource.objects.filter(id=int(course.id))
        return render(request, 'course-video.html', {
            'course': course,
            'all_recourse': all_recourse,
            'relate_courses': relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_recourse = CourseResource.objects.filter(id=int(course.id))
        all_comments = CourseComments.objects.all()
        course_users = UserCourse.objects.filter(course=course)
        course_ids = [user_id.course.id for user_id in course_users]
        relate_courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_recourse': all_recourse,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        user_courses = UserCourse.objects.filter(course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        course_users = UserCourse.objects.filter(course=course)
        all_user_ids = [usercourse.id for usercourse in course_users]
        all_relate_courses = UserCourse.objects.filter(user_id__in=all_user_ids)
        course_ids = [relate_course.course.id for relate_course in all_relate_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        all_recourse = CourseResource.objects.filter(id=int(course.id))
        return render(request, 'course-play.html', {
            'course': course,
            'all_recourse': all_recourse,
            'relate_courses': relate_courses,
            'video': video
        })
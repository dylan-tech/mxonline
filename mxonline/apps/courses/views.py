# coding:utf-8

from django.shortcuts import render

# Create your views here.
from .models import Course
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator


class CoursesView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        sort = request.GET.get('sort', '')
        hot_courses = all_courses.order_by('-click_nums')[:3]

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

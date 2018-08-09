# coding:utf-8
__author__ = 'Dylan'

import xadmin
from models import Course, CourseResource, Lesson, Video, IsBannerCourse
from xadmin import views


class LessonInline(object):
    model = Lesson
    extra = 0


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = u'慕学后台管理'
    site_footer = u'慕学在线学习'
    menu_style = 'accordion'


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                   'click_nums', 'add_time']

    ordering = ['-click_nums']
    # exclude = ['fav_nums']

    inlines = [LessonInline]
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, *args, **kwargs)


class IsBannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                   'click_nums', 'add_time']

    ordering = ['-click_nums']
    # exclude = ['fav_nums']

    inlines = [LessonInline]

    def queryset(self):
        qs = super(IsBannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['video', 'name', 'add_time']
    search_fields = ['video', 'name']
    list_filter = ['video__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(IsBannerCourse, IsBannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

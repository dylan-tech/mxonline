# coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from organization.models import CourseOrg, CityDict
from pure_pagination import Paginator, PageNotAnInteger


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()
        city_id = request.GET.get('city', '')

        # 城市
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类型
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        orgs_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        objects = all_orgs
        p = Paginator(objects, 5, request=request)
        orgs = p.page(page)
        # return render(request, 'org-list.html', {'all_orgs':all_orgs, 'all_cities':all_cities, 'orgs_nums':orgs_nums})
        return render(request, 'org-list.html', {
            'orgs': orgs,
            'all_cities': all_cities,
            'orgs_nums': orgs_nums,
            'city_id': city_id,
            'category': category,
        })

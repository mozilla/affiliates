from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import DetailView

from affiliates.banners.models import Category
from affiliates.links.models import Link


def index(request):
    return render(request, 'statistics/index.html', {
        'total_link_clicks': Link.objects.total_link_clicks(),
        'total_link_count': Link.objects.count(),
        'total_user_count': User.objects.count(),
        'categories': (Category.objects
                       .filter(level=1)
                       .order_by('parent__name', 'name')),
    })


class CategoryDetailView(DetailView):
    queryset = Category.objects.filter(level=1)
    template_name = 'statistics/category.html'
    context_object_name = 'category'

    def get_context_data(self, **context):
        context['banners'] = self.object.banners(prefetch=['variation_set'])
        return super(CategoryDetailView, self).get_context_data(**context)

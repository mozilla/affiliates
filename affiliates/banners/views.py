from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from affiliates.banners.models import Category


class CategoryListView(ListView):
    """List root categories and their subcategories."""
    queryset = Category.objects.root_nodes()
    template_name = 'banners/generator/categories.html'
    context_object_name = 'categories'


class BannerListView(ListView):
    """List banners available in a given category."""
    template_name = 'banners/generator/banners.html'
    context_object_name = 'banners'

    def dispatch(self, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['category_pk'])
        return super(BannerListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.category.imagebanner_set.all()

    def get_context_data(self, **context):
        context['category'] = self.category
        return super(BannerListView, self).get_context_data(**context)

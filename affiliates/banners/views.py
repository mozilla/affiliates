import json

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, FormView

from braces.views import LoginRequiredMixin

from affiliates.banners.forms import CustomizeImageBannerForm
from affiliates.banners.models import Category, ImageBanner


class CategoryListView(LoginRequiredMixin, ListView):
    """List root categories and their subcategories."""
    queryset = Category.objects.root_nodes()
    template_name = 'banners/generator/categories.html'
    context_object_name = 'categories'


class BannerListView(LoginRequiredMixin, ListView):
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


class CustomizeBannerView(LoginRequiredMixin, FormView):
    """Base class for views for customizing banners."""
    banner_class = None

    def dispatch(self, *args, **kwargs):
        self.banner = get_object_or_404(self.banner_class, pk=kwargs['pk'])
        return super(CustomizeBannerView, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        # Pass banner as first argument to this view's customization
        # form.
        return form_class(self.banner, **self.get_form_kwargs())

    def form_valid(self, form):
        link = self.banner.create_link(self.request.user, **form.cleaned_data)
        return redirect(link)


class CustomizeImageBannerView(CustomizeBannerView):
    """Display and process form for customizing an image banner."""
    banner_class = ImageBanner
    form_class = CustomizeImageBannerForm
    template_name = 'banners/generator/customize/image_banner.html'

    def get_context_data(self, **context):
        # JSON object containing data on available variations.
        variations = {}
        for variation in self.banner.variation_set.all():
            variations[variation.pk] = {
                'locale': variation.locale,
                'color': variation.color,
                'size': variation.size,  # <- Why we can't use serialize.
                'image': variation.image.url
            }
        context['variations_json'] = json.dumps(variations)

        return super(CustomizeImageBannerView, self).get_context_data(**context)

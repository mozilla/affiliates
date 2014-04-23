import json

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, FormView

from braces.views import LoginRequiredMixin

from affiliates.banners.forms import CustomizeImageBannerForm, CustomizeTextBannerForm
from affiliates.banners.models import Category, FirefoxUpgradeBanner, ImageBanner, TextBanner
from affiliates.base.utils import locale_to_native


_has_banners_q = (Q(imagebanner__visible=True) | Q(textbanner__visible=True) |
                  Q(firefoxupgradebanner__visible=True))


class CategoryListView(LoginRequiredMixin, ListView):
    """List all categories."""
    queryset = (Category.objects
                .filter(_has_banners_q, level=1)
                .distinct()
                .order_by('parent__name', 'name'))
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
        return (list(self.category.imagebanner_set.filter(visible=True)) +
                list(self.category.textbanner_set.filter(visible=True)) +
                list(self.category.firefoxupgradebanner_set.filter(visible=True)))

    def get_context_data(self, **context):
        context['category'] = self.category
        return super(BannerListView, self).get_context_data(**context)


class CustomizeBannerView(LoginRequiredMixin, FormView):
    """Base class for views for customizing banners."""
    banner_class = None

    def dispatch(self, *args, **kwargs):
        self.banner = get_object_or_404(self.banner_class, pk=kwargs['pk'], visible=True)
        return super(CustomizeBannerView, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        # Pass banner as first argument to this view's customization
        # form.
        return form_class(self.banner, **self.get_form_kwargs())

    def form_valid(self, form):
        link = self.banner.create_link(self.request.user, form.cleaned_data['variation'])
        return redirect(link.get_absolute_url() + '?generator=1')

    def get_context_data(self, **context):
        context['banner'] = self.banner
        return super(CustomizeBannerView, self).get_context_data(**context)


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
                'locale': locale_to_native(variation.locale),
                'color': variation.color,
                'size': variation.size,  # <- Why we can't use serialize.
                'image': variation.image.url
            }
        context['variations_json'] = json.dumps(variations)

        return super(CustomizeImageBannerView, self).get_context_data(**context)


class CustomizeTextBannerView(CustomizeBannerView):
    """Display and process form for customizing a text banner."""
    banner_class = TextBanner
    form_class = CustomizeTextBannerForm
    template_name = 'banners/generator/customize/text_banner.html'

    def get_context_data(self, **context):
        # Add JSON object containing text for each variation.
        variations_text = dict([(v.pk, v.text) for v in self.banner.variation_set.all()])
        context['variations_text_json'] = json.dumps(variations_text)
        return super(CustomizeTextBannerView, self).get_context_data(**context)


class CustomizeFirefoxUpgradeBannerView(CustomizeImageBannerView):
    banner_class = FirefoxUpgradeBanner

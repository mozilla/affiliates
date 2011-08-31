from django.contrib.auth.decorators import login_required

from badges.views import dashboard


@login_required(redirect_field_name='')
def about(request):
    return dashboard(request, 'shared/about.html')


@login_required(redirect_field_name='')
def faq(request):
    return dashboard(request, 'shared/faq.html')

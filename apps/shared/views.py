from badges.views import dashboard
from shared.decorators import login_required


@login_required
def about(request):
    return dashboard(request, 'shared/about.html')


@login_required
def faq(request):
    return dashboard(request, 'shared/faq.html')

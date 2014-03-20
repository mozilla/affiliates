from django.shortcuts import redirect
from django.views.generic import UpdateView

from affiliates.users.forms import EditProfileForm
from affiliates.users.models import UserProfile


class UserProfileView(UpdateView):
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def post(self, request, *args, **kwargs):
        # Only allow editing of the user if you are logged in as the
        # current user.
        profile = self.get_object()
        if request.user != profile.user:
            # TODO: Add some sort've error message here.
            return redirect(profile)
        else:
            return super(UserProfileView, self).post(request, *args, **kwargs)

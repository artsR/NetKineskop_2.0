from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden



class TagUserPermission(UserPassesTestMixin, LoginRequiredMixin):

    def test_func(self):
        tag = self.get_object()
        return tag.user_id == self.request.user.id

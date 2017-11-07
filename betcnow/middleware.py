from .models import Profile


class CheckWinner(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.show_notification = False

    def __call__(self, request):
        response = self.get_response(request)
        self.show_notification = False
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            if p.premio:
                self.show_notification = True
        return response

    def process_template_response(self, request, response):
        if self.show_notification:
            response.context_data['show_notification'] = True
        return response
from django.http import HttpResponse
from django.views import View


class manage_formulas_view(View):
    template_name = 'company/displayCard.html'

    def get(self, request):
        # <view logic>
        return render(request, self.template_name, {})

    def get_object(self):
        return 

from django.shortcuts import render


def view_404(request,exception):
    return render(request,'company/errors/404.html')

def view_500(request):
    return render(request,'company/errors/500.html')

from django.shortcuts import render
import os

def base_view(request):
    context={"api_hostname_from_django":f"http://{os.environ.get('hostname')}:{os.environ.get('webappport')}"}
    return render(request,"index.html",context)


def custom_404(request, exception):
    context={"api_hostname_from_django":f"http://{os.environ.get('hostname')}:{os.environ.get('webappport')}"}
    return render(request, '404.html', context, status=404)

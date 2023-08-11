from django.shortcuts import render
import os

def base_view(request):
    context={"api_hostname_from_django":f"http://{os.environ.get('hostname')}:8000"}
    return render(request,"index.html",context)
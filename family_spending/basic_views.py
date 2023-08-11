from django.shortcuts import render

def base_view(request):
    context={"api_hostname_from_django":"http://localhost:8000"}
    return render(request,"index.html",context)
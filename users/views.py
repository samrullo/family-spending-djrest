from django.shortcuts import render

# Create your views here.
def account_profile(request):
    return render(request,"account_profile.html",context={"username":request.user.username})

def account_signup(request):
    return render(request,"account_signup.html")
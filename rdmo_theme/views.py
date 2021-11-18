from django.shortcuts import redirect, render

def impressum(request):
    return render(request, 'rdmo_theme/impressum.html')

def privacy_policy(request):
    return render(request, 'rdmo_theme/privacy_policy.html')

def FAQs(request):
    return render(request, 'rdmo_theme/FAQs.html')

def quickstart(request):
    return render(request, 'rdmo_theme/quickstart.html')

def login_form_sso(request):
    return render(request, 'rdmo_theme/login_form_sso.html')
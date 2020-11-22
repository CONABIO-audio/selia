from django.shortcuts import render


def about_selia(request):
    return render(request, 'selia_about/selia.html')

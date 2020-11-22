from django.shortcuts import render


def about_collections(request):
    return render(request, 'selia_about/collections.html')

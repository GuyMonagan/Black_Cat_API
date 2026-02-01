from django.shortcuts import render

def easter_egg(request):
    return render(request, "easter_egg.html")

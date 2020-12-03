from django.shortcuts import render

def home(request):

    return render(request,'index.html')


def about(request):

    return render(request,'pages/about.html')
def handler404(request, exception):
    
    return render(request,"errors/404.html",status = 404)  
from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')
# Create your views here.
def producto(request):
    return render(request, 'core/producto.html')

def html_registro(request):
    return render(request, 'core/formularioRegistro.html')

def html_login(request):
    return render(request, 'core/formularioLogin.html')
from django.http import HttpResponse

def index(request):
    param = request.GET.get('name_param', None)
    return HttpResponse(f'Hello, World! {param}') # http://127.0.0.1:8000/web?name_param=test
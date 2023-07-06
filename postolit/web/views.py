from django.http import HttpResponse
from django.shortcuts import render
from web.forms import RegForm


def index(request):
    param = request.GET.get('name_param', None)
    return HttpResponse(f'Hello, World! {param}') # http://127.0.0.1:8000/web?name_param=test


def index_2(request, id):
    print(id)
    return HttpResponse(f'Hello, World! {id}')


def reg(request):
    form = RegForm(request.POST or None) # None - это GET-запрос (просто загружаем страницу), request.POST - отправляем форму
    message = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            message = f'{email} {password} Вы успешно зарегистрировались'

    context = {
        'form': form,
        'message': message
    }
    return render(request, template_name='reg.html', context=context)
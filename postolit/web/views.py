from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from web.forms import RegForm, LoginForm
from postolit.clickhouse import create_connection
from .clickhouse_models import Vedomost3
from .models import User#, Session
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout # <Для аутентификации с помощью сессий (встроенной в Django)>
from django.contrib.sessions.backends.db import SessionStore


def index(request):
    param = request.GET.get('name_param', None)
    return HttpResponse(f'Hello, World! {param}') # http://127.0.0.1:8000/web?name_param=test


def index_2(request, id):
    print(id)
    return HttpResponse(f'Hello, World! {id}')

db = create_connection()


def clickhouse_test(request):
    # Получаем значение по параметру type , иначе берем None   
    operation = request.GET.get('type', None)
    message = None
    result = None
    if operation:
        # Добавление данных в таблицу (для таблиц, которую мы создали в моделях django)
        if operation == 'insert_new':
            db.insert([Vedomost3(ID_C=1, ID_D=2, ID_P=3, Otsenka=5)])
            message = 'Операция добавления прошла успешно !'
        elif operation == 'update_new':
        # Обновление данных (для таблиц, которую мы создали в моделях django)
        # (недоступно обновление первичного ключа)
            obj = Vedomost3.objects_in(db).filter(ID_C=1, ID_D=2, ID_P=3, Otsenka=5).update(ID_P=4, Otsenka=3)
            message = 'Операция обновления прошла успешно !'
        #print(obj)
        elif operation == 'delete_new':
            result = Vedomost3.objects_in(db).filter(ID_C=1, ID_D=2, ID_P=4, Otsenka=3).delete()
            message = 'Операция удаления прошла успешно !'
        elif operation == 'select_filter_new':
        # Получение данных по фильтру (для таблиц, которую мы создали в моделях django)
            result = Vedomost3.objects_in(db).filter(ID_C=123,ID_D=123)
            #for row in result:
                #print(row.ID_C, row.ID_D, row.ID_P, row.Otsenka)
        elif operation == 'select_new':
        # Обычный SELECT (для таблиц, которую мы создали в моделях django)
            result = Vedomost3.objects_in(db)
            #for row in result:
                #print(row.ID_C, row.ID_P)
        elif operation == 'select_old':
            # SELECT - Выполнение SQL запроса (!!! для ранее созданных таблиц - вне django)
            result = db.select('SELECT * FROM Vedomost1')
            # for row in result:
            #  print(row.ID_C, row.ID_D, row.ID_P, row.Otsenka)
        elif operation == 'insert_old':
             # Добавление данных в таблицу (!!! для ранее созданных таблиц - вне django)
            result = db.raw('INSERT INTO Vedomost1(ID_C, ID_D, ID_P, Otsenka) VALUES(1001, 1001, 1001, 5) ')
            message = 'Операция добавления прошла успешно !'
        elif operation == 'update_old_1':
            # Обновление строк (!!! для ранее созданных таблиц - вне django)
            #ALTER TABLE [db.]table [ON CLUSTER cluster] UPDATE column1 = expr1 [, ...] WHERE filter_expr
            result = db.raw('ALTER TABLE test.Vedomost1 UPDATE ID_P = 500 WHERE ID_C = 1001')
            message = 'Операция обновления прошла успешно !'
        elif operation == 'delete_old':
            # Удаление строк (!!! для ранее созданных таблиц - вне django)
            result = db.raw('ALTER TABLE Vedomost1 DELETE WHERE ID_C=1001')
            message = 'Операция удаления прошла успешно !'
        return render(request, "click.html", {'objects': result, 'message': message})

    else: # если get-парраметр type не передан, то отображаем данные новой таблицы
        result = Vedomost3.objects_in(db)
        #result = db.select('SELECT * FROM Vedomost1')
        #for row in result:
        #       print(row.ID_C, row.ID_D, row.ID_P, row.Otsenka)
        return render(request, "click.html", {'objects': result})

    # db.raw() - !!! для выполнения любого SQL-запроса в ClickHouse для существующих таблиц, кроме SELECT (для SELECT db.select)


def reg(request):
    form = RegForm(request.POST or None) # None - это GET-запрос (просто загружаем страницу), request.POST - отправляем форму
    message = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # <Для аутентификации с помощью сессий (НЕ встроенной в Django)>
            #name = form.cleaned_data['name']
            #User.objects.create(login=email, password=password, name=name) # создаем пользователя в базе данных

            # <Для аутентификации с помощью сессий (встроенной в Django)>
            User.objects.create_user(username=email, password=password, email=email)

            print(email, password)
            message = f'{email} {password} Вы успешно зарегистрировались'
    context = {
        'form': form,
        'message': message
    }
    return render(request, template_name='reg.html', context=context)

# <Для аутентификации с помощью сессий (НЕ встроенной в Django)>
'''def do_login(log_user, password): # Функция для создания аутентификации пользователя и создания сессии для пользователя
    try:
        user = User.objects.get(login=log_user) # Проверяем на наличие ползователя в базе по email
    except User.DoesNotExist:
        return None
    if user.password != password: # Проверяем на соответствие пароля в базе
        return None

    session = Session() # Создаем объект сессии для пользователя
    session.key = get_random_string(32) # Генерируем ключ сессии
    session.user = user # Привязываем пользователя
    session.expires = datetime.now() + timedelta(days=1) # Устанавливаем время жизни сессии
    session.save() # Сохраняем объект сессии
    return session'''

def login_view(request):
    error = ''
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():            
            password = form.cleaned_data['password']

            # <Для аутентификации с помощью сессий (НЕ встроенной в Django)>
            #login = form.cleaned_data['email']
            #session = do_login(login, password) # Получаем объект сессии

            # <Для аутентификации с помощью сессий (встроенной в Django)>
            email = form.cleaned_data['email']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('web')
            else:
                error = "Неверный логин или пароль" 

            # <Для аутентификации с помощью сессий (НЕ встроенной в Django)>
            '''url = request.POST.get('continue', 'web') # адрес для редиректа
            response = redirect(url)
            if session: # Если пользователь аутентифицирован
                response = HttpResponseRedirect(url) # Создаем ответ в виде редиректа на адрес
                # Устанавливаем cookies с name = session_id (Создаем ключ сессии на стороне клиента (в браузере))
                response.set_cookie('session_id', session.key, domain='127.0.0.1', httponly=True, expires=session.expires)
                return response
            else:
                error = "Неверный логин или пароль"'''

    return render(request, "login.html", {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def anonymous_session(request): # Например, anonymous_session - точка входа в ваше веб-приложение,
# в этой функции сохраняем в базу какие-либо данные о текущем, еще не авторизованном пользователе,
# далее используем эти данные в своих целях  
    session_key = request.COOKIES.get('sessionid') # Извлекаем id сессии пользователя из cookies
    if not session_key: # Если его нет, то создаем новую сессию
        session = SessionStore()
        session.save()
        session_key = session.session_key
    session = SessionStore(session_key=session_key) # Извлекаем объект сессии из базы данных
    session['anonymous_data'] = 'Some My Data' # Устанавливаем какие-то данные для сессии текущего анонимного пользователя
    session.save() # Сохраняем
    response = render(request, 'anonymous.html') # Создаем ответ для пользователя
    response.set_cookie('sessionid', session_key, httponly=True) # Устанавливаем в cookies ответа ключ sessionid
    return response
def anonymous_page(request): # Последующая страница после anonymous_session, теперь можем использовать данные,
    # которые установили в точке входа(anonymous_session)
    session_key = request.COOKIES.get('sessionid') # Извлекаем id сессии пользователя из cookies
    session = SessionStore(session_key=session_key) # Извлекаем объект сессии из базы данных
    anonymous_data = session.get('anonymous_data') # Извлекаем данные об анонимном пользователе, которые создали для текущей сессии
    print(anonymous_data)
    return render(request, 'anonymous.html', {'anonymous_data': anonymous_data})
from django.http import HttpResponse

def home():
    html = f"""
    <html>
        <head><title>Главная страница</title></head>
        <body>
            <h1>Главная страница</h1>
            <ul>
                <li><a href="{('/admin')}">Админка</a></li>
                <li><a href="{('/users')}">Пользователи</a></li>
                <li><a href="{('/grades')}">Оценки</a></li>
                <li><a href="{('/schedules')}">Расписание</a></li>
            </ul>
        </body>
    </html>
    """
    return HttpResponse(html)
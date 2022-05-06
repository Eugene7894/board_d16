from django.apps import AppConfig


class BoardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board_app'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми
    # функциями обработчиками
    def ready(self):
        import board_app.signals
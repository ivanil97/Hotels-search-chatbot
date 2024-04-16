from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('user_requests.db')


class BaseModel(pw.Model):
    """
    Класс BaseModel является таблицей для хранения запросов пользователей

    Атрибуты
    -------
    created_at: время и дата создания записи в таблице

    """
    created_at = pw.DateTimeField(default=datetime.now())

    class Meta:
        database = db


class RequestHistory(BaseModel):
    """
    Класс RequestHistory является дочерним от BaseModel и устанавливает столбцы в базе данных

    Атрибуты
    -------
    user_id: id пользователя
    user_name: никнейм пользователя
    request_type: название функции, которую вызвал пользователь (low, high, custom)
    request_body: краткое описание запроса
    hotels: сериализованный json-словарь с данными по отелям, найденным в рамках запроса

    """
    user_id = pw.TextField()
    user_name = pw.TextField()
    request_type = pw.TextField()
    request_body = pw.TextField()
    hotels = pw.TextField()

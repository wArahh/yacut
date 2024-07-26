import os
import string

UNEXPECTED_NAME = 'Указано недопустимое имя для короткой ссылки'
TOO_MANY_ATTEMPTS = (
    'Было потрачено слишком много попыток на генерацию short'
)
URL_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
MUST_SET_REQUIRED_FIELD = '{must_set} является обязательным полем!'
REQUEST_IS_NONE = 'Отсутствует тело запроса'
URL_NOT_EXISTS = 'Указанный id не найден'
SHORT_ALREADY_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
BANNED_SYMBOLS_USED = 'Нельзя использовать запрещенные символы'
ORIGINAL_LINK = 'Ссылка на страницу'
CUSTOM_ID = 'Желаемая ссылка'
REQUIRED_FIELD = 'Обязательное поле!'
URLFIELD_ONLY = 'Поле для ссылки!'
ACCEPT = 'Добавить'
DB_ERROR = 'При добавлении в базу данных произошла ошибка: {error}'
MAX_ORIGINAL_LENGTH = 1024
MAX_SHORT_LENGTH = 16
SHORT_BASE_LENGTH = 6
MAX_ATTEMPTS = 10
BASE_URL = os.getenv('BASE_URL', 'http://localhost/')
ACCEPTED_SYMBOLS = string.ascii_letters + string.digits
REGEXP_ACCEPTED_SYMBOLS = f'^[{ACCEPTED_SYMBOLS}]*$'

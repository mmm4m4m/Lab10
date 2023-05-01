class CustomException(BaseException):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return f'Исключение {self.__class__.__name__}: "{self.message}"'


class NotUniqueUsernameException(CustomException):
    pass


class PasswordCheckException(CustomException):
    pass


class UserIsNotAuthenticatedException(CustomException):
    pass


class User:
    users = {}

    def __init__(self, username, password):
        self.__username, self.__password = self.get_username_password(str(username), str(password))
        self.__authenticated = False

    def authenticate(self, password):
        if self.__password != str(password):
            raise PasswordCheckException('Пароль введен неверно, попробуйте его восстановить')
        self.__authenticated = True

    def get_username_password(self, username, password):
        if username in self.users:
            raise NotUniqueUsernameException('Такое имя уже существует')
        self.users[username] = password
        return username, password

    def check_auth(self):
        if not self.__authenticated:
            raise UserIsNotAuthenticatedException('Пользователь не авторизован, чтобы совершить это действие')


class Site:
    def register(self):
        try:
            username, password = input('Введите имя пользователя: '), input('Введите пароль: ')
            user = User(username, password)
            return user
        except NotUniqueUsernameException as e:
            print(e)

    def login(self, user: User):
        tries = 3
        while True:
            try:
                password = input('Введите пароль: ')
                user.authenticate(password)
            except PasswordCheckException as e:
                if tries == 1:
                    print(e)
                    break
                tries -= 1
                print(f'Пароль неверный, осталось попыток: {tries}')
            else:
                print('Вы успешно авторизовались')
                break

    def add_new_note(self, user: User):
        try:
            user.check_auth()
        except UserIsNotAuthenticatedException as e:
            print(e)
        else:
            print('Добавление новой записи')


if __name__ == '__main__':
    google_keep = Site()

    first_user = google_keep.register()
    second_user = google_keep.register() # В случае, если имя пользователя совпадает с уже существующим (first_user) - Исключение NotUniqueUsernameException: "Такое имя уже существует"

    google_keep.add_new_note(first_user) # Исключение UserIsNotAuthenticatedException: "Пользователь не авторизован, чтобы совершить это действие"

    google_keep.login(first_user) # Если 3 раза введен неверный пароль - Исключение PasswordCheckException: "Пароль введен неверно, попробуйте его восстановить"

    google_keep.add_new_note(first_user) # На этот раз ошибки не будет

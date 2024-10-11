# pylint: disable=too-few-public-methods
class BaseDescriptor:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate(value)  # Вызов метода для проверки значения
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут.")

    def validate(self, value):
        raise NotImplementedError("Подклассы должны реализовать этот метод!")


class PositiveInteger(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'''
                    Ожидалось целое число, получено {type(value).__name__}
            ''')
        if value < 0:
            raise ValueError("Значение должно быть положительным целым числом.")


class PositiveNumber(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Ожидалось число, получено {type(value).__name__}")
        if value < 0:
            raise ValueError("Значение должно быть положительным числом.")


class PoolLength(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Ожидалось число, получено {type(value).__name__}")
        if value <= 0:
            raise ValueError("Длина бассейна должна быть положительным числом.")


class NonEmptyString(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'''
                Ожидалась строка, получено {type(value).__name__}
            ''')
        if not value.strip():
            raise ValueError("Имя не должно быть пустым.")


class SwimmingStats:
    pools_count = PositiveInteger()
    pool_length = PoolLength()
    time = PositiveNumber()
    swimmer_name = NonEmptyString()

    def __init__(self, swimmer_name, pools_count, time, pool_length=25):
        self.swimmer_name = swimmer_name
        self.pools_count = pools_count
        self.pool_length = pool_length
        self.time = time

    @property
    def distance(self):
        return self.pools_count * self.pool_length

    @property
    def speed(self):
        if self.time == 0:
            return 0
        return self.distance / self.time

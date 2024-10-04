class CustomList(list):
    def __init__(self, *args):
        super().__init__(args[0] if args else [])

    # метод вывода
    def __str__(self):
        return f"Элементы списка: {list(self)}. Сумма: {sum(self)}"

    # методы сложения
    def __add__(self, other):
        result = []
        if isinstance(other, (list, CustomList)):
            max_len = max(len(self), len(other))
            for i in range(max_len):
                if i < len(self) and i < len(other):
                    result.append(self[i] + other[i])
                elif i < len(self):
                    result.append(self[i] + 0)
                else:
                    result.append(0 + other[i])

        elif isinstance(other, int):
            for i, value in enumerate(self):
                result.append(value + other)
        else:
            return NotImplemented
        return CustomList(result)

    def __radd__(self, other):
        return self.__add__(other)

    # методы вычитания
    def __sub__(self, other):
        result = []
        if isinstance(other, (list, CustomList)):
            max_len = max(len(self), len(other))
            for i in range(max_len):
                if i < len(self) and i < len(other):
                    result.append(self[i] - other[i])
                elif i < len(self):
                    result.append(self[i] - 0)
                else:
                    result.append(0 - other[i])

        elif isinstance(other, int):
            for i, value in enumerate(self):
                result.append(value - other)
        else:
            return NotImplemented
        return CustomList(result)

    def __rsub__(self, other):
        result = []
        if isinstance(other, list):
            max_len = max(len(self), len(other))
            for i in range(max_len):
                if i < len(self) and i < len(other):
                    result.append(other[i] - self[i])
                elif i < len(self):
                    result.append(0 - self[i])
                else:
                    result.append(other[i] - 0)

        elif isinstance(other, int):
            for i, value in enumerate(self):
                result.append(other - value)
        else:
            return NotImplemented
        return CustomList(result)

    # методы сравнения
    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        return NotImplemented

class CustomMeta(type):
    def __new__(mcs, name, bases, dct):
        custom_dct = {}
        for attr_name, attr_value in dct.items():
            if attr_name.startswith("__"):
                custom_dct[attr_name] = attr_value
            else:
                custom_dct[f"custom_{attr_name}"] = attr_value

        def custom_setattr(instance, attr_name, attr_value):
            if attr_name.startswith("__"):
                object.__setattr__(instance, attr_name, attr_value)
            else:
                object.__setattr__(instance, f"custom_{attr_name}", attr_value)

        instance = super().__new__(mcs, name, bases, custom_dct)
        instance.__setattr__ = custom_setattr

        return instance


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

# pylint: disable=too-few-public-methods
import cProfile
import time
import weakref
from io import StringIO
import pstats


class TypecalInfo:
    def __init__(self, serial_number, age, vendor, model):
        self.serial_number = serial_number
        self.age = age
        self.vendor = vendor
        self.model = model


class Device:
    def __init__(self, name, info):
        self.name = name
        self.info = info


class SlottedDevice:
    __slots__ = ('name', 'info')

    def __init__(self, name, info):
        self.name = name
        self.info = info


class WeakRefDevice:
    def __init__(self, name, info):
        self.name = name
        self._info = weakref.ref(info)

    @property
    def info(self):
        return self._info()

    @info.setter
    def info(self, value):
        self._info = weakref.ref(value)


def create_device_instances(cur_cls, count):
    return [cur_cls(f"SN{i}",
                    TypecalInfo(100 * i,
                                2 * i,
                                f"vendor{i}",
                                f"model{3 * i}")) for i in range(count)]


def measure_time(func, *args, **kwargs):
    start_time = time.perf_counter()
    func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time


def test_device_access(instances):
    for instance in instances:
        _ = instance.name
        _ = instance.info


def test_device_modify(instances):
    for instance in instances:
        instance.name = "NewName"
        instance.info = TypecalInfo(100,
                                    2,
                                    "vendor_updated",
                                    "model_updated")


# Запуск профилирования
profiler = cProfile.Profile()
profiler.enable()

device_results = {}
DEVICE_INSTANCE_COUNT = 500_000

# Измерение времени на создание экземпляров
for cls, cls_name in [(Device, "Device"),
                      (SlottedDevice, "SlottedDevice"),
                      (WeakRefDevice, "WeakRefDevice")]:
    creation_time = measure_time(
        create_device_instances,
        cls, DEVICE_INSTANCE_COUNT)
    device_results[f"{cls_name}_instance_creation"] = creation_time

# Предсоздание экземпляров для следующих экспериментов
device_instances = create_device_instances(Device, DEVICE_INSTANCE_COUNT)
slotted_device_instances = create_device_instances(SlottedDevice,
                                                   DEVICE_INSTANCE_COUNT)
weakref_device_instances = create_device_instances(WeakRefDevice,
                                                   DEVICE_INSTANCE_COUNT)

# Измерение времени на чтение
device_access_time = measure_time(test_device_access, device_instances)
slotted_device_access_time = measure_time(test_device_access,
                                          slotted_device_instances)
weakref_device_access_time = measure_time(test_device_access,
                                          weakref_device_instances)

# Измерение времени на изменение
device_modify_time = measure_time(test_device_modify, device_instances)
slotted_device_modify_time = measure_time(test_device_modify,
                                          slotted_device_instances)
weakref_device_modify_time = measure_time(test_device_modify,
                                          weakref_device_instances)

# Запись результатов
device_results["Device_access"] = device_access_time
device_results["SlottedDevice_access"] = slotted_device_access_time
device_results["WeakRefDevice_access"] = weakref_device_access_time
device_results["Device_modify"] = device_modify_time
device_results["SlottedDevice_modify"] = slotted_device_modify_time
device_results["WeakRefDevice_modify"] = weakref_device_modify_time

profiler.disable()

# Печать профиля
s = StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
ps.print_stats()
print(s.getvalue())

# Выводим результаты
print(device_results)

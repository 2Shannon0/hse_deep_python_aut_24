# pylint: disable=no-member
import unittest
from metaclass import CustomClass


class TestCustomClass(unittest.TestCase):
    def test1_custom_x(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

    def test2_instance_attributes(self):
        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError):
            _ = inst.x

        with self.assertRaises(AttributeError):
            _ = inst.val

        with self.assertRaises(AttributeError):
            inst.line()

    def test3_dynamic_attribute(self):
        inst = CustomClass()
        inst.dynamic = "added later"

        self.assertEqual(inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError):
            _ = inst.dynamic

    def test4_non_existent_attribute(self):
        inst = CustomClass()
        with self.assertRaises(AttributeError):
            _ = inst.yyy

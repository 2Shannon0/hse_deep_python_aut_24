import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test1_customlist_plus_customlist(self):
        self.assertEqual(
            CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]),
            CustomList([6, 3, 10, 7])
        )

    def test2_customlist_plus_list(self):
        self.assertEqual(
            CustomList([10]) + [1, 2, 7],
            CustomList([11, 2, 7])
        )

    def test3_list_plus_customlist(self):
        self.assertEqual(
            [1, 2, 7] + CustomList([10]),
            CustomList([11, 2, 7])
        )

    def test4_customlist_minus_customlist(self):
        self.assertEqual(
            CustomList([5, 1, -3, 7]) - CustomList([1, 2, 7]),
            CustomList([4, -1, -10, 7])
        )

    def test5_customlist_minus_list(self):
        self.assertEqual(
            CustomList([10]) - [1, 2, 7],
            CustomList([9, -2, -7])
        )

    def test6_list_minus_customlist(self):
        self.assertEqual(
            [1, 2, 7] - CustomList([10]),
            CustomList([-9, 2, 7])
        )

    def test7_customlist_plus_int(self):
        self.assertEqual(
            CustomList([1, 2, 7]) + 12,
            CustomList([13, 14, 19])
        )

    def test8_int_plus_customlist(self):
        self.assertEqual(
            100 + CustomList([-10, 20, 15]),
            CustomList([90, 120, 115])
        )

    def test9_int_plus_empty_customlist(self):
        self.assertEqual(
            100 + CustomList([]),
            CustomList([])
        )

    def test10_customlist_minus_int(self):
        self.assertEqual(
            CustomList([1, 12, 57]) - 12,
            CustomList([-11, 0, 45])
        )

    def test11_int_minus_customlist(self):
        self.assertEqual(
            100 - CustomList([-10, 20, 15]),
            CustomList([110, 80, 85])
        )

    def test12_str_minus_customlist(self):
        with self.assertRaises(TypeError):
            _ = '100' + CustomList([-10, 20, 15])

    def test13_comparisons(self):
        self.assertFalse(CustomList([]) == CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([1, 2, 3]))

        self.assertFalse(CustomList([1, 2, 3]) != CustomList([1, 2, 3]))
        self.assertTrue(CustomList([1, 2]) != CustomList([1, 2, 3]))

        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, -20]) >= CustomList([1, 2, 3]))

        self.assertTrue(CustomList([1, 2, 4]) > CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, 2]) > CustomList([1, 2, 3]))

        self.assertTrue(CustomList([2, 3]) < CustomList([1, 2, 3]))
        self.assertFalse(CustomList([2, 30]) < CustomList([1, 2, 3]))

        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([1, 2, 3]))
        self.assertFalse(CustomList([1, 2, 4]) <= CustomList([1, 2, 3]))

    def test14_str_method(self):
        cl = CustomList([1, 2, 3, 4])
        expected_output = "Элементы списка: [1, 2, 3, 4]. Сумма: 10"
        self.assertEqual(str(cl), expected_output)

        cl_empty = CustomList()
        expected_output_empty = "Элементы списка: []. Сумма: 0"
        self.assertEqual(str(cl_empty), expected_output_empty)

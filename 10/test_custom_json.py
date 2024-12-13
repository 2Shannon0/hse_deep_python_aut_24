import unittest
import json
import custom_json


class TestCustomJson(unittest.TestCase):

    def test0_compare_with_py_json(self):
        json_str = '{"hello": 10, "world": "value"}'

        json_doc = json.loads(json_str)
        cust_json_doc = custom_json.loads(json_str)

        assert json_doc == cust_json_doc
        assert json_str == custom_json.dumps(custom_json.loads(json_str))

    def test1_loads_valid(self):
        json_str = '{"hello": 10, "world": "value"}'
        expected_result = {"hello": 10, "world": "value"}
        result = custom_json.loads(json_str)
        self.assertEqual(result, expected_result)

    def test2_loads_invalid(self):
        invalid_json_str = '{"hello": 10, "world": }'
        with self.assertRaises(TypeError):
            custom_json.loads(invalid_json_str)

    def test3_dumps_valid(self):
        obj = {"hello": 10, "world": "value"}
        expected_result = '{"hello": 10, "world": "value"}'
        result = custom_json.dumps(obj)
        self.assertEqual(result, expected_result)

    def test4_dumps_unsupported_value(self):
        obj = {"hello": 10, "unsupported": [1, 2, 3]}
        with self.assertRaises(TypeError):
            custom_json.dumps(obj)

    def test5_load_and_dump(self):
        json_str = '{"key1": 123, "key2": "string value"}'
        parsed = custom_json.loads(json_str)
        serialized = custom_json.dumps(parsed)
        self.assertEqual(json_str, serialized)


if __name__ == "__main__":
    unittest.main()

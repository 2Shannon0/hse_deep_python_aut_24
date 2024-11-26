import unittest
from generator import generate


class TestGenerator(unittest.TestCase):

    def test1_file_name(self):
        outputs = list(generate("./01/1-input.txt", ['груша'], ['банан']))
        self.assertEqual(outputs, [
            'яблоко апеЛьсин Груша арбуз Еда комплекс бизнес\n',
            'рыба карась игра Началась груша\n'
            ])

    def test2_file_object(self):
        with open("./01/1-input.txt", "r", encoding='UTF-8') as file:
            outputs = list(generate(file, ['груша'], ['банан']))
        self.assertEqual(outputs, [
            'яблоко апеЛьсин Груша арбуз Еда комплекс бизнес\n',
            'рыба карась игра Началась груша\n'
            ])

    def test2_2_file_object_empty_result(self):
        with open("./01/2-input.txt", "r", encoding='UTF-8') as file:
            outputs = list(generate(file, ['яблоко'], ['груша']))
        self.assertEqual(outputs, [])

    def test3_3_three_serach_words(self):
        outputs = list(generate("./01/3-input.txt",
                                ['банан', 'арбуз', 'яблоко'],
                                ['ананас']))
        self.assertEqual(outputs, ['арбуз банан яблоко груша\n',
                                   'ДОООМ яблоКО\n',
                                   'бананный баНан\n'])

    def test4_line_is_search_word(self):
        outputs = list(generate("./01/4-input.txt", ['арбуз'], ['банан']))
        self.assertEqual(outputs, ['арбуз ананас виноград\n',
                                   'арбуз\n', 'арбуз сад\n'])

    def test4__1_stop_word_is_search_word(self):
        outputs = list(generate("./01/4-input.txt", ['арбуз'], ['арбуз']))
        self.assertEqual(outputs, [])

    def test5_line_is_stop_word(self):
        outputs = list(generate("./01/5-input.txt", ['яблоко'], ['банан']))
        self.assertEqual(outputs, ['яблоко ананас арбуз\n'])

    def test6_stop_word_is_line(self):
        outputs = list(generate("./01/6-input.txt",
                                ['груша'],
                                ['сад дом храм', 'банан']))
        self.assertEqual(outputs, ['груша арбуз ананас яблоко\n',
                                   'сад дом храм груша арбуз ананас яблоко\n'])

    def test7_search_word_is_line(self):
        outputs = list(generate("./01/6-input.txt",
                                ['сад дом храм'],
                                ['банан']))
        self.assertEqual(outputs, [])

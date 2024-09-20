import unittest
from generator import generate


class TestGenerator(unittest.TestCase):

    def test1(self):
        outputs = []
        for line in generate("./1-input.txt", ['груша'], ['банан']):
            outputs.append(line)
        self.assertEqual(outputs, [
            'яблоко апеЛьсин Груша арбуз Еда комплекс бизнес\n'
            ])

    def test2(self):
        outputs = []
        for line in generate("./2-input.txt", ['яблоко'], ['груша']):
            outputs.append(line)
        self.assertEqual(outputs, [])

    def test3(self):
        outputs = []
        for line in generate("./3-input.txt", ['банан'], ['ананас']):
            outputs.append(line)
        self.assertEqual(outputs, ['арбуз банан яблоко груша\n'])

    def test4(self):
        outputs = []
        for line in generate("./4-input.txt", ['арбуз'], ['банан']):
            outputs.append(line)
        self.assertEqual(outputs, ['арбуз ананас виноград\n'])

    def test5(self):
        outputs = []
        for line in generate("./5-input.txt", ['яблоко'], ['банан']):
            outputs.append(line)
        self.assertEqual(outputs, ['яблоко ананас арбуз\n'])

    def test6(self):
        outputs = []
        for line in generate("./6-input.txt", ['яблоко'], ['банан']):
            outputs.append(line)
        self.assertEqual(outputs, ['груша арбуз ананас яблоко\n'])

import unittest

#run via terminal: python3 -m unittest
class FooTest(unittest.TestCase):
    def test_bar1(self):
        def add(a, b):
            return a + b
        
        self.assertEqual(5, add(2,3)) 
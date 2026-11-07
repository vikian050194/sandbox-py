import unittest

# python -m unittest discover -s . -p "test_*.py" -v
# python -m unittest -v test_foo
# python -m unittest test_foo.TestFoo.test_bar1
class TestFoo(unittest.TestCase):
    def test_bar1(self):
        def add(a, b):
            return a + b
        
        self.assertEqual(5, add(2,3)) 
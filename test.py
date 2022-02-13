import unittest
from main import main, setTesting

@setTesting(2, 2)
def summ(a, b):
    return a + b

class MaitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.main = main(["time", "memory"], "hTable")

    def test_testingFunctions(self):
        pass

if __name__ == "__main__":
    unittest.main()
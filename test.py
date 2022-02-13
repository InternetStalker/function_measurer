import unittest
from main import main, setTesting

@setTesting(2, 2)
def summ(a, b):
    return a + b

class MaitTest(unittest.TestCase):
    possibleOutputMods = "hTable vTable"

    def setUp(self) -> None:
        self.main = main(["time", "memory"], "hTable")

    def test_testingFunctions(self):
        self.assertNotEqual(self.main.testingFunctions, [])

    def testLoad(self):
        self.main.importScript("script")
        self.assertNotEqual(self.main.testingFunctions, [summ])

    def test_res(self):
        with self.subTest("Testing tests..."):
            for key in self.main.res:
                self.assertIn(key, self.possibleOutputMods, f"Key: {key}...")

if __name__ == "__main__":
    unittest.main()
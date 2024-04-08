import os
import unittest
import sys

with open("results.csv", "w") as results_file:
    results_file.write("name, test, error \n")


for file in os.scandir():
    name = file.name
    if name[-3:] == ".py" and name != "__init__.py" and name != "mass_tester.py":
        module = name[:-3]
        try:
            # because we want to import using a variable, do it this way
            module_obj = __import__(module)
            # create a global object containing our module
            globals()[module] = module_obj
        except ImportError:
            sys.stderr.write("ERROR: missing python module: " + module + "\n")
            sys.exit(1)


        class MyTestResult(unittest.TestResult):
            def addFailure(self, test, err):
                with open("results.csv", "a") as results_file:
                    results_file.write(f"{module}, {test}, {err} \n")
                super(MyTestResult, self).addFailure(test, err)

            def addError(self, test, err):
                with open("results.csv", "a") as results_file:
                    results_file.write(f"{module}, {test}, {err} \n")
                super(MyTestResult, self).addError(test, err)

        class TestCalc(unittest.TestCase):
            def test_example(self):
                if "test_example" in module:
                    self.assertEqual(module_obj.example_function("example input"), "example output")
                    self.assertEqual(module_obj.example_function("input"), "output")
                else:
                    with open("results.csv", "a") as results_file:
                        results_file.write(f"{module}, ""messing func"" \n")
                    self.fail("No function with the name test_example")

        if __name__ == '__main__':
            unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult), exit=False)

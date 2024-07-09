import os
import unittest
import sys

# Create or overwrite the results.csv file and write the header
with open("results.csv", "w") as results_file:
    results_file.write("name, test, error \n")

# Scan the current directory for Python files
modules = []
for file in os.scandir():
    name = file.name
    # Check if the file is a Python file, excluding __init__.py and the current script
    if name.endswith(".py") and name not in ["__init__.py", "mass_tester.py"]:
        module = name[:-3]  # Remove the .py extension to get the module name
        modules.append(module)
        try:
            # Import the module dynamically using __import__
            module_obj = __import__(module)
            # Make the module available globally
            globals()[module] = module_obj
        except ImportError:
            # If the module cannot be imported, log the error and exit
            sys.stderr.write("ERROR: missing python module: " + module + "\n")
            sys.exit(1)


# Custom test result class to log failures and errors to results.csv
class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        with open("results.csv", "a") as results_file:
            results_file.write(f"{test}, {err} \n")
        super(MyTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        with open("results.csv", "a") as results_file:
            results_file.write(f"{test}, {err} \n")
        super(MyTestResult, self).addError(test, err)


# Dynamically create test cases for each module
def create_test_case(module_name, module_obj):
    class TestModule(unittest.TestCase):
        # Define new tests here
        # Each test method should start with 'test_'

        def test_example_function(self):
            # Check if the module has the function example_function
            if hasattr(module_obj, "example_function"):
                # Test case 1: example_function should return 'example output' for input 'example input'
                self.assertEqual(module_obj.example_function("example input"), "example output")
                # Test case 2: example_function should return 'output' for input 'input'
                self.assertEqual(module_obj.example_function("input"), "output")
            else:
                # If the function is missing, log it and fail the test
                with open("results.csv", "a") as results_file:
                    results_file.write(f"{module_name}, missing func\n")
                self.fail(f"No function with the name example_function in {module_name}")

    # Set the name of the test case class
    TestModule.__name__ = f"Test{module_name.capitalize()}"
    return TestModule


# Load all test cases into a test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

for module in modules:
    module_obj = globals()[module]
    test_case = create_test_case(module, module_obj)
    suite.addTests(loader.loadTestsFromTestCase(test_case))

# Run the tests
if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=MyTestResult)
    runner.run(suite)

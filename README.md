# Mass Tester

This project is designed to dynamically discover and test all Python modules in the current directory, excluding specified files. The results of the tests, including any errors or failures, are logged into a `results.csv` file.

## How It Works

1. The script scans the current directory for Python files.
2. It dynamically imports each module and applies a predefined test to all modules.
3. If a module cannot be imported, an error message is printed to `stderr` and the script exits.
4. Test results are logged to `results.csv`, including the name of the module, the test, and any errors.

## Getting Started

### Prerequisites

- Python 3.x
- `unittest` module (included in the Python Standard Library)

### Running the Script

1. Place `mass_tester.py` in the directory containing the Python modules you want to test.
2. Run the script using Python:

    ```bash
    python mass_tester.py
    ```

3. Check the `results.csv` file for the test results.

## Creating New Tests

To apply new tests to all modules, modify the `create_test_case` function in `mass_tester.py`:

```python
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

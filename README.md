# Automated Test Case Generation

This project implements automated test case generation techniques for two case studies: a Quadratic Equation Solver and a Date Format Converter. The implementation compares Z3-solver and Category-Partition testing techniques in terms of code coverage, mutation testing, and execution performance.

## Project Overview

This project was developed for SYSC 5807 - Automated Test Case Generation course at Carleton University, Winter 2025. It demonstrates the application of formal test generation techniques to produce effective test cases with high coverage and fault detection capabilities.

### Implemented Testing Techniques

1. **Z3-Solver Based Test Generation**
   - Uses the Z3 constraint solver to generate test cases based on mathematical constraints
   - Applied to the Quadratic Equation Solver case study
   - Systematically generates test cases covering different scenarios (real roots, complex roots, etc.)

2. **Category-Partition Testing**
   - Divides input parameters into categories and applies constraints
   - Applied to the Date Format Converter case study
   - Creates test frames by combining parameter values systematically

### Case Studies

1. **Quadratic Equation Solver**
   - Solves equations of the form ax² + bx + c = 0
   - Handles various scenarios: real roots, complex roots, and special cases
   - Tested with Z3-solver generated test cases

2. **Date Format Converter**
   - Converts dates between different formats (YYYY-MM-DD to DD/MM/YYYY and vice versa)
   - Handles valid and invalid dates, including leap year considerations
   - Tested with Category-Partition generated test cases

## Project Structure

```
+-- data/                           # Test case data storage
+-- reports/                        # Test reports and visualizations
¦   +-- visualizations/             # Charts and visualizations
¦   +-- summary_report.html         # Comprehensive test results report
+-- src/
¦   +-- case_studies/               # Implementation of case studies
¦   ¦   +-- date_converter.py       # Date format converter implementation
¦   ¦   +-- quadratic_solver.py     # Quadratic equation solver implementation
¦   +-- test_generation/            # Test generation implementations
¦       +-- category_partition.py   # Category-Partition test generator
¦       +-- z3_solver.py            # Z3-solver based test generator
+-- tests/                          # Test implementations
¦   +-- test_date_converter.py      # Tests for date converter
¦   +-- test_quadratic_solver.py    # Tests for quadratic solver
+-- utils/                          # Utility modules
¦   +-- coverage_analysis.py        # Code coverage analysis
¦   +-- mutation_analysis.py        # Mutation testing analysis
¦   +-- visualization.py            # Result visualization utilities
+-- main.py                         # Main execution script
```

## Prerequisites

- Python 3.8 or higher
- Required Python packages:
  - z3-solver
  - matplotlib
  - numpy
  - pandas
  - seaborn
  - coverage
  - mutmut (optional, for mutation testing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/automated-test-generation.git
   cd automated-test-generation
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script to generate test cases and perform analysis:
   ```bash
   python main.py
   ```

2. The script will:
   - Generate test cases using Z3-solver for the quadratic equation solver
   - Generate test cases using Category-Partition for the date converter
   - Run the test cases and collect coverage data
   - Perform mutation testing
   - Generate visualizations and a summary report

3. View the results in the `reports` directory:
   - `reports/summary_report.html` for a comprehensive report
   - `reports/visualizations/` for individual charts and visualizations

## Test Generation Process

### Z3-Solver for Quadratic Equation

The Z3-solver test generator (`src/test_generation/z3_solver.py`) works by:

1. Defining mathematical constraints for different scenarios (real distinct roots, real identical roots, complex roots, etc.)
2. Using the Z3 constraint solver to find values of a, b, and c that satisfy these constraints
3. Generating a balanced set of test cases covering different quadratic equation scenarios

### Category-Partition for Date Converter

The Category-Partition test generator (`src/test_generation/category_partition.py`) works by:

1. Identifying categories for date components (year, month, day) and conversion directions
2. Specifying choices for each category (e.g., leap years, month lengths, format directions)
3. Generating test frames by combining choices from different categories
4. Applying constraints to filter out invalid combinations
5. Adding specific test cases for edge cases and error conditions

## Analysis Tools

1. **Coverage Analysis**
   - Uses Python's `coverage` package to measure line and branch coverage
   - Generates HTML and JSON reports for detailed coverage information

2. **Mutation Testing**
   - Uses `mutmut` to introduce small changes (mutations) to the code
   - Measures how many mutations are detected (killed) by the test suite
   - Higher mutation scores indicate more effective tests

3. **Visualization**
   - Creates charts showing test case distribution, coverage results, and mutation scores
   - Generates a comprehensive HTML report comparing the techniques

## Results

The project evaluates and compares the effectiveness of Z3-solver and Category-Partition techniques based on:

- Number of generated test cases
- Code coverage (line and branch)
- Mutation score (fault detection capability)
- Execution time

The summary report (`reports/summary_report.html`) provides detailed information about the comparison results.

## Key Findings

- Both techniques achieve high code coverage (>90% line coverage)
- Category-Partition generates more test cases but provides more thorough coverage of edge cases
- Z3-solver is particularly effective for the mathematical domain of quadratic equations
- Both techniques achieve good mutation scores (~85%)

## License

[MIT License](LICENSE)

## Acknowledgements

This project was developed for SYSC 5807 - Automated Test Case Generation at Carleton University.

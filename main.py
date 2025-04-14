import os
import sys
import time
import importlib.util

# Add the project root to the path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the required modules for test generation and analysis
from src.test_generation.z3_solver import Z3TestGenerator
from src.test_generation.category_partition import CategoryPartitionTestGenerator
from utils.mutation_analysis import MutationAnalyzer
from utils.coverage_analysis import CoverageAnalyzer
from utils.visualization import Visualizer

def ensure_directories():
    """Create necessary directories"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('reports/visualizations', exist_ok=True)

def generate_test_cases():
    """Generate test cases using both techniques"""
    print("Generating test cases...")
    
    # Generate quadratic equation test cases using Z3
    z3_generator = Z3TestGenerator(os.path.join('data', 'quadratic_test_cases.csv'))
    z3_test_cases = z3_generator.generate_quadratic_test_cases()
    print(f"Generated {len(z3_test_cases)} test cases for quadratic equation using Z3")
    
    # Generate date conversion test cases using Category-Partition
    cp_generator = CategoryPartitionTestGenerator(os.path.join('data', 'date_test_cases.csv'))
    cp_test_cases = cp_generator.generate_date_conversion_test_cases()
    print(f"Generated {len(cp_test_cases)} test cases for date conversion using Category-Partition")
    
    return z3_test_cases, cp_test_cases

def analyze_quadratic_test_cases(test_cases):
    """Analyze the generated quadratic equation test cases"""
    scenarios = {}
    for case in test_cases:
        scenario = case['scenario']
        if scenario not in scenarios:
            scenarios[scenario] = 0
        scenarios[scenario] += 1
    
    print("Quadratic equation test case distribution:")
    for scenario, count in scenarios.items():
        print(f"  - {scenario}: {count} cases ({count/len(test_cases)*100:.1f}%)")

def analyze_date_test_cases(test_cases):
    """Analyze the generated date conversion test cases"""
    valid_count = sum(1 for case in test_cases if case['expected_output'] != "ValueError")
    invalid_count = len(test_cases) - valid_count
    
    print("Date conversion test case distribution:")
    print(f"  - Valid dates: {valid_count} cases ({valid_count/len(test_cases)*100:.1f}%)")
    print(f"  - Invalid dates: {invalid_count} cases ({invalid_count/len(test_cases)*100:.1f}%)")
    
    directions = {"iso_to_dmy": 0, "dmy_to_iso": 0}
    for case in test_cases:
        direction = case['format_direction']
        directions[direction] += 1
    
    print("Conversion direction distribution:")
    for direction, count in directions.items():
        print(f"  - {direction}: {count} cases ({count/len(test_cases)*100:.1f}%)")

def run_tests_and_analysis():
    """Run tests and analyze the results"""
    print("\n*** Starting test execution and analysis ***")
    
    # Create analyzers
    mutation_analyzer = MutationAnalyzer()
    coverage_analyzer = CoverageAnalyzer()
    visualizer = Visualizer()
    
    # Dictionaries to store results for visualization
    coverage_results = {}
    mutation_results = {}
    coverage_times = {}
    mutation_times = {}
    
    try:
        # Analyze quadratic solver
        print("\n=== Quadratic Solver Analysis ===")
        print("Running coverage analysis...")
        quadratic_coverage = coverage_analyzer.run_coverage_analysis(
            "src.case_studies.quadratic_solver",
            "tests.test_quadratic_solver"
        )
        
        # Store results for visualization
        coverage_results["src.case_studies.quadratic_solver"] = quadratic_coverage
        coverage_times["src.case_studies.quadratic_solver"] = quadratic_coverage.get('execution_time', 0)
        
        if quadratic_coverage.get('success', False):
            print(f"Coverage analysis completed successfully")
            if 'coverage_data' in quadratic_coverage and quadratic_coverage['coverage_data']:
                print(f"Line coverage: {quadratic_coverage['coverage_data'].get('line_coverage', 0):.2f}%")
                print(f"Branch coverage: {quadratic_coverage['coverage_data'].get('branch_coverage', 0):.2f}%")
        else:
            print(f"Coverage analysis failed: {quadratic_coverage.get('error', 'Unknown error')}")
        
        print("\nRunning mutation testing...")
        quadratic_mutation = mutation_analyzer.run_mutation_testing(
            "src.case_studies.quadratic_solver",
            "tests.test_quadratic_solver"
        )
        
        # Store results for visualization
        mutation_results["src.case_studies.quadratic_solver"] = quadratic_mutation
        mutation_times["src.case_studies.quadratic_solver"] = quadratic_mutation.get('execution_time', 0)
        
        if quadratic_mutation.get('success', False):
            print(f"Mutation testing completed successfully")
            print(f"Mutation score: {quadratic_mutation.get('mutation_score', 0):.2f}%")
        else:
            print(f"Mutation testing failed: {quadratic_mutation.get('error', 'Unknown error')}")
        
        # Analyze date converter
        print("\n=== Date Converter Analysis ===")
        print("Running coverage analysis...")
        date_coverage = coverage_analyzer.run_coverage_analysis(
            "src.case_studies.date_converter",
            "tests.test_date_converter"
        )
        
        # Store results for visualization
        coverage_results["src.case_studies.date_converter"] = date_coverage
        coverage_times["src.case_studies.date_converter"] = date_coverage.get('execution_time', 0)
        
        if date_coverage.get('success', False):
            print(f"Coverage analysis completed successfully")
            if 'coverage_data' in date_coverage and date_coverage['coverage_data']:
                print(f"Line coverage: {date_coverage['coverage_data'].get('line_coverage', 0):.2f}%")
                print(f"Branch coverage: {date_coverage['coverage_data'].get('branch_coverage', 0):.2f}%")
        else:
            print(f"Coverage analysis failed: {date_coverage.get('error', 'Unknown error')}")
        
        print("\nRunning mutation testing...")
        date_mutation = mutation_analyzer.run_mutation_testing(
            "src.case_studies.date_converter",
            "tests.test_date_converter"
        )
        
        # Store results for visualization
        mutation_results["src.case_studies.date_converter"] = date_mutation
        mutation_times["src.case_studies.date_converter"] = date_mutation.get('execution_time', 0)
        
        if date_mutation.get('success', False):
            print(f"Mutation testing completed successfully")
            print(f"Mutation score: {date_mutation.get('mutation_score', 0):.2f}%")
        else:
            print(f"Mutation testing failed: {date_mutation.get('error', 'Unknown error')}")
        
        # Create visualizations
        print("\n=== Generating Visualizations ===")
        visualizer.plot_coverage_comparison(coverage_results)
        visualizer.plot_mutation_scores(mutation_results)
        visualizer.plot_execution_times(coverage_times, mutation_times)
        
    except Exception as e:
        print(f"\nError during test run: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\nAll analyses completed. Reports and visualizations saved in the 'reports' directory.")
    
    return coverage_results, mutation_results, coverage_times, mutation_times

def main():
    """Main execution function"""
    start_time = time.time()
    
    print("=== Automated Test Case Generation Project ===")
    
    # Ensure directories exist
    ensure_directories()
    
    # Create visualizer
    visualizer = Visualizer()
    
    # Generate test cases
    test_cases = generate_test_cases()
    quadratic_cases = test_cases[0]
    date_cases = test_cases[1]
    
    # Summarize test case generation results
    print("\n=== Test Case Generation Summary ===")
    print(f"Total quadratic equation test cases: {len(quadratic_cases)}")
    print(f"Total date conversion test cases: {len(date_cases)}")
    
    # Analyze test cases
    print("\n=== Test Case Analysis ===")
    analyze_quadratic_test_cases(quadratic_cases)
    analyze_date_test_cases(date_cases)
    
    # Create visualizations for test case distributions
    print("\nGenerating test case distribution visualizations...")
    visualizer.plot_test_case_distribution(quadratic_cases, case_type='quadratic')
    visualizer.plot_test_case_distribution(date_cases, case_type='date')
    visualizer.plot_test_case_distribution(date_cases, case_type='date', category_field='format_direction')
    
    # Run tests and analysis
    coverage_results, mutation_results, coverage_times, mutation_times = run_tests_and_analysis()
    
    # Create a comprehensive summary report
    print("\n=== Creating Summary Report ===")
    test_gen_data = {
        'quadratic_count': len(quadratic_cases),
        'date_count': len(date_cases)
    }
    execution_data = {
        'total_time': time.time() - start_time
    }
    
    report_path = visualizer.create_summary_report(
        test_gen_data, 
        coverage_results, 
        mutation_results, 
        execution_data
    )
    
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print(f"Project execution completed. Summary report available at: {report_path}")

if __name__ == "__main__":
    main()
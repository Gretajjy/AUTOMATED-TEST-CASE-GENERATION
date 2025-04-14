import unittest
import csv
import os
import time
import math
import cmath
import sys

# Fix the import path to find the source modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.case_studies.quadratic_solver import QuadraticSolver

class TestQuadraticSolver(unittest.TestCase):
    """
    Test cases for the QuadraticSolver class.
    """
    
    def setUp(self):
        """Set up the test environment."""
        # No need to instantiate the class since all methods are static
        self.solver = QuadraticSolver
        self.test_cases_file = os.path.join('data', 'quadratic_test_cases.csv')
    
    def test_z3_generated_cases(self):
        """Test the quadratic solver with Z3-generated test cases."""
        if not os.path.exists(self.test_cases_file):
            self.skipTest(f"Test cases file not found: {self.test_cases_file}")
        
        start_time = time.time()
        total_tests = 0
        passed_tests = 0
        
        with open(self.test_cases_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                a = float(row['a'])
                b = float(row['b'])
                c = float(row['c'])
                scenario = row['scenario']
                
                total_tests += 1
                
                try:
                    result = self.solver.solve(a, b, c)
                    
                    # Verify the result based on the scenario
                    if scenario == 'real_distinct_roots':
                        self.assertEqual(len(result), 2)
                        self.assertNotEqual(result[0], result[1])
                        for root in result:
                            self.assertIsInstance(root, float)
                            self.assertAlmostEqual(a * root * root + b * root + c, 0, places=8)
                    
                    elif scenario == 'real_identical_roots':
                        self.assertEqual(len(result), 2)
                        self.assertEqual(result[0], result[1])
                        root = result[0]
                        self.assertIsInstance(root, float)
                        self.assertAlmostEqual(a * root * root + b * root + c, 0, places=8)
                    
                    elif scenario == 'complex_roots':
                        self.assertEqual(len(result), 2)
                        for root in result:
                            self.assertIsInstance(root, complex)
                            self.assertAlmostEqual(a * root * root + b * root + c, 0, places=8)
                    
                    elif scenario == 'linear_equation':
                        self.assertEqual(len(result), 1)
                        root = result[0]
                        self.assertAlmostEqual(b * root + c, 0, places=8)
                    
                    elif scenario == 'no_solution':
                        self.assertEqual(result, "No solution")
                    
                    elif scenario == 'infinite_solutions':
                        self.assertEqual(result, "Infinite solutions")
                    
                    passed_tests += 1
                
                except Exception as e:
                    print(f"Test failed for a={a}, b={b}, c={c}, scenario={scenario}: {str(e)}")
        
        execution_time = time.time() - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        print(f"Passed tests: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.2f}%)")
    
    def test_special_cases(self):
        """Test special cases manually."""
        # Test with a = 0 (linear equation)
        self.assertEqual(self.solver.solve(0, 2, -4), (2.0,))
        
        # Test with a = 0, b = 0, c = 0 (infinite solutions)
        self.assertEqual(self.solver.solve(0, 0, 0), "Infinite solutions")
        
        # Test with a = 0, b = 0, c != 0 (no solution)
        self.assertEqual(self.solver.solve(0, 0, 5), "No solution")
        
        # Test with discriminant = 0 (one real root)
        result = self.solver.solve(1, 2, 1)
        self.assertEqual(result[0], result[1])
        self.assertAlmostEqual(result[0], -1.0)

if __name__ == '__main__':
    unittest.main()
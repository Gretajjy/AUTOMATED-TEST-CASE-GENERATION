import csv
import os
from z3 import Real, Solver, sat, Or

class Z3TestGenerator:
    """
    A class to generate test cases using Z3 Solver
    """
    
    def __init__(self, output_file):
        """
        Initialize the Z3 test generator.
        
        Args:
            output_file (str): Path to save the generated test cases
        """
        self.output_file = output_file
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    def generate_quadratic_test_cases(self, num_cases=20):
        """
        Generate test cases for quadratic equation solver using Z3.
        
        Args:
            num_cases (int): Number of test cases to generate
            
        Returns:
            list: Generated test cases
        """
        # Initialize Z3 solver
        solver = Solver()
        
        # Declare variables
        a = Real('a')
        b = Real('b')
        c = Real('c')
        
        # List to store test cases
        test_cases = []
        
        # Generate cases with real roots (discriminant > 0)
        test_cases.extend(self._generate_cases_with_condition(
            solver, a, b, c, 
            condition=b*b - 4*a*c > 0,
            additional_constraints=[a != 0],
            scenario="real_distinct_roots",
            count=int(num_cases * 0.3)
        ))
        
        # Generate cases with one real root (discriminant = 0)
        test_cases.extend(self._generate_cases_with_condition(
            solver, a, b, c, 
            condition=b*b - 4*a*c == 0,
            additional_constraints=[a != 0],
            scenario="real_identical_roots",
            count=int(num_cases * 0.2)
        ))
        
        # Generate cases with complex roots (discriminant < 0)
        test_cases.extend(self._generate_cases_with_condition(
            solver, a, b, c, 
            condition=b*b - 4*a*c < 0,
            additional_constraints=[a != 0],
            scenario="complex_roots",
            count=int(num_cases * 0.3)
        ))
        
        # Generate edge case: a = 0 (linear equation)
        test_cases.extend(self._generate_cases_with_condition(
            solver, a, b, c, 
            condition=a == 0,
            additional_constraints=[b != 0],
            scenario="linear_equation",
            count=int(num_cases * 0.1)
        ))
        
        # Generate edge case: a = 0, b = 0 (degenerate case)
        test_cases.extend(self._generate_cases_with_condition(
            solver, a, b, c, 
            condition=a == 0,
            additional_constraints=[b == 0, c != 0],
            scenario="no_solution",
            count=1
        ))
        
        # Add one case for a = 0, b = 0, c = 0 (all solutions)
        test_cases.append({
            'a': 0.0,
            'b': 0.0,
            'c': 0.0,
            'scenario': 'infinite_solutions'
        })
        
        # Save test cases to CSV
        self._save_to_csv(test_cases)
        
        return test_cases
    
    def _generate_cases_with_condition(self, solver, a, b, c, condition, additional_constraints, scenario, count):
        """
        Generate test cases with specific conditions using Z3.
        
        Args:
            solver (z3.Solver): Z3 solver instance
            a, b, c: Z3 variables for coefficients
            condition: Z3 condition for test cases
            additional_constraints (list): Additional constraints for Z3
            scenario (str): Description of the test scenario
            count (int): Number of test cases to generate
            
        Returns:
            list: Generated test cases that satisfy the conditions
        """
        cases = []
        solver.push()
        
        # Add the main condition
        solver.add(condition)
        
        # Add any additional constraints
        for constraint in additional_constraints:
            solver.add(constraint)
        
        # Generate the specified number of test cases
        for _ in range(count):
            if solver.check() == sat:
                model = solver.model()
                
                # Modify this part to correctly handle Z3 model values
                try:
                    a_val = self._parse_z3_decimal(model[a])
                    b_val = self._parse_z3_decimal(model[b])
                    c_val = self._parse_z3_decimal(model[c])
                    
                    case = {
                        'a': a_val,
                        'b': b_val,
                        'c': c_val,
                        'scenario': scenario
                    }
                    cases.append(case)
                    
                    # Add constraint to get different values next time
                    solver.add(Or(a != model[a], b != model[b], c != model[c]))
                except Exception as e:
                    print(f"Error parsing model values: {e}")
                    # Skip this case and try to generate the next one
                    solver.add(Or(a != model[a], b != model[b], c != model[c]))
                    continue
            else:
                # No more satisfying models
                break
        
        solver.pop()
        return cases
    
    def _parse_z3_decimal(self, value):
        """
        Parse a Z3 decimal value to float, handling special cases.
        
        Args:
            value: Z3 model value
            
        Returns:
            float: Parsed float value
        """
        try:
            # Try to get numeric value directly
            if hasattr(value, 'numerator_as_long') and hasattr(value, 'denominator_as_long'):
                # Handle rational numbers
                num = value.numerator_as_long()
                den = value.denominator_as_long()
                if den != 0:
                    return float(num) / float(den)
            
            # Try regular parsing
            decimal_str = value.as_decimal(10)
            # Handle values with question marks that Z3 might produce
            if '?' in decimal_str:
                decimal_str = decimal_str.replace('?', '')
            return float(decimal_str)
        except Exception as e:
            # If parsing fails, try string representation
            try:
                str_val = str(value)
                if '/' in str_val:  # Handle fraction format
                    num, den = str_val.split('/')
                    return float(num) / float(den)
                return float(str_val)
            except:
                # Last attempt: return a reasonable default value
                return 1.0  # Return a safe value that won't cause subsequent errors
    
    def _save_to_csv(self, test_cases):
        """
        Save generated test cases to a CSV file.
        
        Args:
            test_cases (list): List of test case dictionaries
        """
        with open(self.output_file, 'w', newline='') as file:
            if not test_cases:
                return
                
            fieldnames = test_cases[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_cases)
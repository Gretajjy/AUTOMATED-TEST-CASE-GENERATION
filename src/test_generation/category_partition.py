import csv
import os
from itertools import product

class CategoryPartitionTestGenerator:
    """
    A class to generate test cases using Category-Partition method
    """
    
    def __init__(self, output_file):
        """
        Initialize the Category-Partition test generator.
        
        Args:
            output_file (str): Path to save the generated test cases
        """
        self.output_file = output_file
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    def generate_date_conversion_test_cases(self):
        """
        Generate test cases for date format conversion using Category-Partition method.
        
        Returns:
            list: Generated test cases
        """
        # Define categories and choices
        categories = {
            "year": [
                {"value": "0001", "description": "minimum allowed year"},
                {"value": "1000", "description": "early year"},
                {"value": "1999", "description": "year before millennium"},
                {"value": "2000", "description": "millennium year (leap)"},
                {"value": "2020", "description": "leap year"},
                {"value": "2023", "description": "current year"},
                {"value": "2100", "description": "century year (non-leap)"},
                {"value": "9999", "description": "maximum allowed year"}
            ],
            "month": [
                {"value": "01", "description": "January (31 days)"},
                {"value": "02", "description": "February (28/29 days)"},
                {"value": "03", "description": "March (31 days)"},
                {"value": "04", "description": "April (30 days)"},
                {"value": "06", "description": "June (30 days)"},
                {"value": "09", "description": "September (30 days)"},
                {"value": "11", "description": "November (30 days)"},
                {"value": "12", "description": "December (31 days)"}
            ],
            "day": [
                {"value": "01", "description": "first day"},
                {"value": "15", "description": "middle day"},
                {"value": "28", "description": "last day in February (non-leap)"},
                {"value": "29", "description": "leap day in February"},
                {"value": "30", "description": "30th day"},
                {"value": "31", "description": "31st day"}
            ],
            "format_direction": [
                {"value": "iso_to_dmy", "description": "YYYY-MM-DD to DD/MM/YYYY"},
                {"value": "dmy_to_iso", "description": "DD/MM/YYYY to YYYY-MM-DD"}
            ]
        }
        
        # Generate all possible combinations (test frames)
        test_cases = []
        
        # Generate valid date combinations
        for year_choice, month_choice, day_choice, format_choice in product(
            categories["year"], categories["month"], categories["day"], categories["format_direction"]
        ):
            year = year_choice["value"]
            month = month_choice["value"]
            day = day_choice["value"]
            
            # Skip invalid dates based on constraints
            if not self._is_valid_date(year, month, day):
                continue
            
            format_direction = format_choice["value"]
            
            if format_direction == "iso_to_dmy":
                input_date = f"{year}-{month}-{day}"
                expected_output = f"{day}/{month}/{year}"
            else:  # dmy_to_iso
                input_date = f"{day}/{month}/{year}"
                expected_output = f"{year}-{month}-{day}"
            
            test_case = {
                "input_date": input_date,
                "format_direction": format_direction,
                "expected_output": expected_output,
                "description": f"{year_choice['description']}, {month_choice['description']}, {day_choice['description']}"
            }
            
            test_cases.append(test_case)
        
        # Add invalid date test cases - fundamental validation issues
        invalid_test_cases = [
            # Invalid dates with out-of-range values
            {
                "input_date": "2023-02-30",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid date - February 30th"
            },
            {
                "input_date": "2023-13-01",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid month - 13"
            },
            {
                "input_date": "2023-00-01",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid month - 0"
            },
            {
                "input_date": "2023-01-00",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid day - 0"
            },
            {
                "input_date": "2023-01-32",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid day - 32"
            },
            {
                "input_date": "31/04/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - April 31st"
            },
            {
                "input_date": "31/06/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - June 31st"
            },
            {
                "input_date": "31/09/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - September 31st"
            },
            {
                "input_date": "31/11/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - November 31st"
            },
            
            # Leap year special cases
            {
                "input_date": "29/02/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - February 29th in non-leap year"
            },
            {
                "input_date": "2023-02-29",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid date - February 29th in non-leap year"
            },
            {
                "input_date": "29/02/2100",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid date - February 29th in century non-leap year"
            },
            
            # Format errors
            {
                "input_date": "2023/01/15",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Format mismatch - using slashes instead of hyphens in ISO format"
            },
            {
                "input_date": "15-01-2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Format mismatch - using hyphens instead of slashes in DMY format"
            },
            {
                "input_date": "2023-1-1",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Format mismatch - single digits without leading zeros in ISO format"
            },
            {
                "input_date": "1/1/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Format mismatch - single digits without leading zeros in DMY format"
            },
            
            # Incomplete or malformed inputs
            {
                "input_date": "2023-01",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Incomplete date - missing day"
            },
            {
                "input_date": "01/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Incomplete date - missing day"
            },
            {
                "input_date": "2023",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Incomplete date - year only"
            },
            {
                "input_date": "2023-JAN-15",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Invalid format - month as text in ISO format"
            },
            {
                "input_date": "15/JAN/2023",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Invalid format - month as text in DMY format"
            },
            
            # Special input errors
            {
                "input_date": "",
                "format_direction": "iso_to_dmy",
                "expected_output": "ValueError",
                "description": "Empty input"
            },
            {
                "input_date": None,
                "format_direction": "iso_to_dmy",
                "expected_output": "TypeError",
                "description": "None input - should raise TypeError"
            },
            {
                "input_date": 20230115,
                "format_direction": "iso_to_dmy",
                "expected_output": "TypeError",
                "description": "Integer input - should raise TypeError"
            },
            
            # Extreme values
            {
                "input_date": "01/01/0000",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Year out of range - year 0 doesn't exist"
            },
            {
                "input_date": "01/01/10000",
                "format_direction": "dmy_to_iso",
                "expected_output": "ValueError",
                "description": "Year out of range - beyond maximum (9999)"
            }
        ]
        
        test_cases.extend(invalid_test_cases)
        
        # Add format detection test cases
        format_detection_test_cases = [
            {
                "input_date": "2023-01-15",
                "format_direction": "auto_detect",
                "expected_output": "15/01/2023",
                "description": "Auto-detect ISO format (YYYY-MM-DD)"
            },
            {
                "input_date": "15/01/2023",
                "format_direction": "auto_detect",
                "expected_output": "2023-01-15",
                "description": "Auto-detect DMY format (DD/MM/YYYY)"
            },
            {
                "input_date": "01/15/2023",
                "format_direction": "auto_detect",
                "expected_output": "2023-01-15",
                "description": "Auto-detect MDY format (MM/DD/YYYY)"
            },
            {
                "input_date": "2023/01/15",
                "format_direction": "auto_detect",
                "expected_output": "15-01-2023",
                "description": "Auto-detect YMD format with slashes"
            },
            {
                "input_date": "15-01-2023",
                "format_direction": "auto_detect",
                "expected_output": "2023/01/15",
                "description": "Auto-detect DMY format with dashes"
            },
            {
                "input_date": "15.01.2023",
                "format_direction": "auto_detect",
                "expected_output": "2023.01.15",
                "description": "Auto-detect DMY format with dots"
            },
            {
                "input_date": "20230115",
                "format_direction": "auto_detect",
                "expected_output": "15/01/2023",
                "description": "Auto-detect basic format without separators"
            }
        ]
        
        # Include format detection test cases if the DateConverter class supports it
        # test_cases.extend(format_detection_test_cases)
        
        # Save test cases to CSV
        self._save_to_csv(test_cases)
        
        return test_cases
    
    def _is_valid_date(self, year, month, day):
        """
        Check if a date is valid.
        
        Args:
            year (str): Year as string
            month (str): Month as string
            day (str): Day as string
            
        Returns:
            bool: True if date is valid, False otherwise
        """
        try:
            year_val = int(year)
            month_val = int(month)
            day_val = int(day)
            
            # Check year range (1-9999)
            if year_val < 1 or year_val > 9999:
                return False
                
            # Check basic month and day validity
            if month_val < 1 or month_val > 12 or day_val < 1 or day_val > 31:
                return False
            
            # Check months with 30 days
            if month_val in [4, 6, 9, 11] and day_val > 30:
                return False
            
            # Check February
            if month_val == 2:
                if self._is_leap_year(year_val):
                    return day_val <= 29
                else:
                    return day_val <= 28
            
            return True
        except ValueError:
            return False
    
    def _is_leap_year(self, year):
        """
        Check if a year is a leap year.
        
        Args:
            year (int): Year to check
            
        Returns:
            bool: True if year is a leap year, False otherwise
        """
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        return year % 4 == 0
    
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
            
    def generate_quadratic_test_cases_cp(self, output_file=None):
        """
        Generate test cases for quadratic equation solver using Category-Partition method.
        This is an alternative to Z3-based generation for comparison purposes.
        
        Args:
            output_file (str, optional): Path to save the test cases. Defaults to None.
            
        Returns:
            list: Generated test cases
        """
        if output_file:
            self.output_file = output_file
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
        # Define categories and choices for quadratic equation ax^2 + bx + c = 0
        categories = {
            "a": [
                {"value": 0, "description": "zero (linear equation)"},
                {"value": 1, "description": "positive one (simplified)"},
                {"value": -1, "description": "negative one (simplified)"},
                {"value": 2, "description": "positive integer"},
                {"value": -2, "description": "negative integer"},
                {"value": 0.5, "description": "positive fraction"},
                {"value": -0.5, "description": "negative fraction"}
            ],
            "b": [
                {"value": 0, "description": "zero"},
                {"value": 1, "description": "positive one"},
                {"value": -1, "description": "negative one"},
                {"value": 10, "description": "large positive"},
                {"value": -10, "description": "large negative"},
                {"value": 0.5, "description": "positive fraction"},
                {"value": -0.5, "description": "negative fraction"}
            ],
            "c": [
                {"value": 0, "description": "zero"},
                {"value": 1, "description": "positive one"},
                {"value": -1, "description": "negative one"},
                {"value": 25, "description": "large positive perfect square"},
                {"value": -25, "description": "large negative"},
                {"value": 0.25, "description": "positive fraction"},
                {"value": -0.25, "description": "negative fraction"}
            ]
        }
        
        test_cases = []
        
        # Generate all combinations
        for a_choice, b_choice, c_choice in product(
            categories["a"], categories["b"], categories["c"]
        ):
            a = a_choice["value"]
            b = b_choice["value"]
            c = c_choice["value"]
            
            # Determine the scenario based on parameter values
            scenario = self._determine_quadratic_scenario(a, b, c)
            
            test_case = {
                "a": a,
                "b": b,
                "c": c,
                "scenario": scenario,
                "description": f"a={a} ({a_choice['description']}), b={b} ({b_choice['description']}), c={c} ({c_choice['description']})"
            }
            
            test_cases.append(test_case)
        
        # Apply constraints to reduce test case count (optional)
        # This could be a place to eliminate redundant or less valuable test cases
        
        # Save test cases to CSV
        if output_file:
            self._save_to_csv(test_cases)
        
        return test_cases
    
    def _determine_quadratic_scenario(self, a, b, c):
        """
        Determine the scenario for a quadratic equation based on coefficient values.
        
        Args:
            a (float): Coefficient of x^2
            b (float): Coefficient of x
            c (float): Constant term
            
        Returns:
            str: Description of the scenario
        """
        if a == 0:
            if b == 0:
                if c == 0:
                    return "infinite_solutions"  # 0 = 0
                else:
                    return "no_solution"  # 0 = non-zero
            else:
                return "linear_equation"  # bx + c = 0
        
        # Calculate the discriminant
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            return "real_distinct_roots"
        elif discriminant == 0:
            return "real_identical_roots"
        else:  # discriminant < 0
            return "complex_roots"
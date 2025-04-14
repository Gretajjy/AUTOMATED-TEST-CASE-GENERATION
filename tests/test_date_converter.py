import unittest
import csv
import os
import time
import sys

# Fix the import path to find the source modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.case_studies.date_converter import DateConverter

class TestDateConverter(unittest.TestCase):
    """
    Test cases for the DateConverter class.
    """
    
    def setUp(self):
        """Set up the test environment."""
        # No need to instantiate the class since all methods are static
        self.converter = DateConverter
        self.test_cases_file = os.path.join('data', 'date_test_cases.csv')
    
    def test_category_partition_cases(self):
        """Test the date converter with category-partition generated test cases."""
        if not os.path.exists(self.test_cases_file):
            self.skipTest(f"Test cases file not found: {self.test_cases_file}")
        
        start_time = time.time()
        total_tests = 0
        passed_tests = 0
        
        with open(self.test_cases_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                input_date = row['input_date']
                format_direction = row['format_direction']
                expected_output = row['expected_output']
                description = row['description']
                
                total_tests += 1
                
                try:
                    if format_direction == "iso_to_dmy":
                        if expected_output == "ValueError":
                            # Expect a ValueError for invalid dates
                            with self.assertRaises(ValueError, msg=f"Failed for {description}"):
                                self.converter.iso_to_dmy(input_date)
                        else:
                            result = self.converter.iso_to_dmy(input_date)
                            self.assertEqual(result, expected_output, f"Failed for {description}")
                    else:  # dmy_to_iso
                        if expected_output == "ValueError":
                            # Expect a ValueError for invalid dates
                            with self.assertRaises(ValueError, msg=f"Failed for {description}"):
                                self.converter.dmy_to_iso(input_date)
                        else:
                            result = self.converter.dmy_to_iso(input_date)
                            self.assertEqual(result, expected_output, f"Failed for {description}")
                    
                    passed_tests += 1
                    
                except Exception as e:
                    print(f"Test failed for input={input_date}, direction={format_direction}: {str(e)}")
        
        execution_time = time.time() - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        print(f"Passed tests: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.2f}%)")
    
    def test_basic_conversion(self):
        """Test basic date conversion functionality."""
        # Test ISO to DMY
        self.assertEqual(self.converter.iso_to_dmy("2023-01-15"), "15/01/2023")
        
        # Test DMY to ISO
        self.assertEqual(self.converter.dmy_to_iso("15/01/2023"), "2023-01-15")
        
        # Test invalid date format
        with self.assertRaises(ValueError):
            self.converter.iso_to_dmy("2023/01/15")
        
        # Test invalid date
        with self.assertRaises(ValueError):
            self.converter.iso_to_dmy("2023-02-30")
            
    def test_format_date(self):
        """Test automatic format detection."""
        # Test that None input raises ValueError as expected
        with self.assertRaises(ValueError):
            self.converter.format_date(None, "%Y-%m-%d")
            
        # Test with valid inputs in different formats
        self.assertEqual(self.converter.format_date("2023-05-15", "%d/%m/%Y"), "15/05/2023")
        self.assertEqual(self.converter.format_date("15/05/2023", "%Y-%m-%d"), "2023-05-15")
        self.assertEqual(self.converter.format_date("05/15/2023", "%Y-%m-%d"), "2023-05-15")
        
        # Test with invalid date format
        with self.assertRaises(ValueError):
            self.converter.format_date("2023.05.15", "%Y-%m-%d")

if __name__ == '__main__':
    unittest.main()
import os
import sys
import json
import time
import subprocess

class CoverageAnalyzer:
    """
    A class to analyze code coverage of Python tests.
    """
    
    def __init__(self, reports_dir='reports'):
        """
        Initialize the CoverageAnalyzer.
        
        Args:
            reports_dir (str): Directory to store coverage reports
        """
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def run_coverage_analysis(self, source, test_module, report_name=None):
        """
        Run coverage analysis using coverage.py.
        
        Args:
            source (str): Module to measure coverage for
            test_module (str): Test module path (dot notation)
            report_name (str, optional): Name for the report directory
            
        Returns:
            dict: Results of coverage analysis including stats and execution time
        """
        if report_name is None:
            report_name = f"{source.split('.')[-1]}_coverage"
        
        report_path = os.path.join(self.reports_dir, report_name)
        os.makedirs(report_path, exist_ok=True)
        
        print(f"Running coverage analysis for {source}...")
        start_time = time.time()
        
        try:
            # Build absolute path to the test file
            test_file_name = f"{test_module.split('.')[-1]}.py"
            test_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                         "tests", test_file_name)
            
            if not os.path.exists(test_file_path):
                print(f"Test file not found: {test_file_path}")
                return {
                    "execution_time": time.time() - start_time,
                    "success": False,
                    "error": f"Test file not found: {test_file_path}"
                }
            
            print(f"Found test file: {test_file_path}")
            
            # 1. 首先创建覆盖率配置文件
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".coveragerc")
            if not os.path.exists(config_path):
                with open(config_path, 'w') as f:
                    f.write("""
[run]
branch = True
source = src

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
                    """)
                print("Created coverage configuration file")
            
            # 2. 运行测试并收集覆盖率数据，确保加上--branch参数
            coverage_run_cmd = [
                "coverage", "run", 
                "--branch",  # 添加branch参数
                f"--source={source}", 
                test_file_path
            ]
            
            print(f"Running command: {' '.join(coverage_run_cmd)}")
            
            process = subprocess.run(
                coverage_run_cmd,
                check=False,
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                print(f"Coverage command failed with error: {process.stderr}")
            
            # 3. 生成JSON报告以便解析
            json_file = os.path.join(report_path, "coverage.json")
            json_cmd = ["coverage", "json", "-o", json_file]
            
            print(f"Generating JSON report: {' '.join(json_cmd)}")
            
            json_process = subprocess.run(
                json_cmd,
                check=False,
                capture_output=True,
                text=True
            )
            
            if json_process.returncode != 0:
                print(f"JSON report generation failed: {json_process.stderr}")
            
            # 4. 生成HTML报告方便查看
            html_cmd = ["coverage", "html", "-d", report_path]
            
            print(f"Generating HTML report: {' '.join(html_cmd)}")
            
            html_process = subprocess.run(
                html_cmd,
                check=False,
                capture_output=True,
                text=True
            )
            
            if html_process.returncode != 0:
                print(f"HTML report generation failed: {html_process.stderr}")
            
            # 5. 获取覆盖率数据
            coverage_data = self.parse_coverage_json(json_file)
            
            execution_time = time.time() - start_time
            
            results = {
                "execution_time": execution_time,
                "coverage_data": coverage_data,
                "success": True,
                "report_path": report_path
            }
            
            print(f"Coverage analysis completed in {execution_time:.2f} seconds")
            if coverage_data:
                print(f"Line coverage: {coverage_data.get('line_coverage', 0):.2f}%")
                print(f"Branch coverage: {coverage_data.get('branch_coverage', 0):.2f}%")
            
            return results
            
        except Exception as e:
            print(f"Error in coverage analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "execution_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }
    
    def parse_coverage_json(self, json_file):
        """
        Parse the coverage JSON report.
        
        Args:
            json_file (str): Path to the JSON coverage report
            
        Returns:
            dict: Coverage metrics or None if parsing failed
        """
        try:
            if not os.path.exists(json_file):
                print(f"Coverage JSON file not found: {json_file}")
                return None
                
            print(f"Parsing coverage data from {json_file}")
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            totals = data.get('totals', {})
            
            # 更详细地打印解析到的数据
            print(f"Found coverage data: {json.dumps(totals, indent=2)}")
            
            coverage_data = {
                'line_coverage': totals.get('percent_covered', 0),
                'missing_lines': totals.get('missing_lines', 0),
                'excluded_lines': totals.get('excluded_lines', 0),
                'num_statements': totals.get('num_statements', 0),
                'num_branches': totals.get('num_branches', 0) or 0  # 确保不为None
            }
            
            # 手动计算分支覆盖率
            num_branches = totals.get('num_branches', 0)
            if num_branches > 0:
                covered_branches = totals.get('covered_branches', 0)
                coverage_data['branch_coverage'] = (covered_branches / num_branches) * 100
            else:
                coverage_data['branch_coverage'] = 0
            
            return coverage_data
            
        except Exception as e:
            print(f"Error parsing coverage JSON: {str(e)}")
            import traceback
            traceback.print_exc()  # 打印更详细的错误信息
            return None
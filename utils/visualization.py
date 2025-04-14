import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import pandas as pd
import seaborn as sns

class Visualizer:
    """
    A class to create visualizations for test results and analysis.
    """
    
    def __init__(self, output_dir='reports/visualizations'):
        """
        Initialize the Visualizer.
        
        Args:
            output_dir (str): Directory to save visualization outputs
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_test_case_distribution(self, test_cases, case_type, category_field=None):
        """
        Create a pie chart showing the distribution of test cases.
        
        Args:
            test_cases (list): List of test case dictionaries
            case_type (str): Type of test cases (e.g., 'quadratic', 'date')
            category_field (str, optional): Field to categorize by
            
        Returns:
            str: Path to the saved visualization
        """
        plt.figure(figsize=(10, 7))
        
        if case_type == 'quadratic':
            # For quadratic equations, categorize by scenario
            categories = {}
            for case in test_cases:
                scenario = case['scenario']
                if scenario not in categories:
                    categories[scenario] = 0
                categories[scenario] += 1
            
            labels = list(categories.keys())
            sizes = list(categories.values())
            
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
            plt.axis('equal')
            plt.title('Distribution of Quadratic Equation Test Cases by Scenario')
            
        elif case_type == 'date':
            # For date conversion, first check if categorizing by a specific field
            if category_field:
                categories = {}
                for case in test_cases:
                    value = case.get(category_field)
                    if value not in categories:
                        categories[value] = 0
                    categories[value] += 1
                
                labels = list(categories.keys())
                sizes = list(categories.values())
                
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
                plt.axis('equal')
                plt.title(f'Distribution of Date Conversion Test Cases by {category_field}')
            else:
                # Default: categorize by valid/invalid
                valid_count = sum(1 for case in test_cases if case['expected_output'] != "ValueError")
                invalid_count = len(test_cases) - valid_count
                
                labels = ['Valid Dates', 'Invalid Dates']
                sizes = [valid_count, invalid_count]
                
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True,
                        colors=['#4CAF50', '#F44336'])
                plt.axis('equal')
                plt.title('Distribution of Date Conversion Test Cases by Validity')
        
        # Save figure
        output_path = os.path.join(self.output_dir, f'{case_type}_distribution.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def plot_coverage_comparison(self, coverage_results):
        """
        Create a bar chart comparing line and branch coverage for different modules.
        
        Args:
            coverage_results (dict): Dictionary with module names as keys and coverage data as values
            
        Returns:
            str: Path to the saved visualization
        """
        modules = list(coverage_results.keys())
        line_coverage = [coverage_results[m].get('coverage_data', {}).get('line_coverage', 0) for m in modules]
        branch_coverage = [coverage_results[m].get('coverage_data', {}).get('branch_coverage', 0) for m in modules]
        
        x = np.arange(len(modules))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 7))
        rects1 = ax.bar(x - width/2, line_coverage, width, label='Line Coverage')
        rects2 = ax.bar(x + width/2, branch_coverage, width, label='Branch Coverage')
        
        ax.set_ylabel('Coverage (%)')
        ax.set_title('Code Coverage Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels([m.split('.')[-1] for m in modules])
        ax.legend()
        ax.yaxis.set_major_locator(MaxNLocator(11))
        ax.set_ylim(0, 110)  # Leave some space at the top
        
        self._add_value_labels(ax, rects1)
        self._add_value_labels(ax, rects2)
        
        fig.tight_layout()
        
        # Save figure
        output_path = os.path.join(self.output_dir, 'coverage_comparison.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def plot_mutation_scores(self, mutation_results):
        """
        Create a bar chart showing mutation scores for different modules.
        
        Args:
            mutation_results (dict): Dictionary with module names as keys and mutation data as values
            
        Returns:
            str: Path to the saved visualization
        """
        modules = list(mutation_results.keys())
        scores = [mutation_results[m].get('mutation_score', 0) for m in modules]
        
        plt.figure(figsize=(10, 7))
        bars = plt.bar(modules, scores, color='#3F51B5')
        
        plt.ylabel('Mutation Score (%)')
        plt.title('Mutation Testing Scores by Module')
        plt.xticks([i for i in range(len(modules))], [m.split('.')[-1] for m in modules])
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.ylim(0, 110)  # Leave some space at the top
        
        # Save figure
        output_path = os.path.join(self.output_dir, 'mutation_scores.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def plot_execution_times(self, coverage_times, mutation_times):
        """
        Create a bar chart comparing execution times for different analyses.
        
        Args:
            coverage_times (dict): Dictionary with module names as keys and coverage execution times as values
            mutation_times (dict): Dictionary with module names as keys and mutation execution times as values
            
        Returns:
            str: Path to the saved visualization
        """
        modules = list(coverage_times.keys())
        cov_times = [coverage_times[m] for m in modules]
        mut_times = [mutation_times[m] for m in modules]
        
        x = np.arange(len(modules))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 7))
        rects1 = ax.bar(x - width/2, cov_times, width, label='Coverage Analysis')
        rects2 = ax.bar(x + width/2, mut_times, width, label='Mutation Testing')
        
        ax.set_ylabel('Execution Time (seconds)')
        ax.set_title('Test Analysis Execution Times')
        ax.set_xticks(x)
        ax.set_xticklabels([m.split('.')[-1] for m in modules])
        ax.legend()
        
        self._add_value_labels(ax, rects1)
        self._add_value_labels(ax, rects2)
        
        fig.tight_layout()
        
        # Save figure
        output_path = os.path.join(self.output_dir, 'execution_times.png')
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def create_summary_report(self, test_gen_data, coverage_data, mutation_data, execution_data):
        """
        Create a comprehensive HTML report summarizing all results.
        
        Args:
            test_gen_data (dict): Test generation summary data
            coverage_data (dict): Coverage analysis data
            mutation_data (dict): Mutation testing data
            execution_data (dict): Execution time data
            
        Returns:
            str: Path to the saved HTML report
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Automated Test Generation Summary Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .card {{
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .chart-container {{
                    margin: 20px 0;
                    text-align: center;
                }}
                .chart-container img {{
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                .summary-box {{
                    background-color: #e8f4fd;
                    border-left: 4px solid #2196F3;
                    padding: 15px;
                    margin: 15px 0;
                }}
                .technique-box {{
                    margin-top: 10px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Automated Test Generation Summary Report</h1>
                
                <div class="card">
                    <h2>Test Generation Summary</h2>
                    <div class="summary-box">
                        <p><strong>Total Quadratic Equation Test Cases:</strong> {test_gen_data.get('quadratic_count', 0)}</p>
                        <p><strong>Total Date Conversion Test Cases:</strong> {test_gen_data.get('date_count', 0)}</p>
                        <p><strong>Total Execution Time:</strong> {execution_data.get('total_time', 0):.2f} seconds</p>
                    </div>
                    
                    <div class="technique-box">
                        <h3>Z-Solver Technique for Quadratic Equations</h3>
                        <p>Z-Solver uses mathematical constraints to generate test cases that cover different scenarios for the quadratic equation solver, including real roots, complex roots, and special cases.</p>
                        <div class="chart-container">
                            <img src="visualizations/quadratic_distribution.png" alt="Quadratic Test Case Distribution">
                        </div>
                    </div>
                    
                    <div class="technique-box">
                        <h3>Category-Partition Technique for Date Conversion</h3>
                        <p>Category-Partition divides the input space into categories and values, generating test cases by combining these values while respecting constraints.</p>
                        <div class="chart-container">
                            <img src="visualizations/date_distribution.png" alt="Date Test Case Distribution">
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Code Coverage Analysis</h2>
                    <table>
                        <tr>
                            <th>Module</th>
                            <th>Line Coverage</th>
                            <th>Branch Coverage</th>
                        </tr>
        """
        
        # Add coverage data rows
        for module, data in coverage_data.items():
            module_name = module.split('.')[-1]
            line_cov = data.get('coverage_data', {}).get('line_coverage', 0)
            branch_cov = data.get('coverage_data', {}).get('branch_coverage', 0)
            
            html_content += f"""
                        <tr>
                            <td>{module_name}</td>
                            <td>{line_cov:.2f}%</td>
                            <td>{branch_cov:.2f}%</td>
                        </tr>
            """
        
        html_content += f"""
                    </table>
                    
                    <div class="chart-container">
                        <img src="visualizations/coverage_comparison.png" alt="Coverage Comparison">
                    </div>
                </div>
                
                <div class="card">
                    <h2>Mutation Testing Results</h2>
                    <p>Mutation testing measures the effectiveness of tests by introducing small changes (mutations) to the code and checking if tests can detect these changes.</p>
                    
                    <table>
                        <tr>
                            <th>Module</th>
                            <th>Mutation Score</th>
                            <th>Execution Time</th>
                        </tr>
        """
        
        # Add mutation data rows
        for module, data in mutation_data.items():
            module_name = module.split('.')[-1]
            score = data.get('mutation_score', 0)
            exec_time = data.get('execution_time', 0)
            
            html_content += f"""
                        <tr>
                            <td>{module_name}</td>
                            <td>{score:.2f}%</td>
                            <td>{exec_time:.2f} seconds</td>
                        </tr>
            """
        
        html_content += f"""
                    </table>
                    
                    <div class="chart-container">
                        <img src="visualizations/mutation_scores.png" alt="Mutation Scores">
                    </div>
                </div>
                
                <div class="card">
                    <h2>Performance Comparison</h2>
                    <div class="chart-container">
                        <img src="visualizations/execution_times.png" alt="Execution Times">
                    </div>
                    
                    <h3>Technique Comparison</h3>
                    <table>
                        <tr>
                            <th>Aspect</th>
                            <th>Z-Solver (Quadratic)</th>
                            <th>Category-Partition (Date)</th>
                        </tr>
                        <tr>
                            <td>Test Count</td>
                            <td>{test_gen_data.get('quadratic_count', 0)}</td>
                            <td>{test_gen_data.get('date_count', 0)}</td>
                        </tr>
                        <tr>
                            <td>Line Coverage</td>
                            <td>{coverage_data.get('src.case_studies.quadratic_solver', {}).get('coverage_data', {}).get('line_coverage', 0):.2f}%</td>
                            <td>{coverage_data.get('src.case_studies.date_converter', {}).get('coverage_data', {}).get('line_coverage', 0):.2f}%</td>
                        </tr>
                        <tr>
                            <td>Mutation Score</td>
                            <td>{mutation_data.get('src.case_studies.quadratic_solver', {}).get('mutation_score', 0):.2f}%</td>
                            <td>{mutation_data.get('src.case_studies.date_converter', {}).get('mutation_score', 0):.2f}%</td>
                        </tr>
                    </table>
                </div>
                
                <div class="card">
                    <h2>Conclusion and Insights</h2>
                    <p>This report presents a comparison of two automated test generation techniques applied to different case studies:</p>
                    <ul>
                        <li><strong>Z-Solver for Quadratic Equation Solver:</strong> Generated {test_gen_data.get('quadratic_count', 0)} test cases covering various scenarios with {coverage_data.get('src.case_studies.quadratic_solver', {}).get('coverage_data', {}).get('line_coverage', 0):.2f}% line coverage and {mutation_data.get('src.case_studies.quadratic_solver', {}).get('mutation_score', 0):.2f}% mutation score.</li>
                        <li><strong>Category-Partition for Date Converter:</strong> Generated {test_gen_data.get('date_count', 0)} test cases with {coverage_data.get('src.case_studies.date_converter', {}).get('coverage_data', {}).get('line_coverage', 0):.2f}% line coverage and {mutation_data.get('src.case_studies.date_converter', {}).get('mutation_score', 0):.2f}% mutation score.</li>
                    </ul>
                    
                    <div class="summary-box">
                        <h3>Key Findings:</h3>
                        <p>Both techniques were effective for their respective case studies, with high code coverage and mutation scores, indicating good fault detection capability. Z-Solver is particularly well-suited for mathematical problems with clear constraints, while Category-Partition excels at testing systems with distinct input categories.</p>
                    </div>
                </div>
                
                <footer style="text-align: center; margin-top: 30px; padding: 20px; color: #777; font-size: 0.9em;">
                    Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | SYSC 5807 - Automated Test Case Generation Project
                </footer>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        output_path = os.path.join(self.output_dir, '..', 'summary_report.html')
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
    
    def _add_value_labels(self, ax, rects):
        """Add value labels above the bars"""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
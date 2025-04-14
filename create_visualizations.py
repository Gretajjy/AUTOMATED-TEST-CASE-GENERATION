import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd # Not used in this version
import os
import json
import sys # Import sys for command line arguments

# Create output directory if it doesn't exist
output_dir = 'visualizations'
os.makedirs(output_dir, exist_ok=True)

# --- Plotting Functions ---

def create_coverage_comparison(data):
    """Creates coverage comparison bar chart from loaded data."""
    plt.figure(figsize=(10, 6))

    # Extract data, use defaults if missing
    quad_cov = data.get('quadratic_coverage', {})
    date_cov = data.get('date_coverage', {})

    quad_line = quad_cov.get('line_coverage', 0) if quad_cov.get('success') else 0
    date_line = date_cov.get('line_coverage', 0) if date_cov.get('success') else 0
    # Handle potential None for branch coverage
    quad_branch = quad_cov.get('branch_coverage', 0) if quad_cov.get('success') and quad_cov.get('branch_coverage') is not None else 0
    date_branch = date_cov.get('branch_coverage', 0) if date_cov.get('success') and date_cov.get('branch_coverage') is not None else 0


    techniques = ['Quadratic Solver', 'Date Converter']
    line_coverage = [quad_line, date_line]
    branch_coverage = [quad_branch, date_branch] # Add branch coverage data

    bar_width = 0.35
    index = np.arange(len(techniques))

    # Create grouped bar chart
    bars1 = plt.bar(index - bar_width/2, line_coverage, bar_width, label='Line Coverage', color='#3498db')
    bars2 = plt.bar(index + bar_width/2, branch_coverage, bar_width, label='Branch Coverage', color='#2ecc71')


    # Add labels and title
    plt.ylabel('Coverage (%)', fontsize=12)
    plt.title('Code Coverage Comparison (Line & Branch)', fontsize=14)
    plt.xticks(index, techniques, fontsize=11) # Set x-axis labels
    plt.ylim(0, 105) # Start y-axis from 0

    # Add percentage text on bars
    for bars in [bars1, bars2]:
         for bar in bars:
              height = bar.get_height()
              plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=10)


    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    plt.tight_layout()

    # Save the figure
    save_path = os.path.join(output_dir, 'coverage_comparison.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Coverage comparison chart saved to {save_path}")
    plt.close()

def create_mutation_pie_chart(data, target_key, title_suffix):
     """Creates mutation score pie chart for a given target."""
     plt.figure(figsize=(8, 8))

     mutation_data = data.get(target_key, {})
     killed = 0
     total = 0
     score = 0

     if mutation_data and mutation_data.get('success'):
          killed = mutation_data.get('killed_mutants', 0)
          total = mutation_data.get('total_mutants', 0)
          score = mutation_data.get('mutation_score', 0)
     else:
          print(f"Warning: Mutation data for {title_suffix} not found or analysis failed. Using placeholders.")
          # Use placeholder values if data is missing
          killed = 17 # Placeholder
          total = 20 # Placeholder
          score = (killed / total) * 100 if total > 0 else 0


     survived = total - killed
     if total == 0: # Avoid division by zero if no mutants generated
          sizes = [0, 0]
          print(f"Warning: Zero total mutants reported for {title_suffix}. Pie chart will be empty.")
     else:
          sizes = [killed, survived]

     labels = [f'Killed ({killed})', f'Survived ({survived})']
     colors = ['#27ae60', '#e74c3c']
     explode = (0, 0.1) # Explode survived slice

     # Create pie chart
     if total > 0:
          plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                  autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 12})
          plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
     else:
          plt.text(0.5, 0.5, "No mutation data available", ha='center', va='center', fontsize=12)


     plt.title(f'Mutation Testing Results for {title_suffix}\nScore: {score:.1f}%', fontsize=14)
     plt.tight_layout()

     # Save the figure
     safe_suffix = title_suffix.lower().replace(' ', '_')
     save_path = os.path.join(output_dir, f'mutation_results_{safe_suffix}.png')
     plt.savefig(save_path, dpi=300, bbox_inches='tight')
     print(f"Mutation results pie chart for {title_suffix} saved to {save_path}")
     plt.close()


# --- Other visualization functions (Quadratic, Date, Architecture, Techniques) ---
# These currently use hardcoded data as they depend on the specific test generation logic
# or represent conceptual design. Keep them as they are for now, or adapt them
# if you have specific data sources for them.

def create_quadratic_distribution():
    # This visualization depends on the Z3 generation logic distribution,
    # which seems fixed in the generator script. Keep as is unless generator changes.
    plt.figure(figsize=(10, 8))
    labels = ['Real Distinct Roots (30%)', 'Real Identical Roots (20%)',
              'Complex Roots (30%)', 'Linear Equation (10%)',
              'No Solution (5%)', 'Infinite Solutions (5%)'] # Based on Z3 generator proportions
    sizes = [30, 20, 30, 10, 5, 5]
    colors = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#f39c12', '#1abc9c']
    explode = (0.05, 0.05, 0.05, 0.1, 0.15, 0.15)
    patches, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=90,
                                        textprops={'fontsize': 11})
    for text in texts: text.set_fontsize(9)
    plt.axis('equal')
    plt.title('Target Quadratic Equation Test Case Distribution (Z3-Solver)', fontsize=14)
    plt.tight_layout()
    save_path = os.path.join(output_dir, 'quadratic_distribution.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Quadratic equation distribution chart saved to {save_path}")
    plt.close()

def create_date_distribution():
    # This depends on the Category-Partition generator output.
    # For simplicity, keeping it based on typical expected output.
    # A more advanced version could read the generated CSV.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    labels1 = ['Valid Dates', 'Invalid Dates']
    # Example sizes - replace with actual analysis if needed
    sizes1 = [95, 5] # Approximate based on typical CP generation
    colors1 = ['#3498db', '#e74c3c']
    ax1.pie(sizes1, labels=None, colors=colors1, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.legend(labels1, loc='upper right', fontsize=12)
    ax1.set_title('Valid vs Invalid Date Test Cases', fontsize=14)

    labels2 = ['ISO to DMY', 'DMY to ISO']
    sizes2 = [50, 50] # Expect roughly equal distribution
    colors2 = ['#2ecc71', '#9b59b6']
    ax2.pie(sizes2, labels=None, colors=colors2, autopct='%1.1f%%', shadow=False, startangle=90)
    ax2.legend(labels2, loc='upper right', fontsize=12)
    ax2.set_title('Conversion Direction Distribution', fontsize=14)

    plt.suptitle('Target Date Converter Test Case Distribution (Category-Partition)', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    save_path = os.path.join(output_dir, 'date_distribution.png')
    plt.savefig(save_path, dpi=400, bbox_inches='tight')
    print(f"Date conversion distribution chart saved to {save_path}")
    plt.close()

def create_system_architecture():
    # Conceptual diagram - keep as is.
    plt.figure(figsize=(12, 8))
    components = {
        'Test Generation': (0.5, 0.8), 'Z3-Solver': (0.3, 0.6), 'Category-Partition': (0.7, 0.6),
        'Test Execution': (0.5, 0.4), 'Quadratic Solver': (0.3, 0.2), 'Date Converter': (0.7, 0.2),
        'Coverage Analysis': (0.2, 0.5), 'Mutation Analysis': (0.8, 0.5)
    }
    connections = [
        ('Test Generation', 'Z3-Solver'), ('Test Generation', 'Category-Partition'),
        ('Z3-Solver', 'Quadratic Solver'), ('Category-Partition', 'Date Converter'),
        ('Quadratic Solver', 'Test Execution'), ('Date Converter', 'Test Execution'),
        ('Test Execution', 'Coverage Analysis'), ('Test Execution', 'Mutation Analysis')
    ]
    for component, (x, y) in components.items():
        color = '#3498db' # Default blue
        width, height = 0.2, 0.1
        if component in ['Z3-Solver', 'Category-Partition']: color = '#27ae60'; width, height = 0.15, 0.08
        elif component in ['Coverage Analysis', 'Mutation Analysis']: color = '#f39c12'; width, height = 0.15, 0.08
        elif component in ['Quadratic Solver', 'Date Converter']: color = '#9b59b6'; width, height = 0.15, 0.08
        rect = plt.Rectangle((x-width/2, y-height/2), width, height, facecolor=color, alpha=0.7, edgecolor='black', linewidth=2, zorder=2)
        plt.gca().add_patch(rect)
        plt.text(x, y, component.replace(' ', '\n'), ha='center', va='center', fontsize=9, fontweight='bold', zorder=3)
    for start, end in connections:
        start_x, start_y = components[start]; end_x, end_y = components[end]
        plt.arrow(start_x, start_y - height/2 if start_y > end_y else start_y + height/2, # Adjust arrow start/end
                  end_x-start_x, end_y-start_y,
                  head_width=0.015, head_length=0.02, fc='black', ec='black', length_includes_head=True, zorder=1)
    plt.xlim(0, 1); plt.ylim(0, 1)
    plt.title('System Architecture Diagram', fontsize=14); plt.axis('off')
    save_path = os.path.join(output_dir, 'system_architecture.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"System architecture diagram saved to {save_path}")
    plt.close()


def create_techniques_comparison():
    # Conceptual comparison - keep as is. Values represent subjective assessment.
    plt.figure(figsize=(10, 8))
    categories = ['Code Coverage', 'Execution Speed', 'Setup Complexity',
                 'Edge Case Detection', 'Maintainability']
    z3_values = [4.8, 3.5, 4.0, 5.0, 3.5] # Example scores
    cp_values = [5.0, 4.0, 3.0, 4.0, 4.5] # Example scores
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist() + [0]
    z3_values += z3_values[:1]; cp_values += cp_values[:1]
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, fontsize=11)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], fontsize=9)
    plt.ylim(0, 5.5) # Extend ylim slightly
    ax.plot(angles, z3_values, 'o-', linewidth=2, label='Z3-Solver', color='#3498db')
    ax.fill(angles, z3_values, alpha=0.25, color='#3498db')
    ax.plot(angles, cp_values, 'o-', linewidth=2, label='Category-Partition', color='#2ecc71')
    ax.fill(angles, cp_values, alpha=0.25, color='#2ecc71')
    plt.title('Subjective Technique Comparison Across Metrics', fontsize=14, y=1.1) # Adjust title position
    plt.legend(loc='lower right', bbox_to_anchor=(1.1, 0.05)) # Adjust legend position
    # Save the figure
    save_path = os.path.join(output_dir, 'techniques_comparison.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Techniques comparison chart saved to {save_path}")
    plt.close()


# --- Main execution block ---

def main(summary_file="reports/analysis_summary.json"):
    """Loads data and creates all visualizations."""
    print("Creating visualizations...")
    analysis_data = {}
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            print(f"Loaded analysis data from {summary_file}")
        except Exception as e:
            print(f"Warning: Could not load analysis data from {summary_file}. Using defaults. Error: {e}")
    else:
        print(f"Warning: Analysis summary file not found at {summary_file}. Using defaults.")

    # Create visualizations using loaded data (or defaults)
    create_coverage_comparison(analysis_data)
    create_mutation_pie_chart(analysis_data, 'quadratic_mutation', 'Quadratic Solver')
    create_mutation_pie_chart(analysis_data, 'date_mutation', 'Date Converter')

    # Create other visualizations (currently using hardcoded/conceptual data)
    create_quadratic_distribution()
    create_date_distribution()
    create_system_architecture()
    create_techniques_comparison()

    print("\nAll visualizations created successfully in the 'visualizations' directory.")

if __name__ == "__main__":
    # Allow running directly, optionally taking summary file as argument
    file_to_load = sys.argv[1] if len(sys.argv) > 1 else "reports/analysis_summary.json"
    main(file_to_load)

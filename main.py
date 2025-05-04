import os
import subprocess
import sys
import time
from datetime import datetime

def run_script(script_name):
    """Run a Python script and display its output."""
    print(f"\n{'=' * 50}")
    print(f"Running {script_name}...")
    print(f"{'=' * 50}\n")
    
    # Use sys.executable to ensure we use the same Python interpreter
    process = subprocess.Popen(
        [sys.executable, script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Print the output as it comes
    for line in process.stdout:
        print(line.strip())
    
    # Wait for the process to complete
    process.wait()
    
    if process.returncode == 0:
        print(f"\n✓ {script_name} completed successfully.")
    else:
        print(f"\n✗ {script_name} failed with return code {process.returncode}.")
    
    return process.returncode == 0

def main():
    # List of scripts to run in order
    scripts = [
        'convert_to_csv.py',         # Convert HTML to CSV
        'find_not_following_back.py', # Find users not following back
        'generate_instagram_report.py' # Generate comprehensive report
    ]
    
    print("\n" + "=" * 70)
    print("          INSTAGRAM ANALYSIS - RUNNING ALL SCRIPTS")
    print("=" * 70 + "\n")
    
    start_time = time.time()
    
    # Check if all scripts exist
    for script in scripts:
        if not os.path.exists(script):
            print(f"Error: Script '{script}' not found.")
            return
    
    # Run each script
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1
    
    # Report summary
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {success_count}/{len(scripts)} scripts completed successfully")
    print(f"Total time: {elapsed_time:.2f} seconds")
    print("=" * 70)
    
    # Look for the report in the reports directory
    report_dir = "reports"
    if os.path.exists(report_dir):
        today_date = datetime.now().strftime('%Y-%m-%d')
        report_file = os.path.join(report_dir, f"instagram_report_{today_date}.txt")
        
        if os.path.exists(report_file):
            print(f"\nInstagram report has been generated. Opening report: {report_file}\n")
            try:
                # Try to open the report with the default text editor
                os.startfile(report_file)
            except Exception as e:
                print(f"Could not open report automatically: {e}")
                print(f"Please open {report_file} manually to view the results.")
        else:
            print(f"\nReport file not found at expected location: {report_file}")
            print(f"Check the {report_dir} directory for the generated report.")
    else:
        print(f"\nReports directory not found: {report_dir}")

if __name__ == "__main__":
    main() 
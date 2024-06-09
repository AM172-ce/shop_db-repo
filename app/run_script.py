import sys
import subprocess

# Check if the script was called with the correct number of arguments.
if len(sys.argv) != 2:
    print("Usage: python run_script.py <script_name.py>")
    sys.exit(1)

# Get the script name from the command-line arguments.
script_name = sys.argv[1]

# Try to run the specified script using the subprocess module.
try:
    # The subprocess.run method runs the command passed as a list.
    # check=True will raise an exception if the script returns a non-zero exit code.
    subprocess.run(["python", script_name], check=True)
except subprocess.CalledProcessError as e:
    # If there is an error running the script, print the error message.
    print(f"Error running script {script_name}: {e}")

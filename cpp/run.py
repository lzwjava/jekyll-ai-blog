import subprocess
import os


def compile_and_run_cpp():
    # Path to the C++ file
    cpp_file = "main.cpp"
    # Output executable name
    executable = "main"

    try:
        # Compile the C++ code
        compile_command = ["g++", cpp_file, "-o", executable]
        result = subprocess.run(
            compile_command, check=True, capture_output=True, text=True
        )
        print("Compilation successful!")

        # Run the executable
        run_command = [f"./{executable}"]
        subprocess.run(run_command, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred during compilation or execution:")
        if e.stderr:
            print(e.stderr)
        elif e.output:
            print(e.output)
        else:
            print("Unknown error, no output captured.")
    except FileNotFoundError:
        print(
            "Compiler or file not found. Make sure g++ is installed and the C++ file exists."
        )


if __name__ == "__main__":
    # Ensure the script is run from the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    compile_and_run_cpp()

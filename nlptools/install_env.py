import os
import subprocess

def main():
    # Determine the path to the 'environment.yml' file within the package
    package_dir = os.path.dirname(__file__)
    env_file = os.path.join(package_dir, 'environment.yml')

    # Create the conda environment using the 'environment.yml' file
    subprocess.call(["conda", "env", "create", "-f", env_file])

if __name__ == "__main__":
    main()

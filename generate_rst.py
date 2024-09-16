import os

def create_rst_files(source_dir, rst_dir):
    """
    Create index.rst and module rst files for each Python module in the project source directory.

    :param source_dir: The directory where the Python source files are located.
    :param rst_dir: The directory where the .rst files will be created.
    """
    # Create index.rst
    index_rst_path = os.path.join(rst_dir, "index.rst")
    with open(index_rst_path, 'w') as index_file:
        index_file.write("Project Documentation\n")
        index_file.write("======================\n\n")
        index_file.write(".. toctree::\n")
        index_file.write("   :maxdepth: 2\n")
        index_file.write("   :caption: Contents:\n\n")

        # Loop through all Python files in the source directory
        for file_name in os.listdir(source_dir):
            if file_name.endswith(".py") and file_name != "__init__.py":
                module_name = file_name.replace(".py", "")
                rst_file_name = f"{module_name}.rst"
                index_file.write(f"   {module_name}\n")

                # Create module rst file
                module_rst_path = os.path.join(rst_dir, rst_file_name)
                with open(module_rst_path, 'w') as module_file:
                    module_file.write(f"{module_name.capitalize()} Module\n")
                    module_file.write("=" * (len(module_name) + 7) + "\n\n")
                    module_file.write(f".. automodule:: {module_name}\n")
                    module_file.write("   :members:\n")
                    module_file.write("   :undoc-members:\n")
                    module_file.write("   :show-inheritance:\n")

# Example usage
source_dir = "../ticktactoe"  # Replace with your source directory
rst_dir = "source"  # Replace with your .rst directory
os.makedirs(rst_dir, exist_ok=True)
create_rst_files(source_dir, rst_dir)

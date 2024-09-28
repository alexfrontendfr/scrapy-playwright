import os

def print_directory_tree(path, level=3):
    for root, dirs, files in os.walk(path):
        indent_level = root.replace(path, '').count(os.sep)
        if indent_level < level:
            indent = ' ' * 4 * (indent_level)
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (indent_level + 1)
            for f in files:
                print(f'{subindent}{f}')

# Call the function
print_directory_tree('.')

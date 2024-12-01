import os

def find_txt_files(directory):
    """
    Recursively find all .txt files in the given directory and its subdirectories.
    
    Args:
        directory (str): Path to the directory to search
        
    Returns:
        list: List of paths to all .txt files found
    """

    txt_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
                
    return txt_files


def is_valid_path(path):
    try:
        res = os.path.exists(path)
    except Exception as e:
        print(f"Error checking path {path}: {e}")
        return False
    return res


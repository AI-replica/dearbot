from config import CONTEXT_TEXTS_DIR_PATH
from utils.files import find_txt_files, is_valid_path
from os.path import basename

def build_context_data():
    if CONTEXT_TEXTS_DIR_PATH is None:
        return None
    
    if not is_valid_path(CONTEXT_TEXTS_DIR_PATH):
        raise ValueError(f"Can't access the dir path {CONTEXT_TEXTS_DIR_PATH}")
    
    txt_files_list = find_txt_files(CONTEXT_TEXTS_DIR_PATH)
    if len(txt_files_list) == 0:
        print(f"No .txt files found in the dir path {CONTEXT_TEXTS_DIR_PATH}")
        return None
    
    context_data = ""
    for txt_file in txt_files_list:
        filename = basename(txt_file)
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            context_data += f"<{filename}>\n{content}\n</{filename}>\n\n"
    
    return context_data.strip()
    
    
import os
import sys

# Rövid magyarázat / hivatkozás
# Futtatás fájlba:
# python combine_files.py -f
# → combined_plugin_output.txt fájlba ír.
#
# Futtatás vágólapra:
# python combine_files.py
# → vágólapra másol.

# --- Beállítások ---
TARGET_EXTENSIONS = ['.php', '.js', '.css']
EXCLUDE_DIRS = ['.git', 'languages', 'node_modules']
OUTPUT_FILE = 'combined_plugin_output.txt'

COMMENT_PREFIX = {
    '.php': '//',
    '.js': '//',
    '.css': '//',
    '.txt': '//',
}

# --- Segédfüggvények ---

def get_comment_prefix(extension):
    return COMMENT_PREFIX.get(extension, '//')

def collect_files(root_dir):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in TARGET_EXTENSIONS:
                full_path = os.path.join(dirpath, filename)
                all_files.append(full_path)
    return all_files

def generate_structure_listing(files):
    return [os.path.relpath(f).replace("\\", "/") for f in files]

def combine_files_content(files):
    content_lines = []
    content_lines.append("// Futtatás fájlba:")
    content_lines.append("// python combine_files.py -f")
    content_lines.append("// → combined_plugin_output.txt fájlba ír.")
    content_lines.append("// Futtatás vágólapra:")
    content_lines.append("// python combine_files.py")
    content_lines.append("// → vágólapra másol.")
    content_lines.append("// ====== FÁJLSTRUKTÚRA ======")
    for path in generate_structure_listing(files):
        content_lines.append(f"// {path}")
    content_lines.append("// ====== ÖSSZEFŰZÖTT FÁJLOK KEZDETE ======\n")
    for filepath in files:
        rel_path = os.path.relpath(filepath).replace("\\", "/")
        _, ext = os.path.splitext(filepath)
        prefix = get_comment_prefix(ext)
        content_lines.append(f"\n{prefix} ===== FILE: {rel_path} =====\n")
        try:
            with open(filepath, 'r', encoding='utf-8') as infile:
                contents = infile.read()
                content_lines.append(contents)
                content_lines.append("\n")
        except Exception as e:
            content_lines.append(f"{prefix} ERROR reading {rel_path}: {e}\n")
    return "\n".join(content_lines)

def copy_to_clipboard(text):
    try:
        # Próbáljuk használni a pyperclip-et
        import pyperclip
        pyperclip.copy(text)
        print("[✔] Összefűzött tartalom vágólapra másolva.")
    except ImportError:
        # Ha nincs pyperclip, próbálunk natív megoldást
        if sys.platform == "win32":
            import subprocess
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))
            print("[✔] Vágólapra másolva (Windows).")
        elif sys.platform == "darwin":
            import subprocess
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))
            print("[✔] Vágólapra másolva (Mac).")
        elif sys.platform == "linux":
            import subprocess
            try:
                p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))
                print("[✔] Vágólapra másolva (Linux/xclip).")
            except FileNotFoundError:
                print("[!] xclip nincs telepítve. Telepítsd: sudo apt install xclip")
        else:
            print("[!] Vágólapra másolás nem támogatott ezen a rendszeren pyperclip nélkül.")

# --- Futtatás ---

if __name__ == '__main__':
    current_directory = os.getcwd()
    files = collect_files(current_directory)
    content = combine_files_content(files)

    if len(sys.argv) > 1 and sys.argv[1] == '-f':
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
        print(f"[✔] Összefűzés kész: {OUTPUT_FILE}")
    else:
        copy_to_clipboard(content)

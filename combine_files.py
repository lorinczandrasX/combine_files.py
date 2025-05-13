import os

# --- Beállítások ---
TARGET_EXTENSIONS = ['.php', '.js', '.css']
EXCLUDE_DIRS = ['.git', 'languages', 'node_modules']
OUTPUT_FILE = 'combined_plugin_output.txt'

# Komment stílus minden támogatott fájltípushoz (egységes: //)
COMMENT_PREFIX = {
    '.php': '//',
    '.js': '//',
    '.css': '//',
    '.txt': '//',
}


# --- Segédfüggvények ---

def get_comment_prefix(extension):
    return COMMENT_PREFIX.get(extension, '//')  # alapértelmezés: //

def collect_files(root_dir):
    """Bejárja az aktuális könyvtárat, kizárva a megadott mappákat, és összegyűjti a fájlokat."""
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Kizárt mappák eltávolítása
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in TARGET_EXTENSIONS:
                full_path = os.path.join(dirpath, filename)
                all_files.append(full_path)
    return all_files

def generate_structure_listing(files):
    """Relatív elérési útvonalakból készít egy listát a fájlstruktúra blokknak."""
    return [os.path.relpath(f).replace("\\", "/") for f in files]

def combine_files(files, output_file):
    """Kiírja a struktúrát és a fájlok tartalmát egy fájlba."""
    with open(output_file, 'w', encoding='utf-8') as outfile:

        # --- Fájllista blokk a fájl elején ---
        outfile.write("// ====== FÁJLSTRUKTÚRA ======\n")
        for path in generate_structure_listing(files):
            outfile.write(f"// {path}\n")
        outfile.write("// ====== ÖSSZEFŰZÖTT FÁJLOK KEZDETE ======\n\n")

        # --- Tartalom blokk, fájlonként ---
        for filepath in files:
            rel_path = os.path.relpath(filepath).replace("\\", "/")
            _, ext = os.path.splitext(filepath)
            prefix = get_comment_prefix(ext)

            outfile.write(f"\n{prefix} ===== FILE: {rel_path} =====\n\n")

            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    contents = infile.read()
                    outfile.write(contents)
                    outfile.write("\n\n")
            except Exception as e:
                outfile.write(f"{prefix} ERROR reading {rel_path}: {e}\n\n")

    print(f"[✔] Összefűzés kész: {output_file}")


# --- Futtatás ---

if __name__ == '__main__':
    current_directory = os.getcwd()
    files = collect_files(current_directory)
    combine_files(files, OUTPUT_FILE)

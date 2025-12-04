import os

output_file = "unified_llm_eval.txt"

# --- 1. CONFIGURATION ---

# Files to exclude by name, anywhere they appear
exclude_files = {
    "README.md",
    output_file,
    ".DS_Store"
}

# Directories to exclude by name, anywhere they appear
exclude_dirs = {
    ".git",
    "__pycache__"
}

# === The new, easy way to exclude multiple specific paths ===
# Just add any folder path you want to skip into this list.
exclude_full_paths_list = [
    "./vendor",
    "./evaluation_results"
]

# --- END OF CONFIGURATION ---


# For faster lookups, convert the list of normalized paths into a set
exclude_path_set = {os.path.normpath(p) for p in exclude_full_paths_list}

print(f"Excluding specific paths: {exclude_path_set}")

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk("."):
        # First, filter out directories by name (e.g., __pycache__)
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Second, filter out directories if their full path is in our exclusion set
        # This is the key logic that prevents os.walk from going into these folders
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_path_set]

        for file in files:
            if file in exclude_files:
                continue

            file_path = os.path.join(root, file)
            
            # An extra check to skip files if they are inside an excluded path
            # This is a safeguard, as the dirs[:] filtering should already prevent this.
            if any(os.path.normpath(file_path).startswith(p) for p in exclude_path_set):
                continue

            relative_path = os.path.relpath(file_path, ".")
            out.write(f"# {relative_path}\n")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read())
            except UnicodeDecodeError:
                out.write("[Cannot decode this file, skipped]\n")

            out.write("\n\n")

print(f"All files combined to {output_file}")
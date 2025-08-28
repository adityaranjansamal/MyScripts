import os
import argparse
import sys
import shutil

def get_unique_filepath(destination_dir, original_filename):
    """
    Generates a unique file path in the destination directory to avoid overwriting.
    If a file with the same name exists, it appends a number like (1), (2), etc.

    Args:
        destination_dir (str): The directory where the file will be moved.
        original_filename (str): The original name of the file.

    Returns:
        str: A unique file path for the destination.
    """
    # Separate the filename and its extension (e.g., 'data', '.json')
    base, extension = os.path.splitext(original_filename)
    counter = 1
    # Start with the original proposed file path
    new_filepath = os.path.join(destination_dir, original_filename)

    # Loop while a file at the proposed path already exists
    while os.path.exists(new_filepath):
        # Create a new filename with a counter
        new_filename = f"{base} ({counter}){extension}"
        new_filepath = os.path.join(destination_dir, new_filename)
        counter += 1
        
    return new_filepath

def move_json_files(root_folder, dry_run=False):
    """
    Recursively finds and moves all .json files to a new 'All_JSONS'
    directory created inside the specified root folder. Renames files with
    duplicate names to prevent overwrites.

    Args:
        root_folder (str): The absolute or relative path to the starting directory.
        dry_run (bool): If True, the script will only list the files to be
                        moved without actually moving them.
    """
    # --- Initialization ---
    json_files_found = 0
    files_moved_successfully = 0
    files_failed_to_move = 0
    files_to_process = []
    
    destination_dir = os.path.join(root_folder, "All_JSONS")

    # --- Step 1: Find all JSON files recursively ---
    print(f"[*] Starting search in: '{root_folder}'")

    if not os.path.isdir(root_folder):
        print(f"[ERROR] The specified folder does not exist: {root_folder}")
        sys.exit(1)

    for dirpath, _, filenames in os.walk(root_folder):
        if os.path.abspath(dirpath) == os.path.abspath(destination_dir):
            continue
            
        for filename in filenames:
            if filename.lower().endswith('.json'):
                full_path = os.path.join(dirpath, filename)
                files_to_process.append(full_path)
                json_files_found += 1

    # --- Step 2: Process the found files (Move or Dry Run) ---
    if dry_run:
        print("\n" + "="*20)
        print("DRY RUN MODE ENABLED")
        print("="*20)
        print(f"The following files would be moved to '{destination_dir}':")
        if not files_to_process:
            print("No .json files found to move.")
        else:
            # Keep track of names that would be moved to show potential renames
            moved_filenames = set()
            for file_path in files_to_process:
                original_filename = os.path.basename(file_path)
                if original_filename in moved_filenames:
                    print(f"  - {file_path} (will be renamed)")
                else:
                    print(f"  - {file_path}")
                moved_filenames.add(original_filename)
        print("="*20)

    else: # This is the actual move logic
        print(f"\n[*] Found {json_files_found} JSON file(s). Proceeding with relocation...")
        if not files_to_process:
            print("No .json files to move.")
        else:
            try:
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)
                    print(f"[*] Created destination directory: {destination_dir}")
            except OSError as e:
                print(f"[ERROR] Could not create destination directory: {e}")
                sys.exit(1)

            for file_path in files_to_process:
                try:
                    original_filename = os.path.basename(file_path)
                    # Get a unique destination path to prevent overwrites
                    unique_destination_path = get_unique_filepath(destination_dir, original_filename)
                    
                    shutil.move(file_path, unique_destination_path)
                    
                    # Log if the file was renamed
                    final_filename = os.path.basename(unique_destination_path)
                    if original_filename != final_filename:
                        print(f"[MOVED & RENAMED] {file_path} -> {final_filename}")
                    else:
                        print(f"[MOVED] {file_path}")
                        
                    files_moved_successfully += 1
                except (OSError, shutil.Error) as e:
                    print(f"[ERROR] Failed to move {file_path}: {e}")
                    files_failed_to_move += 1

    # --- Step 3: Print the final report ---
    print("\n" + "-"*15)
    print("Execution Report")
    print("-"*15)
    print(f"Total JSON files found: {json_files_found}")
    if not dry_run:
        print(f"Successfully moved:     {files_moved_successfully}")
        print(f"Failed to move:         {files_failed_to_move}")
    print("-"*15)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to recursively find and move all .json files from a given directory to a new 'All_JSONS' sub-directory.",
        epilog="Example usage: python move_script.py /path/to/your/folder --dry-run"
    )
    parser.add_argument(
        "root_folder",
        type=str,
        help="The path to the root folder to start the search from."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without moving any files. It will only list the files that would be moved."
    )
    args = parser.parse_args()
    move_json_files(args.root_folder, args.dry_run)

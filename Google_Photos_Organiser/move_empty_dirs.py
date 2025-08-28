import os
import sys
import shutil
import argparse

def move_empty_folders(root_dir, dry_run=False):
    """
    Recursively finds and moves empty directories, handling name collisions.

    Args:
        root_dir (str): The absolute path to the directory to scan.
        dry_run (bool): If True, only reports what would be moved.
    """
    # --- Initialization ---
    dest_dir = os.path.join(root_dir, "EMPTY_FOLDERS")
    total_found = 0
    moved_successfully = 0
    failed_to_move = 0

    print("--- Empty Directory Mover v2 (Handles Name Collisions) ---")
    print(f"Root Directory: {root_dir}")
    if dry_run:
        print("Mode:           DRY RUN (No changes will be made)")
    else:
        print("Mode:           LIVE RUN")
        print(f"Destination:    {dest_dir}")
    print("----------------------------------------------------------")

    # --- Create Destination Directory ---
    if not dry_run:
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create destination directory '{dest_dir}'. Aborting.", file=sys.stderr)
            print(f"Reason: {e}", file=sys.stderr)
            sys.exit(1)

    # --- Main Logic: Find and Process Empty Dirs ---
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if os.path.abspath(dirpath) == os.path.abspath(dest_dir):
            continue
        
        if not dirnames and not filenames:
            total_found += 1
            print(f"Found empty directory: {dirpath}")

            # --- NEW: Logic to handle name collisions ---
            original_basename = os.path.basename(dirpath)
            target_path = os.path.join(dest_dir, original_basename)
            final_name = original_basename
            counter = 1

            # Check if a folder with the same name exists in the destination.
            # This check is performed for both dry and live runs for accurate reporting.
            while os.path.exists(target_path):
                final_name = f"{original_basename} ({counter})"
                target_path = os.path.join(dest_dir, final_name)
                counter += 1
            # --- END NEW ---

            if dry_run:
                if final_name != original_basename:
                    print(f"  └── [DRY RUN] Would move and rename to '{final_name}'")
                else:
                    print(f"  └── [DRY RUN] Would move '{final_name}'")
                moved_successfully += 1
            else:
                try:
                    # Move the directory. The `target_path` is now guaranteed to be unique.
                    shutil.move(dirpath, target_path)
                    
                    if final_name != original_basename:
                        print(f"  └── [SUCCESS] Moved and renamed to '{final_name}'")
                    else:
                        print(f"  └── [SUCCESS] Moved '{final_name}'")
                    moved_successfully += 1
                except (OSError, shutil.Error) as e:
                    print(f"  └── [FAILURE] Could not move '{original_basename}'", file=sys.stderr)
                    print(f"      Reason: {e}", file=sys.stderr)
                    failed_to_move += 1

    # --- Reporting ---
    print("----------------------------------------------------------")
    print("--- Final Report ---")
    print(f"Total empty directories found:    {total_found}")
    if dry_run:
        print(f"Total directories to be moved:    {moved_successfully}")
    else:
        print(f"Moved successfully:               {moved_successfully}")
        print(f"Failed to move:                   {failed_to_move}")
    print("----------------------------------------------------------")
    
    if not dry_run and failed_to_move > 0:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively finds and moves empty directories, handling name collisions by renaming.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("root_directory", help="The directory to start scanning from.")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Perform a dry run without moving any files.")
    args = parser.parse_args()

    if not os.path.isdir(args.root_directory):
        print(f"Error: The path '{args.root_directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    abs_root_dir = os.path.abspath(args.root_directory)
    move_empty_folders(abs_root_dir, args.dry_run)
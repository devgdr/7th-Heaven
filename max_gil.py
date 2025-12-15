import os
import struct
import sys

# Configuration
MAX_GIL = 99999999
GIL_OFFSET = 0x20
SAVE_FILENAME = "save00.ff7"

def patch_save_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False

    print(f"Found save file: {file_path}")
    confirmation = input(f"Set Gil to {MAX_GIL:,} in '{file_path}'? (y/n): ")
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        return False

    try:
        with open(file_path, 'r+b') as f:
            # Read current Gil for comparison
            f.seek(GIL_OFFSET)
            current_gil_bytes = f.read(4)
            current_gil = struct.unpack('<I', current_gil_bytes)[0]
            print(f"Current Gil: {current_gil:,}")

            # Write new Gil
            f.seek(GIL_OFFSET)
            f.write(struct.pack('<I', MAX_GIL))
            
            print(f"Success! Gil updated to {MAX_GIL:,}")
            return True
    except Exception as e:
        print(f"Failed to patch file: {e}")
        return False

def find_and_patch():
    # 1. Check if a path was provided as an argument
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        patch_save_file(target_path)
        return

    # 2. Search in common 7th Heaven save location (relative to script or game)
    # Checks current directory and a 'save' subdirectory
    possible_paths = [
        os.path.join(os.getcwd(), SAVE_FILENAME),
        os.path.join(os.getcwd(), "save", SAVE_FILENAME),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            patch_save_file(path)
            return

    # 3. If not found, ask user
    print(f"Could not find '{SAVE_FILENAME}' in the current directory or 'save' folder.")
    user_path = input("Please enter the full path to your save00.ff7 file: ").strip()
    # Remove quotes if user added them
    user_path = user_path.strip('"').strip("'")
    
    if user_path:
        patch_save_file(user_path)

if __name__ == "__main__":
    print("--- 7th Heaven Max Gil Patcher ---")
    find_and_patch()
    input("\nPress Enter to exit...")

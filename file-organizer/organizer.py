import os
import shutil
import sys
import time

IGNORE_EXTENSIONS = ["crdownload", "tmp", "part"]

def wait_until_file_ready(file_path, timeout=10):
    start_time = time.time()
    prev_size = -1

    while time.time() - start_time < timeout:
        if not os.path.exists(file_path):
            return False

        curr_size = os.path.getsize(file_path)

        if curr_size == prev_size:
            return True

        prev_size = curr_size
        time.sleep(0.5)

    return False


def create_extension_folder(base_path, extension):
    path = os.path.join(base_path, extension)
    os.makedirs(path, exist_ok=True)
    return path


def move_file_safely(src, dest):
    try:
        shutil.move(src, dest)
        print(f"[INFO] Moved: {os.path.basename(src)}")
    except Exception as e:
        print(f"[ERROR] Move failed: {e}")


def organize(file_path):

    if not os.path.isfile(file_path):
        return

    filename = os.path.basename(file_path)

    if "." not in filename:
        return

    extension = filename.split('.')[-1].lower()

    if extension in IGNORE_EXTENSIONS:
        return

    if not wait_until_file_ready(file_path):
        print(f"[SKIP] File not ready: {filename}")
        return

    folder_path = os.path.dirname(file_path)
    ext_folder = create_extension_folder(folder_path, extension)

    new_path = os.path.join(ext_folder, filename)

    move_file_safely(file_path, new_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 organize.py <file_path>")
        sys.exit(1)

    organize(sys.argv[1])
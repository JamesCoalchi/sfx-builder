import base64
import os
import subprocess
import sys

def pack(files, run_after_unpack, output_name='unpacker'):
    try:
        if len(files) == 0:
            print("No files to pack.")
            return

        rau = os.path.basename(run_after_unpack) if run_after_unpack else ""

        file_data = []
        total = len(files)

        for index, file in enumerate(files, 1):
            progress = (index / total) * 100
            print(f"WORKING ON FILE {file} ({int(progress)}%/100% done)")

            with open(file, 'rb') as readb:
                contents = readb.read()
                encoded = base64.b64encode(contents).decode('utf-8')
                file_data.append({
                    'name': os.path.basename(file),
                    'content': encoded
                })

        script = f"""
import os
import sys
import base64
import subprocess
import ctypes

FILE_DATA = {file_data}
RUN_AFTER = "{rau}"

def show_message_box(title, message, is_error=False):
    style = 0x10 if is_error else 0x40  # 0x10 for error icon, 0x40 for info icon
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, style)
    except:
        pass

def unpack_files():
    extract_dir = os.path.join(os.getcwd(), "unpacked_files")
    
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    for file_info in FILE_DATA:
        file_path = os.path.join(extract_dir, file_info['name'])
        with open(file_path, 'wb') as f:
            content = base64.b64decode(file_info['content'])
            f.write(content)
    
    return extract_dir

def main():
    try:
        extract_dir = unpack_files()

        show_message_box(
            "Extraction Complete", 
            f"Files successfully unpacked to:\\n{{extract_dir}}"
        )

        if RUN_AFTER:
            file_to_run = os.path.join(extract_dir, RUN_AFTER)
            if os.path.exists(file_to_run):
                ext = os.path.splitext(file_to_run)[1].lower()
                
                if ext == '.py':
                    subprocess.Popen(['python', file_to_run], cwd=extract_dir)
                elif ext in ['.exe', '.bat', '.cmd']:
                    subprocess.Popen([file_to_run], cwd=extract_dir)
                else:
                    if sys.platform == 'win32':
                        os.startfile(file_to_run)
                    elif sys.platform == 'darwin':  # macOS
                        subprocess.Popen(['open', file_to_run])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', file_to_run])
    except Exception as e:
        show_message_box("Error", f"An error occurred: {{e}}", is_error=True)

if __name__ == "__main__":
    main()
"""

        with open("temp.py", "w") as f:
            f.write(script)

        try:
            import PyInstaller.__main__
            PyInstaller.__main__.run([
                'temp.py',
                '--onefile',
                '--name=' + output_name,
                '--clean'
            ])

            os.remove("temp.py")
            output_location = os.path.join(os.getcwd(), 'dist', output_name + '.exe')
            print(f"Executable created successfully: {output_name}.exe\nLocation: {output_location}")
        except ImportError:
            print("PyInstaller is not installed. Please install it using 'pip install pyinstaller'.")
        except Exception as e:
            print(f"Failed to create executable: {e}")
    except Exception as e:
        print(e)

def main():
    files = []
    while True:
        file_path = input("Enter file path (Blank if finished):\n>>> ").strip('"')
        if not file_path:
            break
        if os.path.exists(file_path):
            files.append(file_path)
            print(f"Added file: {file_path}")
        else:
            print(f"File not found: {file_path}")

    if not files:
        print("No files to pack.")
        return

    print(f"Files: {files}")
    output_name = input("Enter output name (Not including file extensions):\n>>> ").strip()
    if not output_name:
        output_name = 'unpacker'

    run_after_unpack = input("Enter the file to run after unpacking (Blank if none):\n>>> ").strip('"')
    if run_after_unpack and not os.path.exists(run_after_unpack):
        print(f"File to run after unpacking not found: {run_after_unpack}")
        return

    pack(files, run_after_unpack, output_name)

if __name__ == "__main__":
    main()
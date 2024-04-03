from datetime import datetime

def log(data: str, log_file_path: str) -> None:
    with open(log_file_path, 'a') as f:
        f.write(f'{get_timestamp()}: {data}\n')

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TODO: create_log_folders()
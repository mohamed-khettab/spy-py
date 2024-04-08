from datetime import datetime


def log_data(file_path, data, mode="a"):
    with open(file_path, mode) as f:
        f.write(f"{timestamp()}: {data}\n")


def log_error(file_path, error):
    with open(file_path, "a") as f:
        f.write(f"{timestamp()}: {error}\n")


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

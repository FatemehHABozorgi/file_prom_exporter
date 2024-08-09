import os
import time
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Info

directories = ['/data/users/appuser/DTSfile']
sftp_directory = '/sftp/dts/home/'
files_to_tail = {
    '/data/users/appuser/docker_mongo_insert.log': 2,
    '/data/users/appuser/DTS_Job.log': 1
}

file_count = Gauge('file_count', 'Number of .json files in the directory', ['directory'])
last_mod_date = Gauge('last_mod_date', 'Last modification date of .json files in the directory in YYYYMMDD format', ['directory'])
sftp_files = Gauge('sftp_files', 'Files in the SFTP directory', ['file'])
log_file_tail = Gauge('log_file_tail', 'Tail lines from log files', ['file', 'line'])


def count_files(directory):
    log_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    count = len(log_files)
    file_count.labels(directory=directory).set(count)

    if log_files:
        latest_mod_time_epoch = max(os.path.getmtime(os.path.join(directory, f)) for f in log_files)
        latest_mod_date = datetime.fromtimestamp(latest_mod_time_epoch).strftime('%Y%m%d')
        last_mod_date.labels(directory=directory).set(int(latest_mod_date))
    else:
        last_mod_date.labels(directory=directory).set(19700101)

def list_sftp_files(directory):
    files = os.listdir(directory)
    sftp_files.clear()
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            sftp_files.labels(file=file).set(1)

def tail(file_path, num_lines):
    with open(file_path, 'r') as f:
        return f.readlines()[-num_lines:]

def write_tail_metrics(files):
    for file_path, num_lines in files.items():
        try:
            lines = tail(file_path, num_lines)
            print(lines)
            for i, line in enumerate(lines):
                log_file_tail.labels(file=file_path, line=str(lines)).set(1)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")


if __name__ == '__main__':
    start_http_server(9200)
    while True:
        for directory in directories:
            count_files(directory)
        list_sftp_files(sftp_directory)
        write_tail_metrics(files_to_tail)
        time.sleep(60)

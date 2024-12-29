# Prometheus-File-Metrics-Monitor

This repository contains a Python script that monitors specific directories and log files, exporting metrics to Prometheus. The script tracks the number of `.json` files in specified directories, the last modification date of these files, files in an SFTP directory, and the tail lines from specified log files.

## Features

- **File Count Monitoring**: Tracks the number of `.json` files in specified directories.
- **Last Modification Date**: Monitors and exports the last modification date of `.json` files in YYYYMMDD format.
- **SFTP Directory Monitoring**: Lists and tracks the file's presence in an SFTP directory.
- **Log File Tail Monitoring**: Exports the last N lines from specified log files.

## Prerequisites

- Python 3.6+
- Prometheus client library: [prometheus_client](https://github.com/prometheus/client_python)

Install the required Python libraries using pip:

```
pip install prometheus_client
```
## Setup
Clone the repository:

```
git clone https://github.com/FatemehHABozorgi/Prometheus-File-Metrics-Monitor.git
```
cd Prometheus-File-Metrics-Monitor

Edit the script if necessary:

To fit your monitoring needs, you can modify the script's directories, sftp_directory, and files_to_tail variables. Then you need to create a service to keep running the exporter.

```
cd /usr/lib/systemd/system/
vim prometheus-file-metrics-monitor.service
```
```
[Unit]
Description= Prometheus File Metrics Exporter
After=network-online.target

[Service]
User=root
Group=root
WorkingDirectory= /data/users/appuser/Prometheus-File-Metrics-Monitor
ExecStart=/bin/sh -c 'cd /data/users/appuser/Prometheus-File-Metrics-Monitor/ && python3 file-metrics-exporter.py'
ExecStop=/bin/kill -TERM ${MAINPID}
Restart=always

[Install]
WantedBy=multi-user.target
```
```
systemctl daemon-reload
systemctl enable prometheus-file-metrics-monitor.service && systemctl start prometheus-file-metrics-monitor.service && systemctl status prometheus-file-metrics-monitor.service
```
The script will start an HTTP server on port ```9200``` that Prometheus can scrape.

## Configure Prometheus:
Add the following job to your Prometheus configuration under the ```scrape_configs``` section and restart the Prometheus service:

```
vim /etc/prometheus/prometheus.yml
```
```
scrape_configs:

  - job_name: "file_metrics_monitor"
    static_configs:
      - targets: ["your-server-ip:9200"]
```
```
systemctl restart prometheus
```
## Usage

Directory Monitoring:
The script monitors directories listed in the directories variable. It counts the .json files and checks their last modification date.

SFTP Directory Monitoring:
The list_sftp_files function monitors files in the SFTP directory defined by sftp_directory.

Log File Tail Monitoring:
The script tails the last few lines of log files defined in the files_to_tail dictionary and exports them as metrics.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Author
Created by Fatemeh Haji Agha Bozorgi.

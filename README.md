# log-to-file

A simple, lightweight MicroPython file logger package with log rotation support. Designed to run efficiently on resource-constrained microcontrollers (e.g., ESP32, ESP8266, Raspberry Pi Pico).

[![License](https://img.shields.io/badge/license-SUL--1.0-green.svg)](LICENSE.md)

## Key Features

- **MicroPython Compatible**: Uses standard Python and MicroPython standard library functions (like `time.localtime` and `os.stat`).
- **File Rotation**: Supports log file size limits (`max_bytes`) and automatic backups rotation (`backup_count`).
- **Safe Writes**: Opens and closes the log file on every write, ensuring messages are flushed and safe from unexpected microcontroller resets.
- **Log Levels**: Supports standard levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- **String Formatting**: Support `%`-style string formatting arguments.

## Installation

Upload the package structure to your MicroPython device's filesystem:

```
/
└── lib/
    └── log_to_file/
        └── __init__.py
```

## Usage

```python
from log_to_file import FileLogger

# Initialize a logger with custom source, 10KB size limit and 3 backups
logger = FileLogger("app.log", source="main_sensor", level="INFO", max_bytes=10240, backup_count=3)

# Log messages
logger.info("System initialized")
logger.warning("Low memory warning: %d bytes free", 12340)
logger.error("Failed to connect to Wi-Fi")
```

The log entries will be formatted as `"[LEVEL] [SOURCE] Message"` where `LEVEL` is padded to 8 characters and `SOURCE` to 20 characters:
```
[INFO    ] [main_sensor         ] System initialized
[WARNING ] [main_sensor         ] Low memory warning: 12340 bytes free
[ERROR   ] [main_sensor         ] Failed to connect to Wi-Fi
```

## License

This project is licensed under the **Sustainable Use License (SUL-1.0)**. See the [LICENSE.md](LICENSE.md) file for details.
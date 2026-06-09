import os
import time

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

_level_names = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
    NOTSET: "NOTSET",
}

_level_values = {
    "CRITICAL": CRITICAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}

class FileLogger:
    def __init__(self, filename: str, level: str = "INFO", max_bytes: int = 0, backup_count: int = 0) -> None:
        self.filename = filename
        self.level_name = level.upper()
        self.level = _level_values.get(self.level_name, INFO)
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def _get_time_str(self) -> str:
        # Returns YYYY-MM-DD HH:MM:SS format
        t = time.localtime()
        return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

    def _rotate_files(self) -> None:
        if self.backup_count > 0:
            # Shift old backups rotation.log.N -> rotation.log.N+1
            for i in range(self.backup_count - 1, 0, -1):
                sfn = f"{self.filename}.{i}"
                dfn = f"{self.filename}.{i + 1}"
                try:
                    os.rename(sfn, dfn)
                except OSError:
                    pass
            # Rename rotation.log -> rotation.log.1
            dfn = f"{self.filename}.1"
            try:
                os.rename(self.filename, dfn)
            except OSError:
                pass
        else:
            # If no backups, delete the current file to restart
            try:
                os.remove(self.filename)
            except OSError:
                pass

    def _write(self, msg: str) -> None:
        if self.max_bytes > 0:
            try:
                size = os.stat(self.filename)[6]
            except OSError:
                size = 0

            if size >= self.max_bytes:
                self._rotate_files()

        try:
            with open(self.filename, "a") as f:
                f.write(msg + "\n")
        except OSError:
            pass

    def log(self, level_num: int, level_name: str, msg: str, *args) -> None:
        if level_num < self.level:
            return

        if args:
            try:
                msg = msg % args
            except Exception:  # noqa: S110
                pass

        time_str = self._get_time_str()
        formatted_msg = f"{time_str} [{level_name}] {msg}"
        self._write(formatted_msg)

    def debug(self, msg: str, *args) -> None:
        self.log(DEBUG, "DEBUG", msg, *args)

    def info(self, msg: str, *args) -> None:
        self.log(INFO, "INFO", msg, *args)

    def warning(self, msg: str, *args) -> None:
        self.log(WARNING, "WARNING", msg, *args)

    def error(self, msg: str, *args) -> None:
        self.log(ERROR, "ERROR", msg, *args)

    def critical(self, msg: str, *args) -> None:
        self.log(CRITICAL, "CRITICAL", msg, *args)

def main() -> None:
    logger = FileLogger("app.log", level="DEBUG")
    logger.info("Hello from log-to-file!")

__all__ = ["FileLogger", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]

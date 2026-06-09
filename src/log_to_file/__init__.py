import os
import time

try:
    ticks_ms = time.ticks_ms
except AttributeError:
    # Fallback for standard Python test environment
    def ticks_ms() -> int:
        return int(time.time() * 1000)


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
    def __init__(
        self,
        filename: str,
        source: str = "root",
        level: str = "INFO",
        max_bytes: int = 0,
        backup_count: int = 0,
        use_ticks: bool = False,
    ) -> None:
        self.filename = filename
        self.source = source
        self.level_name = level.upper()
        self.level = _level_values.get(self.level_name, INFO)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.use_ticks = use_ticks

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

        timestamp = ticks_ms() if self.use_ticks else int(time.time())

        formatted_msg = f"{timestamp} [{level_name:8}] [{self.source:20}] {msg}"
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


__all__ = [
    "FileLogger",
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]

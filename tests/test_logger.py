import os
import time
from log_to_file import Logger

def test_log_levels(tmp_path):
    log_file = str(tmp_path / "test.log")
    
    # Logger with INFO level
    logger = Logger(log_file, level="INFO")
    
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    
    # Read the log file
    with open(log_file, "r") as f:
        content = f.read()
        
    assert "debug message" not in content
    assert "info message" in content
    assert "warning message" in content
    assert "error message" in content

def test_log_formatting(tmp_path):
    log_file = str(tmp_path / "test.log")
    # By default, source is "root", use_ticks is False
    logger = Logger(log_file, level="DEBUG")
    
    logger.info("test format")
    
    with open(log_file, "r") as f:
        line = f.readline().rstrip("\n")
    
    # Format should be: "timestamp [INFO    ] [root                ] test format"
    # where timestamp is a Unix timestamp (integer seconds)
    parts = line.split(" ", 1)
    assert len(parts) == 2
    timestamp_str, msg_part = parts
    
    assert timestamp_str.isdigit()
    assert msg_part == "[INFO    ] [root                ] test format"

def test_log_formatting_ticks(tmp_path):
    log_file = str(tmp_path / "test.log")
    # Initialize with use_ticks=True
    logger = Logger(log_file, use_ticks=True, level="DEBUG")
    
    logger.info("test ticks")
    
    with open(log_file, "r") as f:
        line = f.readline().rstrip("\n")
        
    parts = line.split(" ", 1)
    assert len(parts) == 2
    timestamp_str, msg_part = parts
    
    assert timestamp_str.isdigit()
    assert msg_part == "[INFO    ] [root                ] test ticks"

def test_log_custom_source(tmp_path):
    log_file = str(tmp_path / "test.log")
    logger = Logger(log_file, source="my_module", level="DEBUG")
    
    logger.debug("debug custom source")
    
    with open(log_file, "r") as f:
        line = f.readline().rstrip("\n")
        
    parts = line.split(" ", 1)
    assert len(parts) == 2
    timestamp_str, msg_part = parts
    
    assert timestamp_str.isdigit()
    assert msg_part == "[DEBUG   ] [my_module           ] debug custom source"

def test_log_arguments(tmp_path):
    log_file = str(tmp_path / "test.log")
    logger = Logger(log_file, level="DEBUG")
    
    logger.info("hello %s %d", "world", 42)
    
    with open(log_file, "r") as f:
        content = f.read()
        
    assert "hello world 42" in content

def test_log_rotation_with_backups(tmp_path):
    log_file = str(tmp_path / "rotation.log")
    
    # Max size 60 bytes, 2 backups
    # Each log entry will be about 30-40 bytes
    logger = Logger(log_file, level="INFO", max_bytes=60, backup_count=2)
    
    # Write some logs
    logger.info("Line 1")  # Writes to rotation.log
    logger.info("Line 2")  # Triggers rotation?
    logger.info("Line 3")
    logger.info("Line 4")
    logger.info("Line 5")
    
    # Verify backup files exist
    assert os.path.exists(log_file)
    assert os.path.exists(log_file + ".1")
    assert os.path.exists(log_file + ".2")
    assert not os.path.exists(log_file + ".3")

def test_log_rotation_without_backups(tmp_path):
    log_file = str(tmp_path / "rotation_nobackup.log")
    
    # Max size 60 bytes, 0 backups
    logger = Logger(log_file, level="INFO", max_bytes=60, backup_count=0)
    
    logger.info("Line 1")
    logger.info("Line 2")
    logger.info("Line 3")
    
    # Verify no backup files exist
    assert os.path.exists(log_file)
    assert not os.path.exists(log_file + ".1")
    
    # The file should be truncated and contain the last message
    with open(log_file, "r") as f:
        content = f.read()
    assert "Line 3" in content
    assert "Line 1" not in content

def test_logger_always(tmp_path):
    # Test always logs when level is INFO
    log_file_info = str(tmp_path / "test_info.log")
    logger_info = Logger(log_file_info, level="INFO")
    logger_info.always("always message info")
    logger_info.info("info message info")
    
    with open(log_file_info, "r") as f:
        content_info = f.read()
    assert "always message info" in content_info
    assert "info message info" in content_info
    
    # Test always logs when level is CRITICAL
    log_file_crit = str(tmp_path / "test_crit.log")
    logger_crit = Logger(log_file_crit, level="CRITICAL")
    logger_crit.always("always message crit")
    logger_crit.info("info message crit")
    
    with open(log_file_crit, "r") as f:
        content_crit = f.read()
    assert "always message crit" in content_crit
    assert "info message crit" not in content_crit
    
    # Test always does NOT log when level is None
    log_file_none = str(tmp_path / "test_none.log")
    logger_none = Logger(log_file_none, level=None)
    logger_none.always("always message none")
    logger_none.critical("critical message none")
    
    if os.path.exists(log_file_none):
        with open(log_file_none, "r") as f:
            content_none = f.read()
        assert "always message none" not in content_none
        assert "critical message none" not in content_none

    # Test always does NOT log when level is "NONE"
    log_file_none_str = str(tmp_path / "test_none_str.log")
    logger_none_str = Logger(log_file_none_str, level="NONE")
    logger_none_str.always("always message none str")
    logger_none_str.critical("critical message none str")
    
    if os.path.exists(log_file_none_str):
        with open(log_file_none_str, "r") as f:
            content_none_str = f.read()
        assert "always message none str" not in content_none_str
        assert "critical message none str" not in content_none_str

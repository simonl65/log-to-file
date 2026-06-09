import os
import time
from log_to_file import FileLogger

def test_log_levels(tmp_path):
    log_file = str(tmp_path / "test.log")
    
    # Logger with INFO level
    logger = FileLogger(log_file, level="INFO")
    
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
    logger = FileLogger(log_file, level="DEBUG")
    
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
    logger = FileLogger(log_file, use_ticks=True, level="DEBUG")
    
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
    logger = FileLogger(log_file, source="my_module", level="DEBUG")
    
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
    logger = FileLogger(log_file, level="DEBUG")
    
    logger.info("hello %s %d", "world", 42)
    
    with open(log_file, "r") as f:
        content = f.read()
        
    assert "hello world 42" in content

def test_log_rotation_with_backups(tmp_path):
    log_file = str(tmp_path / "rotation.log")
    
    # Max size 60 bytes, 2 backups
    # Each log entry will be about 30-40 bytes
    logger = FileLogger(log_file, level="INFO", max_bytes=60, backup_count=2)
    
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
    logger = FileLogger(log_file, level="INFO", max_bytes=60, backup_count=0)
    
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

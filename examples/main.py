from log_to_file import Logger

logger = Logger("log.txt", level="DEBUG")


def main():
    print("Hello from log-checker!")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    logger.always("This is an always message.")


if __name__ == "__main__":
    main()

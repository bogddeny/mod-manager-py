import logging
import main

log = logging.getLogger("logger")

log.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("manager.log")

console_handler = logging.StreamHandler()

if main.LOG_DEBUG is True:
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)
else:
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

log.addHandler(file_handler)
log.addHandler(console_handler)
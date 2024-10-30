import logging

try:
    2 / 0
except Exception as e:
    logging.warning(e, exc_info=True)

print(1)
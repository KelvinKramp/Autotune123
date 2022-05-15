# from Correy Schaffer.

import logging
from definitions import ROOT_DIR
import os

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

filename = os.path.join(ROOT_DIR, "debug.log")
logging.basicConfig(filename=filename, level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')



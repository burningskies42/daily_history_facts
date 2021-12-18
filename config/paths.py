import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = ROOT / "config.yaml"
if PACKAGE_ROOT not in sys.path:
    sys.path.append(str(PACKAGE_ROOT))

STATIC_FILES_PATH = ROOT / "static"

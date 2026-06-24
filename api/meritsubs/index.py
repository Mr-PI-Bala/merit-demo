"""merit-demo consumer host â€” meritsubs ASGI entry (MERIT Â§0.D.1)."""
import sys
from pathlib import Path

VENDOR = Path(__file__).resolve().parents[2] / "vendor" / "meritsubs"
sys.path.insert(0, str(VENDOR))

from api.app import app  # noqa: F401 â€” Vercel @vercel/python ASGI

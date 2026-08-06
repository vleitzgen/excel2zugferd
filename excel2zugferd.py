"""
Module excel2zugferd
"""

import ctypes
import os
from pathlib import Path
import sys
import tempfile
import traceback


def run() -> None:
    from src.middleware import Middleware
    from src.oberflaeche_excel2zugferd import OberflaecheExcel2Zugferd
    from src.oberflaeche_ini import OberflaecheIniFile
    from src.stammdaten import STAMMDATEN

    middleware: Middleware = Middleware()

    if middleware.check_args(sys.argv):
        return

    if middleware.ini_file.exists_ini_file() is None:
        middleware.ini_file.create_ini_file(middleware.ini_file.set_default_content())
        oberfl = OberflaecheIniFile(STAMMDATEN, middleware)
    else:
        oberfl = OberflaecheExcel2Zugferd(STAMMDATEN, middleware)
    oberfl.loop()


def report_fatal_error(error: Exception) -> None:
    app_data = Path(os.getenv("APPDATA") or tempfile.gettempdir())
    log_directory = app_data / "excel2zugferd"
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file = log_directory / "excel2zugferd-crash.log"
    log_file.write_text(traceback.format_exc(), encoding="utf-8")

    message = (
        "Excel2ZUGFeRD konnte nicht gestartet werden.\n\n"
        f"{error}\n\nDetails wurden gespeichert in:\n{log_file}"
    )
    ctypes.windll.user32.MessageBoxW(0, message, "Excel2ZUGFeRD - Startfehler", 0x10)


if __name__ == "__main__":
    try:
        run()
    except Exception as ex:
        report_fatal_error(ex)
        sys.exit(1)

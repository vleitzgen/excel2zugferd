"""
Module excel2zugferd - Main Entry Point
"""

from sys import argv, exit
import logging
from typing import Union, Any

import src.oberflaeche_ini
import src.oberflaeche_excel2zugferd
from src.stammdaten import STAMMDATEN
from src.middleware import Middleware
import src


def _initialize_middleware() -> Middleware:
    """Initialize middleware and return configured instance."""
    middleware = Middleware()
    
    # Check command line arguments (e.g., quiet mode, file inputs)
    if middleware.check_args(argv):
        exit(0)
    
    return middleware


def _initialize_ui(middleware: Middleware) -> Any:
    """Initialize and return the appropriate UI window.
    
    Args:
        middleware: Configured Middleware instance
        
    Returns:
        GUI window object (OberflaecheIniFile or OberflaecheExcel2Zugferd)
    """
    try:
        # First time: INI file setup required
        if middleware.ini_file.exists_ini_file() is None:
            middleware.ini_file.create_ini_file(
                middleware.ini_file.set_default_content()
            )
            # Type: OberflaecheIniFile
            return src.oberflaeche_ini.OberflaecheIniFile(
                STAMMDATEN, middleware
            )
        # Subsequent runs: Main application window
        else:
            # Type: OberflaecheExcel2Zugferd
            return src.oberflaeche_excel2zugferd.OberflaecheExcel2Zugferd(
                STAMMDATEN, middleware
            )
    
    except Exception as e:
        middleware.logger.error(
            f"Failed to initialize UI: {str(e)}", 
            exc_info=True
        )
        raise


def main():
    """Main application entry point."""
    middleware = None
    try:
        # Initialize
        middleware = _initialize_middleware()
        ui_window = _initialize_ui(middleware)
        
        # Start GUI event loop
        if ui_window and hasattr(ui_window, 'root'):
            ui_window.root.mainloop()
        else:
            raise RuntimeError("UI window initialization failed: invalid window object")
    
    except KeyboardInterrupt:
        # User closed the app normally
        pass
    except Exception as e:
        if middleware and hasattr(middleware, 'logger'):
            middleware.logger.error(
                f"Application startup failed: {str(e)}", 
                exc_info=True
            )
        else:
            logging.error(
                f"Application startup failed: {str(e)}", 
                exc_info=True
            )
        exit(1)


if __name__ == "__main__":
    main()

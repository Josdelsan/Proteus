# ==========================================================================
# File: __main__.py
# Description: entry point for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

from proteus import PROTEUS_VERSION
from proteus.app import ProteusApplication

# --------------------------------------------------------------------------
# Function: main
# Description: Entry point for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

def main() -> int:
    print("="*40)
    print(f"PROTEUS application {PROTEUS_VERSION}")
    print("="*40)

    app = ProteusApplication()
    return app.run()

if __name__ == '__main__':
    main()
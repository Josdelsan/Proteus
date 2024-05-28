# ==========================================================================
# File: __main__.py
# Description: entry point for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

from pathlib import Path
import sys
from proteus import PROTEUS_VERSION, parser
from proteus.app import ProteusApplication

# --------------------------------------------------------------------------
# Function: main
# Description: Entry point for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------


def main() -> int:

    args = parser.parse_args()

    project_path: Path = None
    if args.project_path:
        project_path = Path(args.project_path)
        if not project_path.exists():
            print(f"ERROR: The project path '{project_path}' does not exist.")
            return 1

    print("=" * 40)
    print(f"PROTEUS application {PROTEUS_VERSION}")
    print("=" * 40)

    app = ProteusApplication(project_path=project_path)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())

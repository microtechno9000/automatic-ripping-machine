#!/bin/bash

# ARM_CODE is set in the arm_setup_ui.sh as a global value

ARM_UI=${ARM_CODE}/arm/runui.py

echo "Starting ARM Web Interface - python - script [${ARM_UI}]"
chmod +x ${ARM_UI}
exec /bin/python3 ${ARM_UI}
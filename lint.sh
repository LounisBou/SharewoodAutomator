#!/bin/bash

# Run Pylint on the sharewoodautomator package with the specified configuration
python -m pylint --rcfile=.pylintrc sharewoodautomator/

# Optional: Uncomment to also lint tests
# python -m pylint --rcfile=.pylintrc tests/

# Exit with the status of the last command
exit $?
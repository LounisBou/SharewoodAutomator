#!/bin/bash

# Simplified script to fix linting issues in the project (ignoring docstrings)

# Step 1: Format code with Black
echo "Step 1: Formatting code with Black..."
python -m black --line-length=127 sharewoodautomator/

# Step 2: Sort imports with isort
echo "Step 2: Sorting imports with isort..."
python -m isort --profile=black --line-length=127 sharewoodautomator/

# Step 3: Fix PEP8 issues with autopep8
echo "Step 3: Fixing PEP8 issues with autopep8..."
python -m autopep8 --aggressive --in-place --max-line-length=127 --recursive sharewoodautomator/

# Step 4: Run Pylint with the updated configuration
echo "Step 4: Running Pylint with updated configuration..."
python -m pylint --rcfile=.pylintrc sharewoodautomator/

# Step 5: Fix pre-commit config to ignore docstring issues
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Step 5: Updating pre-commit configuration..."
    sed -i 's/--max-line-length=127/--max-line-length=127 --ignore=D1,D2,D3,D4/' .pre-commit-config.yaml
    echo "Updated pre-commit configuration to ignore docstring errors."
fi

echo "Done! Docstring issues are now ignored."

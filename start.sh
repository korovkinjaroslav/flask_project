#!/bin/bash
export PORT=5000
unset PIP_USER

pip install -r requirments.txt || echo "Pip install failed, but continuing as packages might be pre-installed via system."

echo "Starting application..."

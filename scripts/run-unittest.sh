#!/bin/bash

# Superheroes API - Unit Test Runner
# Simple shell script to run all unit tests

echo "============================================================"
echo "🧪 Bank API - UNIT TEST RUNNER"
echo "============================================================"

# Change to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f "env/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

echo ""
echo "📋 Running all unit tests..."
echo "----------------------------------------"

# Run all tests with verbose output
python manage.py test --verbosity=2

TEST_EXIT_CODE=$?


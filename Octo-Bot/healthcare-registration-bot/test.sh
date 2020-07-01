# Runs all unit tests in the /test directory

# Install dependencies
if ! command -v python3 >/dev/null 2>&1; then
echo "Please install python3 first!"
fi
pip3 install selenium >/dev/null

echo "All dependencies have been fulfilled!"

# Run all unit tests
python3 test/test.py

echo
echo "Please check if tests succeeded!"

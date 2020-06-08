# Runs all unit tests in the ./tests directory

# Install dependencies
if ! command -v python3 >/dev/null 2>&1; then
echo "Please install python3 first!"
fi
pip3 install scapy >/dev/null

# Setup permissions
chmod a+x *.sh &&

# Copy required files to the right folder
cp -r tests/test_*.py bot 

# Run all tests
for test in bot/test_*.py
do
    python3 $test
done

# Remove copied files
rm -f bot/test_*.py

echo
echo "Please check if the tests succeeded!"

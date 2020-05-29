# Runs all unit tests in the ./tests directory

# Setup permissions
chmod a+x *.sh &&

# Copy required files to the right folder
cp -r captures bot && 
cp -r tests/test_*.py bot 

# Run all tests
for test in bot/test_*.py
do
    python $test
done

# Remove copied files
rm -rf bot/captures &&
rm -f bot/test_*.py

echo
echo "Please check if the tests succeeded!"

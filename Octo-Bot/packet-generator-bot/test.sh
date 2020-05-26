chmod a+x *.sh &&

cp -r captures bot && 
cp -r tests/test_*.py bot 

for test in bot/test_*.py
do
    python $test
done

rm -rf bot/captures &&
rm -f bot/test_*.py

echo
echo "Please check if the tests succeeded!"

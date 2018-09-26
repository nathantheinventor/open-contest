ls /
echo "-----"
ls /test
echo "------"
cp -r /test /tmp/test
echo "-----------------"
ls /var/run/
echo "-------------------"
docker run -v /tmp/test/:/source/ nathantheinventor/open-contest-dev-c-runner 2 5
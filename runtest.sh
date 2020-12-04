SECONDS=0

unittest=false
flake8=false
testcase=false
clean=false

if [ $# -eq 0 ]; then
    flake8=true
    unittest=true
else
    for argval in "$@"
    do
        if [ "$argval" == "clean" ]; then
            clean=true
        fi
        if [ "$argval" == "flake8" ]; then
            flake8=true
        fi
        if [ "$argval" == "unit" ] || [ "$argval" == "unittest" ]; then
            unittest=true
        fi
        if [ "$argval" == "all" ]; then
            unittest=true
            flake8=true
        fi
        if [ "$argval" == "case" ]; then
            testcase=true
        fi
        if [ "$testcase" = true ] && [[ "$argval" =~ ^tests.* ]]; then
            label=$argval
        fi
    done
fi

if [ "$flake8" = true ]; then
    echo "# checking flake8..."
    if flake8 --jobs=auto; then
        echo "OK\n"
    fi
fi
if [ "$clean" = true ]; then
    echo "# running unittests with clean db..."
    python manage.py test --noinput --settings=tests.test_settings
fi
if [ "$unittest" = true ]; then
    echo "# running unittests..."
    python manage.py test --keepdb --settings=tests.test_settings
fi
if [ "$testcase" = true ]; then
    echo "# running specific case $label..."
    python manage.py test --keepdb --settings=tests.test_settings $label --debug-mode
fi

if [ "$clean" = false ] && [ "$flake8" = false ] && [ "$unittest" = false ] && [ "$testcase" = false ]; then
    echo "Usage: ./runtest.sh [options] ..."
    echo "* run all tests if no options provided"
    echo "\nOptions:"
    echo "flake8\t\t\t run flake8 only"
    echo "unit, unittest\t\t run unit test only"
    echo "case [case name]\t run a specific unit test in debug-mode"
    echo " - example of case name\t [tests.accounts.test_login.LoginTest]"
    echo "all\t\t\t run both flake8 and unit test"
    echo "clean\t\t\t run unit test without --keepdb option"
else
    duration=$SECONDS
    echo "# test finished in $duration seconds."
fi

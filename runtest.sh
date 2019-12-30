SECONDS=0

unittest=false
flake8=false

if [ $# -eq 0 ]; then
    unittest=true
else
    for argval in "$@"
    do
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
    done
fi

if [ "$flake8" = true ]; then
    echo "# checking flake8..."
    flake8 --jobs=auto
fi
if [ "$unittest" = true ]; then
    echo "# running unittests..."
    python manage.py test --parallel --keepdb --settings=tests.test_settings
fi

if [ "$flake8" = false ] && [ "$unittest" = false ]; then
    echo "Usage: ./runtest.sh [options] ..."
    echo "* run unit test if no options"
    echo "\nOptions:"
    echo "flake8\t\t\t run flake8 only"
    echo "unit, unittest\t\t run unit test only"
    echo "all\t\t\t run both flake8 and unit test"
else
    duration=$SECONDS
    echo "# test finished in $duration seconds."
fi

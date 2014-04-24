#!/bin/bash
export PYTHONPATH=/usr/local/lib64/python2.6/site-packages/:$PYTHONPATH

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
MANAGE="$DIR/manage.py"

function run {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error with $@"
        exit 1
    fi
    return $status
}

echo "Updating product_details"
echo "===================="
run $MANAGE update_product_details

echo ""
echo "Collecting data from Google Analytics"
echo "====================================="
run $MANAGE collect_ga_data

echo ""
echo "Updating leaderboard"
echo "===================="
run $MANAGE update_leaderboard

echo ""
echo "Generating media .htaccess"
echo "===================="
run $MANAGE generate_media_htaccess

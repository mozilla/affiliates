#!/bin/bash
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

echo "Collecting data from Google Analytics"
echo "====================================="
run $MANAGE collect_ga_data

echo ""
echo "Updating leaderboard"
echo "===================="
run $MANAGE update_leaderboard

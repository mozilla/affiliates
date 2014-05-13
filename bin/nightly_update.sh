#!/bin/bash
export PYTHONPATH=/usr/local/lib64/python2.6/site-packages/:$PYTHONPATH

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
MANAGE="$DIR/manage.py"
QUIET=""

while getopts "q" o; do
    case "${o}" in
        q)
            QUIET="-q"
            ;;
    esac
done
shift $((OPTIND-1))

function run {
    PYTHONWARNINGS="ignore" "$@" $QUIET
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error with $@"
        exit 1
    fi
    return $status
}

if [ -z "$QUIET" ]; then
    echo "Updating product_details"
    echo "========================"
fi
run $MANAGE update_product_details

#if [ -z "$QUIET" ]; then
#    echo ""
#    echo "Collecting data from Google Analytics"
#    echo "====================================="
#fi
#run $MANAGE collect_ga_data

if [ -z "$QUIET" ]; then
    echo ""
    echo "Aggregating old datapoints"
    echo "=========================="
fi
run $MANAGE aggregate_old_datapoints

if [ -z "$QUIET" ]; then
    echo ""
    echo "Updating leaderboard"
    echo "===================="
fi
run $MANAGE update_leaderboard

if [ -z "$QUIET" ]; then
    echo ""
    echo "Generating media .htaccess"
    echo "=========================="
fi
run $MANAGE generate_media_htaccess

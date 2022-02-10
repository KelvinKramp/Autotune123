#!/usr/bin/env bash
RECOMMENDS_REPORT=true
pwd=$(pwd)
cd ~
if [[ $RECOMMENDS_REPORT == "true" ]]; then
    # Set the report file name, so we can let the user know where it is and cat
    # it to the screen
    report_file=myopenaps/autotune/autotune_recommendations.log

    echo
    echo "Autotune pump profile recommendations:"
    echo "---------------------------------------------------------"

    # Let the user know where the Autotune Recommendations are logged
    echo "Recommendations Log File: $report_file"
    echo

    # Run the Autotune Recommends Report
    oref0-autotune-recommends-report $directory

    # Go ahead and echo autotune_recommendations.log to the terminal, minus blank lines
    cat $report_file | egrep -v "\| *\| *$"
fi



cp $report_file $pwd/new_profile.csv
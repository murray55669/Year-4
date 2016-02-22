#!/bin/bash

function header {
    printf '\e[1m\e[44m%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
    echo $1
    printf '%*s\e[0m\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}
function subheader {
    printf '\e[105m%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
    echo $1
    printf '%*s\e[0m\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}
function msi {
    header "TRACE 1"
    subheader "Trace 1; MSI; line size: 2"
    python main.py trace1.txt MSI 2
    subheader "Trace 1; MSI; line size: 4"
    python main.py trace1.txt MSI 4
    subheader "Trace 1; MSI; line size: 8"
    python main.py trace1.txt MSI 8
    subheader "Trace 1; MSI; line size: 16"
    python main.py trace1.txt MSI 16
    header "TRACE 2"
    subheader "Trace 2; MSI; line size: 2"
    python main.py trace2.txt MSI 2
    subheader "Trace 2; MSI; line size: 4"
    python main.py trace2.txt MSI 4
    subheader "Trace 2; MSI; line size: 8"
    python main.py trace2.txt MSI 8
    subheader "Trace 2; MSI; line size: 16"
    python main.py trace2.txt MSI 16
}
function mesi {
    header "TRACE 1"
    subheader "Trace 1; MESI; line size: 2"
    python main.py trace1.txt MESI 2
    subheader "Trace 1; MESI; line size: 4"
    python main.py trace1.txt MESI 4
    subheader "Trace 1; MESI; line size: 8"
    python main.py trace1.txt MESI 8
    subheader "Trace 1; MESI; line size: 16"
    python main.py trace1.txt MESI 16
    header "TRACE 2"
    subheader "Trace 2; MESI; line size: 2"
    python main.py trace2.txt MESI 2
    subheader "Trace 2; MESI; line size: 4"
    python main.py trace2.txt MESI 4
    subheader "Trace 2; MESI; line size: 8"
    python main.py trace2.txt MESI 8
    subheader "Trace 2; MESI; line size: 16"
    python main.py trace2.txt MESI 16
}
function mes {
    header "TRACE 1"
    subheader "Trace 1; MES; line size: 2"
    python main.py trace1.txt MES 2
    subheader "Trace 1; MES; line size: 4"
    python main.py trace1.txt MES 4
    subheader "Trace 1; MES; line size: 8"
    python main.py trace1.txt MES 8
    subheader "Trace 1; MES; line size: 16"
    python main.py trace1.txt MES 16
    header "TRACE 2"
    subheader "Trace 2; MES; line size: 2"
    python main.py trace2.txt MES 2
    subheader "Trace 2; MES; line size: 4"
    python main.py trace2.txt MES 4
    subheader "Trace 2; MES; line size: 8"
    python main.py trace2.txt MES 8
    subheader "Trace 2; MES; line size: 16"
    python main.py trace2.txt MES 16
}

if [ $1 == 'MSI' ] 
then
    msi
elif [ $1 == 'MESI' ]
then
    mesi
elif [ $1 == 'MES' ]
then
    mes
else
    msi
    mesi
    mes
fi

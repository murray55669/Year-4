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
    header "TESTING MSI"
    subheader "write to cache block in state shared in another cache"
    python main.py test_0.trace MSI 2 4
    subheader "read to cache block in state modified in another cache"
    python main.py test_1.trace MSI 2 4
    subheader "read to cache block in state shared in another cache"
    python main.py test_2.trace MSI 2 4
    subheader "write to cache block in state modified in another cache"
    python main.py test_3.trace MSI 2 4
}
function mesi {
    header "TESTING MESI"
    subheader "write to cache block in state exclusive in another cache"
    python main.py test_0.trace MESI 2 4
    subheader "read to cache block in state modified in another cache"
    python main.py test_1.trace MESI 2 4
    subheader "read to cache block in state exclusive in another cache"
    python main.py test_2.trace MESI 2 4
    subheader "write to cache block in state modified in another cache"
    python main.py test_3.trace MESI 2 4
    subheader "read to cache block in state shared in another cache"
    python main.py test_4.trace MESI 2 4
    subheader "write to cache block in state shared in another cache"
    python main.py test_5.trace MESI 2 4
}
function mes {
    header "TESTING MES"
    subheader "write to cache block in state exclusive in another cache"
    python main.py test_0.trace MES 2 4
    subheader "read to cache block in state modified in another cache"
    python main.py test_1.trace MES 2 4
    subheader "read to cache block in state exclusive in another cache"
    python main.py test_2.trace MES 2 4
    subheader "write to cache block in state modified in another cache"
    python main.py test_3.trace MES 2 4
    subheader "read to cache block in state shared in another cache"
    python main.py test_4.trace MES 2 4
    subheader "write to cache block in state shared in another cache"
    python main.py test_5.trace MES 2 4
}

if [ $# -eq 0 ]
then
    msi
    mesi
    mes
else
    if [ $1 == 'MSI' ] 
    then
        msi
    elif [ $1 == 'MESI' ]
    then
        mesi
    elif [ $1 == 'MES' ]
    then
        mes
    fi
fi

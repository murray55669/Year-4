#!/bin/bash

if [ $1 == '1' ] 
then
  if [ $2 == '0' ]
  then
    echo '1 0'
    COUNTER=5
    while [ $COUNTER -le 100 ]; do
      ./waf --run "scratch/0-test --question=1 --rayleigh=false --aarfcara=0 --separation=$COUNTER --nodecount=1"
      let COUNTER=COUNTER+5
    done
  elif [ $2 == '1' ]
  then
    echo '1 1'
    COUNTER=5
    while [ $COUNTER -le 100 ]; do
      ./waf --run "scratch/0-test --question=1 --rayleigh=true --aarfcara=0 --separation=$COUNTER --nodecount=1"
      let COUNTER=COUNTER+5
    done
  elif [ $2 == '2' ]
  then 
    echo '1 2'
    COUNTER=5
    while [ $COUNTER -le 100 ]; do
      ./waf --run "scratch/0-test --question=1 --rayleigh=false --aarfcara=1 --separation=$COUNTER --nodecount=1"
      let COUNTER=COUNTER+5
    done
  elif [ $2 == '3' ]
  then
    echo '1 3'
    COUNTER=5
    while [ $COUNTER -le 100 ]; do
      ./waf --run "scratch/0-test --question=1 --rayleigh=true --aarfcara=1 --separation=$COUNTER --nodecount=1"
      let COUNTER=COUNTER+5
    done
  fi
elif [ $1 == '2' ]
then
  if [ $2 == '0' ]
  then
    echo '2 0'
    ./waf --run "scratch/0-test --question=2 --rayleigh=false --aarfcara=0 --separation=0 --nodecount=1"
    COUNTER=5
    while [ $COUNTER -le 50 ]; do
      ./waf --run "scratch/0-test --question=2 --rayleigh=false --aarfcara=0 --separation=0 --nodecount=$COUNTER"
      let COUNTER=COUNTER+5
    done
  elif [ $2 == '1' ]
  then
    echo '2 1'
    ./waf --run "scratch/0-test --question=2 --rayleigh=false --aarfcara=1 --separation=0 --nodecount=1"
    COUNTER=5
    while [ $COUNTER -le 50 ]; do
      ./waf --run "scratch/0-test --question=2 --rayleigh=false --aarfcara=1 --separation=0 --nodecount=$COUNTER"
      let COUNTER=COUNTER+5
    done
  fi
elif [ $1 == '3' ]
then
  if [ $2 == '0' ]
  then
    echo '3 0'
    ./waf --run "scratch/0-test --question=3 --rayleigh=true --aarfcara=0 --separation=0 --nodecount=1"
    COUNTER=5
    while [ $COUNTER -le 50 ]; do
      ./waf --run "scratch/0-test --question=3 --rayleigh=true --aarfcara=0 --separation=0 --nodecount=$COUNTER"
      let COUNTER=COUNTER+5
    done
  elif [ $2 == '1' ]
  then
    echo '3 1'
    ./waf --run "scratch/0-test --question=3 --rayleigh=true --aarfcara=1 --separation=0 --nodecount=1"
    COUNTER=5
    while [ $COUNTER -le 50 ]; do
      ./waf --run "scratch/0-test --question=3 --rayleigh=true --aarfcara=1 --separation=0 --nodecount=$COUNTER"
      let COUNTER=COUNTER+5
    done
  fi
fi
#!/bin/bash

## default value
VALUE_L="1"
IS_MODE="n"
GAME_TIME="180"                  # game time (s)
RESULT_LOG_JSON="result.json"    # result log file
INPUT_RAMDOM_SEED=""             # random seed

## get args level setting
while getopts l:m:s:t:f:r: OPT
do
  case $OPT in
    "l" ) VALUE_L="$OPTARG" ;;
    "m" ) IS_MODE="$OPTARG" ;;
    "t" ) GAME_TIME="$OPTARG" ;;
    "f" ) RESULT_LOG_JSON="$OPTARG" ;;
    "r" ) INPUT_RAMDOM_SEED="$OPTARG" ;;
  esac
done
echo "level: $VALUE_L"
echo "is_manual_controll: $IS_MODE"

## set field parameter for level 1
DROP_SPEED="1000"        # drop speed (s)
RANDOM_SEED="0"          # random seed for field
OBSTACLE_HEIGHT="0"      # obstacle height (blocks)
OBSTACLE_PROBABILITY="0" # obstacle probability (percent)
BLOCK_ORDER="0"          # block order 0=static/random 2=special

case $VALUE_L in
    "0" ) GAME_TIME="-1" ;;
    "1" ) RANDOM_SEED="0" ;;
    "2" ) RANDOM_SEED="-1" ;;
    "3" ) RANDOM_SEED="-1"; OBSTACLE_HEIGHT="10"; OBSTACLE_PROBABILITY="40"; ;;
    "777" ) RANDOM_SEED="0" BLOCK_ORDER="2" ;;
    * ) echo "invalid level: $VALUE_L"; exit 1;;
esac

if [ ! -z ${INPUT_RAMDOM_SEED} ]; then
    # fix random seed from given value.
    RANDOM_SEED=${INPUT_RAMDOM_SEED}
fi
echo "game_time: $GAME_TIME"
echo "RANDOM_SEED: $RANDOM_SEED"
echo "OBSTACLE_HEIGHT: ${OBSTACLE_HEIGHT}"
echo "OBSTACLE_PROBABILITY: ${OBSTACLE_PROBABILITY}"

## start game
python3 game_manager/game_manager.py --game_time ${GAME_TIME} --seed ${RANDOM_SEED} --obstacle_height ${OBSTACLE_HEIGHT} --obstacle_probability ${OBSTACLE_PROBABILITY} --drop_interval ${DROP_SPEED} --mode ${IS_MODE} --resultlogjson ${RESULT_LOG_JSON} --block_order ${BLOCK_ORDER}

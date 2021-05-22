#!
FS=$(dirname "$0")
export PD_BIN_PATH=/Applications/Pd-extended.app/Contents/Resources/bin
export EFFECTS_CONFIG=$FS/effects_config.csv
uvicorn src.api:app --reload
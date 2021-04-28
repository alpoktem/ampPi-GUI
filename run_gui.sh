#!
#Development run:
#uvicorn src.api:app --reload

FS=$(dirname "$0")
gunicorn3 -k uvicorn.workers.UvicornWorker --chdir $FS src.api:app --reload 1> $FS/job.out 2> $FS/job.err

# thesis-tracker

`thesis-tracker` is a simple command line Python program that keeps track of the time spent working on a task.
It depends on the package `pandas`, which makes it easy to extend the functionality.

The available commands are returned by running the program with the flag `--help`.

```bash
> python3 tracker.py --help
usage: thesis-time-tracker [-h] [-c TEXT] [-V] [-v] [-f FILENAME] [-r] {start,stop,total,this_week,avg_week}

Logs the time spent working on the thesis.

positional arguments:
  {start,stop,total,this_week,avg_week}
                        The operation to be performed. 'start' will add a new log entry with the (current) start time. 'stop' will complete the last entry
                        with the (current) end time. 'total' returns the total amount of time tracked. 'this_week' returns the amount of time tracked
                        during the current week. 'avg_week' averages the total amount of time tracked since the first week until the current week.

options:
  -h, --help            show this help message and exit
  -c TEXT, --comment TEXT
                        A comment to be stored along the logged start/end time.
  -V, --version         show program's version number and exit
  -v, --verbose         TODO
  -f FILENAME, --log-file-path FILENAME
                        The path to the log file.
  -r, --reuse-comment   use the same comment as in the previous entry

Copyright 2023 - heckej
```

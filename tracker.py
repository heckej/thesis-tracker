import argparse
import datetime
import os
import csv
import pandas as pd

VERSION = "0.3.0"
AUTHOR  = "heckej"
YEAR    = 2023


def main():
    parser = argparse.ArgumentParser(
        prog = 'thesis-time-tracker',
        description = 'Logs the time spent working on the thesis.',
        epilog = f'Copyright {YEAR} - {AUTHOR}')

    parser.add_argument('operation', choices=['start', 'stop', 'total', 'this_week', 'avg_week'], help="The operation to be performed. 'start' will add a new log entry with the (current) start time. 'stop' will complete the last entry with the (current) end time. 'total' returns the total amount of time tracked. 'this_week' returns the amount of time tracked during the current week. 'avg_week' averages the total amount of time tracked since the first week until the current week.")
    parser.add_argument('-c', '--comment', type=str, metavar='TEXT', default='', help='A comment to be stored along the logged start/end time.')
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('-v', '--verbose', action='store_true', help='TODO')
    parser.add_argument('-f', '--log-file-path', type=str, metavar='FILENAME', default='tracker.csv', help='The path to the log file.')
    parser.add_argument('-r', '--reuse-comment', action='store_true', help='use the same comment as in the previous entry')

    args, remaining = parser.parse_known_args()

    if len(remaining) > 0:
        print(f"Unexpected program arguments found: {remaining}. They will be ignored.")

    now = datetime.datetime.now()
    readable_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.isfile(args.log_file_path):
        with open(args.log_file_path, 'w', newline='') as log_file:
            fieldnames = ['start', 'end', 'comment']
            writer = csv.DictWriter(log_file, fieldnames=fieldnames)
            writer.writeheader()
            print("Log file created.")

    df = pd.read_csv(args.log_file_path, dtype={"comment": str}, parse_dates=["start", "end"])

    if len(df) > 0:
        last_end_time_null = pd.isnull(df.loc[len(df)-1, 'end'])
        last_comment = df.loc[len(df)-1, 'comment']
    else:
        last_end_time_null = False
        last_comment = ""

    if args.operation == "start":
        if last_end_time_null:
            print("Current timer should be stopped before you can start a new timer.")
            parser.exit(-2)
        if args.reuse_comment:
            args.comment = last_comment
        new_row = pd.Series({"start": readable_time, "end": "", "comment": args.comment})
        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    elif args.operation == "stop":
        if not last_end_time_null:
            print("There is no timer that can be stopped. You should start a new timer instead.")
            parser.exit(-3)
        else:
            df.loc[len(df)-1, 'end'] = readable_time
    elif args.operation == "total":
        print(f"Total time worked on thesis: {(df['end'] - df['start']).sum()}")
    elif args.operation == "this_week":
        week_number = datetime.datetime.today().isocalendar().week
        df_this_week = df[df["start"].apply(lambda dt: dt.isocalendar().week == week_number)]
        print(f"Total time worked on thesis this week (week {week_number}): {(df_this_week['end'] - df_this_week['start']).sum()}")
    elif args.operation == "avg_week":
        first_week = df["start"].min().isocalendar().week
        last_week  = datetime.datetime.today().isocalendar().week
        weeks = last_week - first_week + 1
        print(f"Average time per week worked on thesis (from week {first_week} until week {last_week}): {(df['end'] - df['start']).sum() / weeks}")
    else:
        print(f"Unexpected operation: {args.operation}.")
        parser.exit(-4)

    if args.operation in {"start", "stop"}:
        df.to_csv(args.log_file_path, index=False)


if __name__ == "__main__":
    main()

from sys import argv
from parse import parse_log
from plot import plot_job_timeseries

def print_usage():
    print("Usage: python run.py <log_file_path>")

def check_args():
    if len(argv) != 2:
        print_usage()
        exit(1)

def main():
    check_args()
    file_path = argv[1]
    jobs = parse_log(file_path)

    # Print the results
    for job in jobs:
        print(f"Job ID: {job['rule']} ({job['jobid']})")
        print(f"Start Time: {job['start_time']}")
        print(f"End Time: {job['end_time']}")
        print(f"Duration: {job['duration']:.2f} minutes")
        print(f"Threads: {job['threads']}")
        print(f"Command: {job['command']}\n")

    print(f"Total number of jobs: {len(jobs)}")

    # 绘制时间线图
    plot_job_timeseries(jobs)

if __name__ == "__main__":
    main()

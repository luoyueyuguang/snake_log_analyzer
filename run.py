from sys import argv
from parse import parse_log
from plot import plot_job_timeseries
import argparse

def print_usage():
    print("Usage: python run.py <log_file_path>")

def parse_args():
    if len(argv) < 2:
        print_usage()
        exit(1)
    parser = argparse.ArgumentParser(description="Parse and plot snakemake log files")
    parser.add_argument("-i", "--input", type=str, help="Path to the snakemake log file")
    parser.add_argument("-o", "--output", type=str, help="Path to the output plot file")
    return parser.parse_args()

def main():
    args = parse_args()
    file_path = args.input if args.input else argv[1]
    output_path = args.output
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
    plot_job_timeseries(jobs, output_path)

if __name__ == "__main__":
    main()

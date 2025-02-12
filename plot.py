import re
from sys import argv
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def plot_job_timeseries(jobs, output_file=None):
    """

    """
    # 确定时间范围
    min_time = min(job['start_time'] for job in jobs)
    max_time = max(job['end_time'] for job in jobs)
    time_delta = max_time - min_time
    # 设置时间间隔为1分钟
    time_points = pd.date_range(start=min_time, end=max_time, freq='1min')
    time_series = pd.DataFrame(index=time_points, columns=[job['rule'] for job in jobs])

    # 转换时间戳为分钟数
    min_datetime = min_time.replace(tzinfo=None)
    max_datetime = max_time.replace(tzinfo=None)
    total_minutes = (max_datetime - min_datetime).total_seconds() // 60

    # 为每个任务生成时间范围
    job_intervals = []
    job_colors = {}
    for job in jobs:
        start = job['start_time'].replace(tzinfo=None)
        end = job['end_time'].replace(tzinfo=None)
        job_rule = job['rule']
        job_intervals.append((start, end, job_rule))
        # 生成随机颜色
        job_colors[job_rule] = np.random.rand(3,)

    # 绘制时间线图
    fig, ax = plt.subplots(figsize=(12, 8))
    y_ticks = []
    y_labels = []
    # 使用 broken_barh 来绘制每个任务的时间区间
    for i, job_info in enumerate(job_intervals):
        start = job_info[0] - min_datetime
        end = job_info[1] - min_datetime
        duration = int((end - start).total_seconds() / 60)
        ax.broken_barh([(start.total_seconds() / 60, duration)], (i - 0.4, 0.8), facecolor=job_colors[job_info[2]])
        y_ticks.append(i)
        y_labels.append(job_info[2])
        # 添加任务名称和执行时间到图中
        ax.text(start.total_seconds() / 60 + 0.5*duration, i, f"{job_info[2]} ({duration} min)", ha='center', va='center', color='black')

    # 设置纵坐标
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    # 设置横坐标时间格式
    ax.set_xlabel('Time')
    ax.set_ylabel('Job')
    ax.set_title('Job Execution Timeline')
    #myFmt = DateFormatter("%H:%M:%S")
    #ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: (min_datetime + pd.Timedelta(minutes=x)).strftime('%H:%M:%S')))
    # 设置横坐标显示整数分钟
    plt.xticks(np.arange(0, total_minutes + 1, 1))
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    if output_file:
        plt.savefig(output_file)
    plt.close()


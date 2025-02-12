import re
from sys import argv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def plot_job_timeseries(jobs, output_file=None):
    """
    
    """
    # 确定时间范围
    min_time = min(job['start_time'] for job in jobs)
    max_time = max(job['end_time'] for job in jobs)

    # 转换时间戳为相对于min_time的分钟数
    min_datetime = min_time.replace(tzinfo=None)
    job_intervals = []
    for job in jobs:
        start = job['start_time'].replace(tzinfo=None)
        end = job['end_time'].replace(tzinfo=None)
        start_min = (start - min_datetime).total_seconds() // 60  # 转换为分钟
        end_min = (end - min_datetime).total_seconds() // 60
        job_intervals.append((start_min, end_min, job['rule'], job['duration'], job['jobid']))

    # 转换时间范围为分钟数字
    total_minutes = (max_time - min_time).total_seconds() // 60

    # 绘制时间线图
    fig, ax = plt.subplots(figsize=(12, 8))
    y_ticks = []
    y_labels = []
    # 使用 broken_barh 来绘制每个任务的时间区间
    for i, job_info in enumerate(job_intervals):
        start = job_info[0]
        end = job_info[1]
        duration = job_info[3]
        jobid = job_info[4]
        job_rule = job_info[2]
        ax.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolor=np.random.rand(3,))
        y_ticks.append(i)
        y_labels.append(job_rule)

        # 添加任务名称、执行时间、开始时间和结束时间到矩形上
        center_x = end
        ax.text(center_x, i, f"{job_rule}({jobid} {duration:.1f} min {start}-{end})", ha='center', va='center', color='black')
        #ax.text(start, i - 0.5, f"Start: {start} min", ha='left', va='top', color='black', fontsize=8)
        #ax.text(end, i - 0.5, f"End: {end} min", ha='right', va='top', color='black', fontsize=8)

    # 设置纵坐标,设置文字左移
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    # 设置横坐标
    ax.set_xlabel('Time (minutes from start)')
    ax.set_xlim(0, total_minutes)
    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    if output_file:
        plt.savefig(output_file)
    plt.close()

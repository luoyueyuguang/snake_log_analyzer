import re
from collections import defaultdict
from datetime import datetime

def parse_log(input_file):
    # 读取日志文件
    with open(input_file, "r") as f:
        log_data = f.read()
    # 正则表达式用于匹配日志中的localrule信息
    localrule_pattern = re.compile(r'\[([\w\s:]+)\]\nlocalrule\s+([\S]+).*?jobid:\s*(\d+)', re.DOTALL)
    # 正则表达式用于匹配[时间]行
    time_pattern = re.compile(r"\[([\w\s:]+)\]\nFinished job (\d+)", re.DOTALL)
    
    # 用于存储解析结果
    localrules = {}
    for match in localrule_pattern.finditer(log_data):
        localrules[int(match.group(3))] = {
            "start_time": datetime.strptime(match.group(1), "%a %b %d %H:%M:%S %Y"),    
            "localrule": match.group(2)
        }
    for match in time_pattern.finditer(log_data):
        localrules[int(match.group(2))]["end_time"] = datetime.strptime(match.group(1), "%a %b %d %H:%M:%S %Y")
        localrules[int(match.group(2))]["duration"] = (localrules[int(match.group(2))]["end_time"] - localrules[int(match.group(2))]["start_time"]).seconds
    return localrules

def group_by(localrules, sort_by ='duration'):
    if sort_by == "start_time":
        return sorted(localrules.items(), key=lambda x: x[1]["start_time"])
    elif sort_by == "end_time":
        return sorted(localrules.items(), key=lambda x: x[1]["end_time"])
    elif sort_by == "duration":
        return sorted(localrules.items(), key=lambda x: x[1]["duration"])
    else:
        return None

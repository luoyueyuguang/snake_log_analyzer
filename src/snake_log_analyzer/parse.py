import re
from datetime import datetime

def parse_log(file_path):
    jobs = []
    with open(file_path, 'r') as f:
        log_content = f.read()
    
    # Regular expression to match job start and end times 
    start_pattern = re.compile(r"\[(?P<start_time>[^\]]+)\]\s+localrule\s+(?P<rule>\w+):\s+input: (?P<input>.+?)\s+output: (?P<output>.+?)\s+jobid: (?P<jobid>\d+)\s+reason: (?P<reason>.+?)\s+wildcards: (?P<wildcards>.+?)\s+threads: (?P<threads>\d+)\s+resources: (?P<resources>.+?)\s*\n\s*(?P<command>.+)")
    end_pattern = re.compile(r"\[(?P<end_time>[^\]]+)\]\s+Finished job (?P<jobid>\d+)\.")
    
    # Find all start and end times
    start_matches = start_pattern.finditer(log_content)
    end_matches = end_pattern.finditer(log_content)
    
    # Create a dictionary to store start and end times
    start_times = {}
    end_times = {}
    
    for match in start_matches:
        jobid = match.group('jobid')
        start_times[jobid] = {
            'start_time': datetime.strptime(match.group('start_time'), '%a %b %d %H:%M:%S %Y'),
            'rule': match.group('rule'),
            'command': match.group('command').strip(),
            'threads': int(match.group('threads'))
        }
    
    for match in end_matches:
        jobid = match.group('jobid')
        end_times[jobid] = datetime.strptime(match.group('end_time'), '%a %b %d %H:%M:%S %Y')
    
    # Calculate durations
    for jobid in start_times:
        if jobid in end_times:
            duration = (end_times[jobid] - start_times[jobid]['start_time']).total_seconds()
            jobs.append({
                'jobid': jobid,
                'start_time': start_times[jobid]['start_time'],
                'end_time': end_times[jobid],
                'duration': duration / 60,
                'rule': start_times[jobid]['rule'],
                'command': start_times[jobid]['command'],
                'threads': start_times[jobid]['threads']
            })
        else:
            print(f"Warning: Could not find end time for job {jobid}")
    
    return jobs

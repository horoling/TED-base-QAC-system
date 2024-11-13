import subprocess
import re
import os
import tempfile
from VF2.run_vf2 import run_vf2

def vf2(source, target,δ):
    result = run_vf2(source, target, δ)
    return result

def vf2_emb(source, target,δ):
    numbers = run_vf2(source, target,δ)
    embs = extract_matching_lines(target, numbers)

    return numbers, embs


def extract_matching_lines(file_path, numbers):
    if isinstance(numbers, int):
        numbers = [numbers]
    
    numbers = [str(num) for num in numbers]

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    matching_lines = []
    add_lines = False
    
    for line in lines:
        if line.startswith('t'):
            line_number = re.findall(r'\d+', line.strip())
            if line_number and line_number[-1] in numbers:
                add_lines = True
                matching_lines.append(line.strip())
            else:
                add_lines = False
        elif add_lines:
            matching_lines.append(line.strip())
    with open("embeddings.my", 'w', encoding='utf-8') as file:
        for line in matching_lines:
            file.write(line + '\n')    
    
    return matching_lines

def run_subprocess(source, target):
    def is_file_path(data):
        return isinstance(data, str) and os.path.isfile(data)

    def save_to_temp_file(data):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        with open(temp_file.name, 'w', encoding='utf-8') as file:
            file.write(data)
        return temp_file.name

    def process_data(data):
        if isinstance(data, list):
            return [save_to_temp_file(item) if not is_file_path(item) else item for item in data]
        else:
            return save_to_temp_file(data) if not is_file_path(data) else data

    source_files = process_data(source)
    target_files = process_data(target)

    results = []
    for src, tgt in zip(source_files, target_files):
        result = subprocess.run(['v.exe', src, tgt], capture_output=True, text=True)
        results.append(result)

    # Clean up temporary files if they were created
    for file in source_files + target_files:
        if not is_file_path(file):
            os.remove(file)

    return results

def extract_numbers_from_string(input_string):
    lines = input_string.splitlines()
    
    number = 0
    pattern = re.compile(r'.*Edges.*?(\d+)$', re.IGNORECASE)
    
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            number = (int(match.group(1)))
    
    return number

import re

# Path to the uploaded file
input_file = "lrxxoffset.lrc"
output_file = "lrc_adjusted.lrc"

def extract_offset(line):
    match = re.match(r"^\[offset:(-?\d+)\]$", line)
    return int(match.group(1))*(-1) if match else None

# offset_ms = 163500  # -163.5 seconds in milliseconds

def adjust_timestamp(timestamp, offset_ms):
    match = re.match(r"\[(\d+):(\d+\.\d+)\]", timestamp)
    if not match:
        return timestamp  # Return unchanged if not a timestamp

    minutes, seconds = int(match.group(1)), float(match.group(2))
    total_ms = (minutes * 60 + seconds) * 1000 + offset_ms

    if total_ms < 0:
        total_ms = 0  # Avoid negative timestamps

    new_minutes = int(total_ms // 60000)
    new_seconds = (total_ms % 60000) / 1000

    return f"[{new_minutes:02}:{new_seconds:05.2f}]"

def process_lrc(input_path, output_path):
    offset_ms = 0
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            offset = extract_offset(line)
            if offset is not None:
                offset_ms = offset
                continue # Skip adding the offset entry itself
            adjusted_line = re.sub(r"\[\d+:\d+\.\d+\]", lambda m: adjust_timestamp(m.group(0), offset_ms), line)
            outfile.write(adjusted_line)

# Process the LRC file
process_lrc(input_file, output_file)
print(f"Adjusted LRC file saved to {output_file}")

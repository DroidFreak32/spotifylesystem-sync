import argparse
import os
import glob
import re
import sys
import subprocess
import shutil
from concurrent.futures import ProcessPoolExecutor

FFMPEG_BIN = shutil.which("ffmpeg")

def generate_spectrogram(args_tuple):
    """
    Worker function to generate a spectrogram for a single file.
    Args:
        args_tuple (tuple): (file_path, source_dir, dest_dir)
    """
    file_path, source_dir, dest_dir = args_tuple

    try:
        # Calculate relative path to preserve structure info in filename
        rel_path = os.path.relpath(file_path, source_dir)

        # Replace special characters (anything not alphanumeric) with underscores
        # This handles directory separators (/) and other chars like spaces, dots, etc.
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', rel_path)

        output_filename = f"{safe_name}.jpg"
        output_path = os.path.join(dest_dir, output_filename)

        if os.path.exists(output_path):
            return f"[SKIP] Exists: {rel_path}"

        # Use FFmpeg to generate the spectrogram
        # showspectrumpic filter options:
        # s=1280x720: Resolution
        # mode=separate: Show channels separately (like Spek)
        # legend=1: Draw frequency/time axes
        cmd = [
            FFMPEG_BIN, '-y', '-v', 'error',
            '-i', file_path,
            '-lavfi', 'showspectrumpic=s=1280x1280:mode=combined:legend=1',
            output_path
        ]
        subprocess.run(cmd, check=True)

        return f"[OK] Processed: {rel_path}"

    except subprocess.CalledProcessError as e:
        return f"[ERROR] Failed {rel_path}: {str(e)}"
    except Exception as e:
        return f"[ERROR] Unexpected {rel_path}: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Extract spectrograms from FLAC files recursively.")
    parser.add_argument("source_dir", help="Path to the source directory containing FLAC files")
    parser.add_argument("dest_dir", help="Path to the destination directory for images")
    parser.add_argument("-j", "--jobs", type=int, default=4, help="Number of parallel jobs (default: 4)")

    args = parser.parse_args()

    if not FFMPEG_BIN:
        print("Error: 'ffmpeg' is not installed or not in PATH.")
        return

    if not os.path.isdir(args.source_dir):
        print(f"Error: Source directory '{args.source_dir}' does not exist.")
        return

    if not os.path.exists(args.dest_dir):
        try:
            os.makedirs(args.dest_dir)
        except OSError as e:
            print(f"Error creating destination directory: {e}")
            return

    print(f"Scanning '{args.source_dir}' for FLAC files...")

    # Recursive search for .flac files
    search_pattern = os.path.join(args.source_dir, "**", "*.flac")
    flac_files = glob.glob(search_pattern, recursive=True)

    if not flac_files:
        print("No FLAC files found.")
        return

    print(f"Found {len(flac_files)} files. Processing with {args.jobs} parallel jobs...")

    # Prepare arguments for the worker function
    # ProcessPoolExecutor maps a function to an iterable, so we pack args into tuples
    tasks = [(f, args.source_dir, args.dest_dir) for f in flac_files]

    # Use ProcessPoolExecutor for CPU-bound tasks (audio processing/plotting)
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        for result in executor.map(generate_spectrogram, tasks):
            print(result)

    print("Processing complete.")


if __name__ == "__main__":
    main()

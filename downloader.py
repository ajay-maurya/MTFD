"""
Multi-threaded File Downloader

This script allows you to download large files in parallel chunks using multiple threads, maximizing bandwidth utilization. 
The downloaded chunks are merged into a single file. Progress bars are displayed for each thread and overall progress.

Author: Ajaykumar Maurya
Date: March 30, 2024
"""

import os
import requests
import concurrent.futures
from tqdm import tqdm
import psutil
import argparse
from datetime import date

def download_chunk(url, save_path, start_byte, end_byte, thread_index, thread_progress_bars):
    """
    Download a chunk of the file.

    Args:
    url (str): The URL of the file to download.
    save_path (str): The path where the downloaded file will be saved.
    start_byte (int): The start byte of the chunk.
    end_byte (int): The end byte of the chunk.
    thread_index (int): The index of the thread downloading the chunk.
    thread_progress_bars (list): List of tqdm progress bars for each thread.

    Returns:
    str: The path to the downloaded chunk file.
    """
    # Make a GET request for the specified byte range
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    response = requests.get(url, headers=headers, stream=True)
    
    # Write the chunk to a temporary file
    temp_file_path = f"{save_path}.part{thread_index}"
    with open(temp_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                thread_progress_bars[thread_index].update(len(chunk))
    
    return temp_file_path

def merge_files(temp_files, save_path):
    """
    Merge temporary chunk files into the final file.

    Args:
    temp_files (list): List of paths to temporary chunk files.
    save_path (str): The path where the merged file will be saved.
    """
    # Merge temporary files into the final file
    with open(save_path, 'wb') as final_file:
        for temp_file in temp_files:
            with open(temp_file, 'rb') as f:
                final_file.write(f.read())
            os.remove(temp_file)

def download_file_in_chunks(url, save_path, num_threads):
    """
    Download a file in parallel chunks using multiple threads.

    Args:
    url (str): The URL of the file to download.
    save_path (str): The path where the downloaded file will be saved.
    num_threads (int): Number of threads to use for downloading.

    Raises:
    ValueError: If the number of threads is less than or equal to 0.
    """
    if num_threads <= 0:
        raise ValueError("Number of threads must be greater than 0")

    # Get total file size
    response = requests.head(url)
    total_size = int(response.headers['Content-Length'])

    # Calculate chunk size and ranges
    chunk_size = total_size // num_threads
    ranges = [(i * chunk_size, min((i + 1) * chunk_size - 1, total_size - 1)) for i in range(num_threads)]

    # Initialize thread progress bars
    thread_progress_bars = [tqdm(total=end_byte - start_byte + 1, unit='B', unit_scale=True, desc=f"Thread {i+1}", ncols=100) for i, (start_byte, end_byte) in enumerate(ranges)]

    # Initialize list to store temporary file paths
    temp_files = []

    # Initialize thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i, (start_byte, end_byte) in enumerate(ranges):
            future = executor.submit(download_chunk, url, save_path, start_byte, end_byte, i, thread_progress_bars)
            futures.append(future)

        # Wait for all threads to complete and collect the temporary file paths
        for future in concurrent.futures.as_completed(futures):
            temp_files.append(future.result())

        # Close thread progress bars
        for progress_bar in thread_progress_bars:
            progress_bar.close()

    # Merge temporary files into the final file
    merge_files(temp_files, save_path)

def main():
    parser = argparse.ArgumentParser(description='Download a file in chunks using multiple threads.')
    parser.add_argument('--url', type=str, help='URL of the file to download', required=True)
    parser.add_argument('--save_path', type=str, help='Path where the downloaded file will be saved', required=True)
    parser.add_argument('--num_threads', type=int, help='Number of threads to use for downloading (default: number of CPU cores)', default=psutil.cpu_count())
    args = parser.parse_args()

    # Download the file in chunks and merge them
    download_file_in_chunks(args.url, args.save_path, args.num_threads)

if __name__ == "__main__":
    main()

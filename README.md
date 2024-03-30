# Multi-threaded File Downloader

This script allows you to download large files in parallel chunks using multiple threads, maximizing bandwidth utilization. 
The downloaded chunks are merged into a single file. Progress bars are displayed for each thread and overall progress.

## Features

- Download files in parallel using multiple threads
- Download files in chunks to maximize bandwidth utilization
- Merge downloaded chunks into a single file
- Display progress bars for each thread and overall progress
- Utilize system resources efficiently

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ajay-maurya/multi-threaded-file-downloader.git
```

2. Install the required Python packages:

```bash
pip install requests tqdm psutil
```

## Usage

Run the `downloader.py` script and provide the URL of the file to download along with the desired save path:

```bash
python downloader.py --url <file_url> --save_path <save_path> [--num_threads <num_threads>]
```

Replace `<file_url>` with the URL of the file you want to download, `<save_path>` with the path where you want to save the downloaded file, and `<num_threads>` with the number of threads to use for downloading (optional, default is the number of CPU cores).

Example:

```bash
python download_file_in_chunks.py --url https://example.com/large_file.zip --save_path /path/to/save/large_file.zip --num_threads 4
```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

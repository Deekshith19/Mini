import subprocess
import threading
import os
import time

# Function to trigger main6.py
def run_main(input_file):
    subprocess.run(['python3', 'main6.py', input_file])

# Function to trigger second6.py
def run_second(input_file):
    subprocess.run(['python3', 'second6.py', input_file])

# Function to trigger dir.py for brute-forcing hidden paths
def run_dir(base_url):
    subprocess.run(['python3', 'dir.py', base_url])

# Function to wait for both crawlers and then generate the PDF report
def generate_report():
    json_file1 = 'main__crawled.json'
    json_file2 = 'second_crawled.json'
    
    # Wait until both JSON files are generated
    while not (os.path.exists(json_file1) and os.path.exists(json_file2)):
        time.sleep(1)  # Sleep for 1 second before checking again

    # Trigger PDF generation once crawling is complete
    subprocess.run(['python3', 'pdf.py'])

# Function to extract the base URL from the input file
def extract_base_url(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            # Assuming the input file contains the URL in the first non-empty line
            url = line.strip()
            if url:  # If there's a valid non-empty line
                return url
    return None

def main():
    # Accept user input for input file
    input_file = input("Enter the path of the input file: ")

    # Extract base URL from the input file
    base_url = extract_base_url(input_file)

    if not base_url:
        print("Base URL could not be found in the input file.")
        return

    # Start the crawling processes simultaneously
    thread1 = threading.Thread(target=run_main, args=(input_file,))
    thread2 = threading.Thread(target=run_second, args=(input_file,))
    
    # Start the brute-forcing process in parallel
    thread3 = threading.Thread(target=run_dir, args=(base_url,))

    # Start all threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    # Generate the PDF report after crawling and brute-forcing are done
    generate_report()

if __name__ == "__main__":
    main()


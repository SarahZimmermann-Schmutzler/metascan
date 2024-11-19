"""
METASCAN is a programm that downloads all pdf files from a website and saves their metadata in a csv-file.
"""
import argparse
import os
import requests
import csv
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from urllib.parse import urljoin


def ensure_csv_extension(file_name: str) -> str:
    """
    Ensures the file name has a `.csv` extension. If it's missing, it add it.

    Args:
        file_name (str): The name of the file.

    Returns:
        str: The file name with a `.csv` extension if it was missing.
    """
    if not file_name.lower().endswith('.csv'):
        file_name += '.csv'
    return file_name


def get_pdf_links(url: str) -> list[str]:
    """
    Extracts all PDF links from a given URL.

    Args:
        url (str): The URL of the webpage to scan.

    Returns:
        list[str]: A list of full URLs to PDF files.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            full_url = urljoin(url, href)
            pdf_links.append(full_url)
    
    print(f"Found PDF links: {pdf_links}")
    return pdf_links


def extract_pdf_version(pdf_path: str) -> str:
    """
    Extracts the PDF version from the PDF header.

    Args:
        pdf_path (str): The file path to the PDF.

    Returns:
        str: The PDF version, or 'unknown' if it cannot be determined.
    """
    try:
        with open(pdf_path, 'rb') as f:
            # the first 8 bites includes the version number, e.g.: "%PDF-1.4"
            header = f.read(8).decode('utf-8', errors='replace')
            if header.startswith('%PDF-'):
                return header[5:].strip()
            return 'unknown'
    except Exception as e:
        print(f"Error in extracting PDF version in {pdf_path}: {e}")
        return 'unknown'


def extract_pdf_metadata(pdf_path: str) -> dict[str, str] | None:
    """
    Extracts metadata from a single PDF file.

    Args:
        pdf_path (str): The file path to the PDF.

    Returns:
        dict[str, str] | None: A dictionary with PDF metadata, or None if extraction fails.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            info = reader.metadata

            metadata = {
                'Title': getattr(info, 'title', ''),
                'Author': getattr(info, 'author', ''),
                'Creator': getattr(info, 'creator', ''),
                'Created': getattr(info, 'creation_date', ''),
                'Modified': getattr(info, 'modification_date', ''),
                'Subject': getattr(info, 'subject', ''),
                'Description': getattr(info, 'description', ''),
                'Producer': getattr(info, 'producer', ''),

                # keywords are lists or strings
                'Keywords': ', '.join(info.keywords) if hasattr(info, 'keywords') and isinstance(info.keywords, list) else (getattr(info, 'keywords', '')),
                
                # retrieve version via function
                'PDF Version': extract_pdf_version(pdf_path)
            }
            return metadata
    except Exception as e:
        print(f"Error in reading metadata in {pdf_path}: {e}")
        return None


def download_pdf(url: str, download_folder: str) -> str:
    """
    Downloads the PDF files from a URL.

    Args:
        url (str): The URL of the PDF.
        download_folder (str): The folder to save the downloaded PDF.

    Returns:
        str: The file path to the downloaded PDF.
    """
    local_filename = os.path.join(download_folder, url.split('/')[-1])
    
    response = requests.get(url)
    with open(local_filename, 'wb') as file:
        file.write(response.content)
    
    return local_filename


def write_metadata_to_csv(csv_filename: str, pdf_links: list[str], download_folder: str) -> None:
    """
    Writes metadata of downloaded PDFs to a CSV file.

    Args:
        csv_filename (str): The name of the CSV file to create.
        pdf_links (list[str]): A list of URLs pointing to PDF files.
        download_folder (str): The folder where PDFs are downloaded.

    Returns:
        None
    """
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Author', 'Creator', 'Created', 'Modified', 'Subject', 'Keywords', 'Description', 'Producer', 'PDF Version', 'File Path']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        
        writer.writeheader()
        
        for pdf_link in pdf_links:
            print(f"Download PDFs: {pdf_link}")
            pdf_path = download_pdf(pdf_link, download_folder)
            
            if pdf_path:
                print(f"Extract metadata for: {pdf_path}")
                metadata = extract_pdf_metadata(pdf_path)
                
                if metadata:
                    metadata['File Path'] = pdf_path
                    writer.writerow(metadata)


def main() -> None:
    """
    Main function that serves as the entry point for the script.

    This function:
    - Parses command-line arguments to extract the target website URL and the output CSV file name.
    - Ensures the output file name has the correct `.csv` extension. 
    - Creates necessary directories so save the CSV file. Is no location given the file is saved in the current directory.
    - Scans the provided website URL for links to PDF files.
    - Downloads the found PDF files into a designated folder (`downloaded_pdfs`).
    - Extracts metadata from each downloaded PDF file, including:
        - Title, Author, Creator, Creation Date, Modification Date, Subject, Keywords, Description, Producer, and PDF Version.
    - Writes the extracted metadata to the specified CSV file, with each PDF represented as a row.

    This function orchestrates all other helper functions and handles the workflow from URL input to final CSV output.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="online PDF downloader and extractor")
    parser.add_argument('-u', '--url', required=True, help='Website that should be scanned (URL).')
    parser.add_argument('-n', '--name', required=True, help='Name and location of the output file (.csv). Is no location given the file is saved in the current directory.')
    args = parser.parse_args()

    csv_filename = ensure_csv_extension(args.name)

    # extracting the path (location) and creating it if it does not exist
    csv_folder = os.path.dirname(csv_filename)
    if csv_folder and not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # creating storage folder for downloaded pdfs
    download_folder = "downloaded_pdfs"
    os.makedirs(download_folder, exist_ok=True)

    # retrieving pdf links from website
    pdf_links = get_pdf_links(args.url)

    # writing metadata in csv file
    write_metadata_to_csv(csv_filename, pdf_links, download_folder)

if __name__ == "__main__":
    main()
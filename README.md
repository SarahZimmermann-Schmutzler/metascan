# METASCAN

A programm that downloads all PDF files from a website, saves them in a directory, reads out their metadata and publishes it in a CSV file.     

The program was created as part of my training at the Developer Academy and is used exclusively for teaching purposes.  

It was coded on **Windows 10** using **VSCode** as code editor.

## Table of Contents
1. <a href="#technologies">Technologies</a>  
2. <a href="#features">Features</a>  
3. <a href="#getting-started">Getting Started</a>  
4. <a href="#usage">Usage</a>  
5. <a href="#additional-notes">Additional Notes</a>  

## Technologies
* **Python** 3.12.2
    * **requests** 2.32.3 (module to install, <a href="https://pypi.org/project/requests/">More Information</a>)
    * **BeautifulSoup4** 4.12.3 (module to install, <a href="https://pypi.org/project/beautifulsoup4/">More Information</a>)
    * **PyPDF2** 3.0.1 (module to install, <a href="https://pypi.org/project/PyPDF2/">More Information</a>)
    * **argparse, csv, urllib.parse, os** (modules from standard library) 

## Features
The following table shows which functions **Metascan** supports:  

| Flag | Description | Required |
| ---- | ----------- | -------- |
| -u <br> --url | Website that should be scanned (URL) | yes |
| -n <br> --name | Name and location of the output file (.csv) <br> Is no location given the file is saved in the current directory | yes |
  
**Flow of the Program**
- Parses command-line arguments to extract the target website URL and the output CSV file name.
- Ensures the output file name has the correct `.csv` extension. 
- Creates necessary directories so save the CSV file. Is no location given the file is saved in the current directory.
- Scans the provided website URL for links to PDF files.
- Downloads the found PDF files into a designated folder (`downloaded_pdfs`).
- Extracts metadata from each downloaded PDF file, including:
    - Title
    - Author
    - Creator
    - Creation Date
    - Modification Date
    - Subject
    - Keywords
    - Description
    - Producer
    - PDF Version
- Writes the extracted metadata to the specified CSV file, with each PDF represented as a row

## Getting Started
0) <a href="https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo">Fork</a> the project to your namespace, if you want to make changes or open a <a href="https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests">Pull Request</a>.

1) <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">Clone</a> the project to your platform if you just want to use the program.
    - <ins>Example</ins>: Clone the repo e.g. using an SSH-Key:  
    ```bash
    git clone git@github.com:SarahZimmermann-Schmutzler/metascan.git
    ```

2) Install the dependencies. In this case it's just **requests**, **beautifulsoup4** and **PyPDF2**. You can install it across platforms with **Pip**:  
    ```bash
    pip install requests beautifulsoup4 PyPDF2
    ``` 

## Usage
- Make sure you are in the folder where you cloned **Metascan** into.  

- Help! What options does the program support!?  
    ```bash
    python metascan.py -h
    # or
    python metascan.py --help
    ```  

- To scan a website, download the pdfs and extract the metadata use the following command in your terminal:  
    ```bash
    python metascan.py -u [url] -n [path/to/nameOfOutputfile or nameOfOutputfile]
    ```  
    - <ins>Example</ins>: You want to download some coloring pictures and are interested in their metadata? Do this:  
    ```bash
    python metascan.py -u "https://www.kribbelbunt.de/artikel/news/ausmalbild-halloween/" -n metadata_halloween_pics
    ```

    - What you see in the terminal, if the download was successful:  
    ```
    Found PDF links: http://www.kribbelbunt.de/fileadmin/user_upload/ausmalbilder/ausmalbild-halloween.pdf
    Download PDFs: http://www.kribbelbunt.de/fileadmin/user_upload/ausmalbilder/ausmalbild-halloween.pdf
    Extract metadata for: downloaded_pdfs\ausmalbild-halloween.pdf
    ```
    - What you see in the current directory, if the download and extraction was successful:
        - a folder named `downloaded_pdfs` that contains the downloaded PDF files
        - a CSV file that contains the metadata from all of the downloaded PDF files

## Additional Notes
**PyPDF2** is a third-party Python library used for working with PDF files. It allows users to perform various operations on PDF files, including reading, writing, merging, and extracting text and metadata. It's a popular choice for handling PDF files in Python because it provides a relatively straightforward interface for interacting with these file types.  
  
**BeautifulSoup4** (**bs4**) is a third-party library from the Beautiful Soup package, used for parsing and navigating HTML or XML documents. It is ideal for web scraping or analyzing HTML content because it converts raw HTML/XML content into a Python object that is easy to traverse and search using tags, classes, or IDs and it supports multiple parsers (e.g., html.parser).  
  
The **requests** module is a popular third-party library for sending HTTP requests in Python. It provides an easy-to-use interface for sending HTTP/HTTPS requests and handles details like session cookies, redirects, and authentication.  
  
The **argparse** module is used to parse (read) command line arguments in Python programs. It allows to define arguments and options that can be passed to the program when starting it from the command line. These are then processed and are available in the program as variables.  
  
**Urllib.parse** is part of Python's standard library (urllib), which provides modules for working with URLs and web-related tasks. Specifically, the urllib.parse module handles parsing, building, and manipulating URL strings. It allows you to break a URL into its components (e.g., scheme, domain, path, query parameters), lets you construct a complete URL from components and provides utilities like **urljoin** to combine a base URL with a relative path.  
  
The **csv** module allows you to read and write comma-separated values ​​(CSV) files. CSV files are text files that store data in tabular form, with values ​​usually separated by commas (or other separators such as semicolons). They are often used to exchange data between different applications such as spreadsheets, databases and programs.  
  
The **os** module in Python is part of the standard library and provides functions to interact with the operating system. It allows you to perform tasks like working with files and directories, interacting with the environment, and managing processes. Key features include Functions to create, delete, and navigate files and directories, access and modify environment variables, Work with file paths and execute and manage system processes.  
  
**Pip** is the default package manager for Python. It allows you to install, manage, and uninstall third-party Python libraries and modules. It simplifies the process of adding functionality to your Python projects by letting you download and install libraries from the Python Package Index (PyPI), a repository of Python packages.  
  
**ChatGPT** was involved in the creation of the program (Debugging, Prompt Engineering etc.).  
  
I use **Google Translate** for translations from German into English.
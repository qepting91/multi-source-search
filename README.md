# multi-source-search
This project is a Python-based full-text search tool that is capable of searching through multiple document types located either on the local machine or a Google Drive folder. The tool leverages the Whoosh search engine library to efficiently index and search documents. The tool provides a GUI for ease of use and is capable of reading and extracting text from .pdf, .doc, .docx, .jpg, and .png file formats.

## Features

- Full-text search of documents.
- Supports .pdf, .doc, .docx, .jpg, and .png file formats.
- Can search documents located locally or in a Google Drive folder.
- Graphical user interface for ease of use.
- Customizable search context range.

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/qepting91/document-search-engine.git
    ```

2. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Specify the local directories and Google Drive folder to search in the `config.json` file.

2. Run the main script:
    ```
    python main.py
    ```

3. Enter your search query in the application window that appears and click "Search".

The application will display each matching document's path or link and the context around the match.

## Dependencies

- Python 3
- PyPDF2
- python-docx
- PIL
- pytesseract
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- Whoosh

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you encounter any problems or have any questions, please open an issue on this GitHub repository.

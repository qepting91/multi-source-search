# multi-source-search
Document Search Engine is a Python-based tool that indexes and searches text within documents stored either locally or in a Google Drive folder. The tool provides a GUI for ease of use and is capable of reading and extracting text from .pdf, .doc, .docx, .jpg, and .png file formats.

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

## Google Drive Setup

In order to search documents stored in Google Drive, you'll need to create a `credentials.json` file:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project, or select an existing one.
3. In the sidebar, go to APIs & Services > Library.
4. Search for "Drive API" and enable it for your project.
5. Go to APIs & Services > Credentials.
6. Click "Create Credentials", then "OAuth client ID".
7. If you haven't configured the OAuth consent screen, you'll need to do so - you can use the default settings.
8. For application type, choose "Desktop app".
9. Click "Create", then "OK".
10. In the credentials list, you should now see an entry for your client ID. Click the download icon on the right to download your `credentials.json` file.
11. Move `credentials.json` into the same directory as the `main.py` file in this repository.

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

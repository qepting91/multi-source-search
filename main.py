import os
import glob
import json
import threading
import tkinter as tk
import csv
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from PyPDF2 import PdfFileReader
from docx import Document
from PIL import Image
import pytesseract
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PdfFileReader(f)
        text = ''
        for page in range(reader.getNumPages()):
            text += reader.getPage(page).extractText()
    return text

# Function to extract text from Word document
def extract_text_from_doc(file_path):
    doc = Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])

# Function to extract text from image
def extract_text_from_image(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)

# Function to extract text from JSON
def extract_text_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return json.dumps(data)  # converts JSON data to string

# Function to extract text from CSV
def extract_text_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        return ' '.join([' '.join(row) for row in reader])  # converts each row to a string and joins all rows

# Google Drive API settings
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Function to authenticate with Google Drive
def drive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

# Function to extract text from Google Drive files
def extract_text_from_drive_file(file):
    request = drive_service().files().get_media(fileId=file['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    if file['mimeType'] == 'application/pdf':
        return extract_text_from_pdf(io.BytesIO(fh.getvalue()))
    elif file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_doc(io.BytesIO(fh.getvalue()))
    elif file['mimeType'] == 'image/jpeg' or file['mimeType'] == 'image/png':
        return extract_text_from_image(io.BytesIO(fh.getvalue()))
    elif file['mimeType'] == 'application/json':
        return extract_text_from_json(io.BytesIO(fh.getvalue()))
    elif file['mimeType'] == 'text/csv':
        return extract_text_from_csv(io.BytesIO(fh.getvalue()))

# Function to add file to index
def add_to_index(writer, path, link, text):
    writer.add_document(path=path, link=link, content=text)

# Schema for Whoosh index
schema = Schema(path=ID(stored=True), link=ID(stored=True), content=TEXT)

# Function to create index
def create_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    return create_in("indexdir", schema)

# Function to index all local files
def index_local():
    with open('config.json') as f:
        data = json.load(f)
    local_directories = data['local_directories']

    writer = ix.writer()
    for directory in local_directories:
        for file_path in glob.glob(directory + '/**', recursive=True):
            if file_path.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif file_path.endswith('.doc') or file_path.endswith('.docx'):
                text = extract_text_from_doc(file_path)
            elif file_path.endswith('.jpg') or file_path.endswith('.png'):
                text = extract_text_from_image(file_path)
            elif file_path.endswith('.json'):
                text = extract_text_from_json(file_path)
            elif file_path.endswith('.csv'):
                text = extract_text_from_csv(file_path)
            else:
                continue

            add_to_index(writer, file_path, "", text)
    writer.commit()

# Function to index all Google Drive files
def index_drive():
    writer = ix.writer()
    results = drive_service().files().list(
        pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            text = extract_text_from_drive_file(item)
            add_to_index(writer, "", "https://drive.google.com/file/d/" + item['id'], text)
    writer.commit()

# Function to search
def search(query, context_size=50):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(query)

        for hit in results:
            index = hit["content"].find(query)
            start = max(0, index - context_size)
            end = min(len(hit["content"]), index + len(query) + context_size)
            yield (hit["path"] or hit["link"], hit["content"][start:end])

# Create index
ix = create_index()

# Index all files
index_local()
index_drive()

# GUI class
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.query_entry = tk.Entry(self)
        self.query_entry.pack(side="top")
        self.query_entry.insert(0, "Enter your query")

        self.search_button = tk.Button(self)
        self.search_button["text"] = "Search"
        self.search_button["command"] = self.search
        self.search_button.pack(side="top")

        self.results_text = tk.Text(self)
        self.results_text.pack(side="bottom")

    def search(self):
        self.results_text.delete('1.0', tk.END)
        query = self.query_entry.get()
        results = search(query)
        for path, context in results:
            self.results_text.insert(tk.END, f"{path}\n{context}\n\n")

root = tk.Tk()
app = Application(master=root)
app.mainloop()


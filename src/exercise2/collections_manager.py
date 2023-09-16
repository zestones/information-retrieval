import os
import gzip
from exercise2.document_collection import DocumentCollection

class CollectionsManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.collections = []

    def index_documents_in_folder(self):
        """
        Indexes all documents in the folder.
        """
        # List all files in the folder
        file_names = os.listdir(self.folder_path)

        for file_name in file_names:
            if file_name.endswith('.gz'):
                # Construct the full path to the compressed document
                full_path = os.path.join(self.folder_path, file_name)
                # Create a DocumentCollection for each file
                collection = DocumentCollection(full_path)
                file_collection = collection.read_document()
                collection.construct_inverted_index(file_collection)
                self.collections.append(collection)
                

    def display_collections_indexes(self):
        for collection in self.collections:
            collection.display_inverted_index()

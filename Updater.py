import os
import requests
import zipfile
from PySide6.QtUiTools import QUiLoader

class Updater:
    version = ""

    def __init__(self, ver):
        version = ver
        pass

    def open_updater(self):
        loader = QUiLoader()
        updater_path = os.path.join(os.path.dirname(__file__), 'updater.ui')
        updater_dialog = loader.load(updater_path)

        updater_dialog.btnSearch.clicked.connect(lambda: self.search_for_updates(updater_dialog))

        updater_dialog.exec()

    def search_for_updates(self, updater_dialog):
        latest_version, download_url = self.get_latest_release()
        if latest_version and download_url:
            if latest_version != self.version:
                self.log(updater_dialog, f"New version available: {latest_version}. Downloading...")
                self.download_file(download_url, f"MargarinaWikiDesktop_{latest_version}.zip", updater_dialog)
            else:
                self.log(updater_dialog, "You are using the latest version.")

    def get_latest_release(self):
        url = 'https://api.github.com/repos/margarina-not-butter/MargarinaWikiDesktop/releases/latest'
        response = requests.get(url)

        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data['tag_name']
            download_url = release_data['assets'][0]['browser_download_url']
            return latest_version, download_url
        else:
            self.log(f"Error fetching release data: {response.status_code}")
            return None, None

    def download_file(self, url, destination, updater_dialog):
        response = requests.get(url)
        if response.status_code == 200:
            with open(destination, 'wb') as file:
                file.write(response.content)
            self.unzip_file(destination, os.path.dirname(destination), updater_dialog)
            self.log(updater_dialog, f"Downloaded latest version to {destination}")
        else:
            self.log(updater_dialog, f"Error downloading file: {response.status_code}")

    def unzip_file(self, zip_file_path, extract_to_folder, updater_dialog):
        os.makedirs(extract_to_folder, exist_ok=True)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_folder)
        self.log(updater_dialog, f"Extracted all files to: {extract_to_folder}")

    def log(self, updater_dialog, text):
        updater_dialog.teUpdater.append(text)

# Import necessary libraries
import os, sys
import json
import logging

# Define a class for managing a list of URLs to ignore
class URIgnores:

    # Initialize the object
    def __init__(self):
        try:
            self.file_path = os.path.join(os.path.dirname(__file__), 'uri_ignores.json')
            logging.info(self.file_path)
            self.load()
        except Exception as e:
            print(e)

    # Load the list of ignored URLs from the uri_ignores.json file
    def load(self):
        try:
            with open(self.file_path, 'r') as f:
                self.urls = json.loads(f.read())['urls']
        except FileNotFoundError:
            self.urls = {"urls":{}}
            logging.error(f"{self.file_path} does not exist.")

    # Save the list of ignored URLs back into the uri_ignores.json file
    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump({'urls': self.urls}, f)

    # Check if a given URL should be ignored
    def isIgnored(self, url):
        try:
            return url in self.urls
        except Exception as e:
            print(e)
            return False

    # Add a new URL to the list of ignored URLs
    def addUrl(self, url):
        try:
            self.urls[url] = True
        except Exception as e:
            self.urls = {}
            self.urls[url] = True
        finally:
            logging.info("save to url ignore list done")
            self.save()

    # Remove a URL from the list of ignored URLs
    def removeUrl(self, url):
        self.urls.pop(url, None)
        self.save()

# Test cases
if __name__ == "__main__":
    ignores = URIgnores()

    print("Testing initialization...\n")
    assert ignores.isIgnored('http://example.com') != True, "URL should not be ignored after initializing"

    print("Adding a new URL...\n")
    ignores.addUrl('https://www.google.com/')
    assert ignores.isIgnored('https://www.google.com/') == True

    print("Attempting to remove non-existing URL...\n")
    ignores.removeUrl('nonExistingURL')
    assert len(ignores.urls) == 1, "There should still be one URL in the ignored list."

    print("Attempting to add another URL...\n")
    ignores.addUrl('https://stackoverflow.com/')
    assert ignores.isIgnored('https://stackoverflow.com/') == True

    print("Attempting to remove existing URL...\n")
    ignores.removeUrl('https://stackoverflow.com/')
    assert len(ignores.urls) == 1, "The ignored list should now be empty."

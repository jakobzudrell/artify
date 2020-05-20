# Script to obtain artist images from the spotify api
# Written by: Jakob Zudrell
# Created on: 20.05.2020

# Imports
import os
import requests
import json
import urllib.request


# The client ID and client secret of this application
CLIENT_ID = "yourClientId"
CLIENT_SECRET = "yourClientSecret"

# Set the grant type to client credentials - means we are using the
# client id and client secret for authentication
grant_type = 'client_credentials'

# Set the grant type in the body params
body_params = {'grant_type' : grant_type}

# Url for authentication
url = "https://accounts.spotify.com/api/token"

# Log it
print("Authenticating user...")

# Post our request and read the response (which is JSON format)
response = requests.post(url, data = body_params, auth = (CLIENT_ID, CLIENT_SECRET))

# Validate our response status code
if response.status_code != 200:
    print("User authentication failed, please try again...")
    quit()

# If we got here, the user has been authenticated, so Log it
print("User authenticated successfully")

# Read the json format and extract the token value from it
jsonResponse = json.loads(response.text)
token = jsonResponse["access_token"]

# Create headers with the now known token which can be used in future requests
headers = {"Authorization": "Bearer {}".format(token)}

# Get a directory which contains artists
dir = input("Please enter a directory containing artist folders: ")

# Url for spotify api search queries
url = "https://api.spotify.com/v1/search"

# Iterate through all artist folders
for directory in os.scandir(dir):
    # Get a response
    response = requests.get(url=url + "?q=" + directory.name + "&type=artist", headers=headers)

    # Validate our response status code
    if response.status_code != 200:
        print("Bad status code received: " + response.status_code + "for artist: '" + directory.name + "'")
        continue

    # Get our response in JSON format and read the images from it
    jsonResponse = json.loads(response.text)
    artistName = jsonResponse["artists"]["items"][0]["name"]

    # Log it
    print("\nDownloading images for: '" + artistName + "'")

    # Iterate through the first [0] item in our search and then through our images
    for i, image in enumerate(jsonResponse["artists"]["items"][0]["images"]):        
        height = str(image["height"])
        width = str(image["width"])

        # New file information
        newFileName = "artist_" + width + "x" + height + ".jpg"
        newFilePath = os.path.join(directory.path, newFileName)

        # If we already have images downloaded
        if os.path.exists(newFilePath):
            print("- file '" + newFileName + "' already exists. Skipping download...")
            continue

        # Log it
        print(" - downloading size " + width + "x" + height)
        
        # Download the image
        urllib.request.urlretrieve(image["url"], os.path.join(directory.path, newFileName))

    # Log it
    print("Done downloading images for " + artistName)

# Script has finished
print("All done")
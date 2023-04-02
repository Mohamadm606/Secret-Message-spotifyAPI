import os
import sys
import spotipy
import webbrowser
import spotipy.util as util
import json
from json.decoder import JSONDecodeError

# to print json data clearly: print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# In terminal directory of folder with project
# export SPOTIPY_CLIENT_ID='CLIENT_ID'
# export SPOTIPY_CLIENT_SECRET='CLIENT_SECRET'
# export SPOTIPY_REDIRECT_URI='http://google.com/'

# Get username from terminal
if len(sys.argv) == 1 or len(sys.argv) > 2:
    print("\nplease compile with only your spotify username:")
    print("python3 spotifyxx.py YOUR_USERNAME_HERE\n")
    sys.exit(-1)

username = sys.argv[1]

# Erase cache and prompt for user permission
scope = "playlist-modify-public"
try:
   token = util.prompt_for_user_token(username, scope=scope)
except:
    os.remove(f".cache-(username)")
    token = util.prompt_for_user_token(username, scope=scope)

# create spotify object
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

# menu loop

while True:
    
    print()
    print(">>> Welcome to Secret Message " + displayName + "!")
    print(">>> You have " + str(followers) + " followers\n\n")
    print("Input 0: To enter your secret message")
    print("Input 1: To Exit\n")
    print()
    choice = input("Your choice: ")
    
    # String input
    if choice == "0":
       
        print()
        stringQ = input("What is your message?: ")
        print()
        
        # get search result for each word
        stringQ = stringQ.split()
        trackIDs = []
        trackArt = []
        iter = 1 
        for x in stringQ:
            
            # get results and split track name into list
            searchResult = spotifyObject.search(x,50,0,"track")
            amountItems = len(searchResult['tracks']['items'])
            
            if amountItems < 1:
                print("Sorry! No song with the first word being " + x + 
                      " exists, please input a new message\n")
                sys.exit(-1)

            currentTrack = searchResult['tracks']['items'][0]
            trackName = currentTrack["name"].split()
            
            # while first word of track found not equal to searched word
            z = 0
            while str(trackName[0]).lower() != str(x).lower():
                if z >= amountItems:
                    break
                currentTrack = searchResult['tracks']['items'][z]
                trackName = currentTrack["name"].split()
                z+=1
            
            if str(trackName[0]).lower() != str(x).lower():
                print("Sorry! No song with the first word being " + x + 
                      " exists, please input a new message\n")
                exit(-1)
            
            # save name and ID of each track
            trackIDs.append(currentTrack["id"])
            trackArt.append(currentTrack['album']['images'][0]['url'])
            
            # print track info
            print(str(iter) + ") " + str(currentTrack['name']))
            print("   Artist: " + str(currentTrack['artists'][0]['name']))
            print()
            iter += 1
            

        while True:
            
            songSelection = input("Enter a song number to view album art associated with it!\n" + 
                              "Enter \"x\" To add songs to a playlist on your account!\n" + 
                              "Enter \"z\" To exit\n")
    
            if songSelection == "x":
                playlistName = input("What would you like to name the playlist?:\n")
                playlist = spotifyObject.user_playlist_create(user=username,name=playlistName, public=True)
                playlistID = playlist["id"]
                spotifyObject.playlist_add_items(playlist_id=playlistID,items=trackIDs)
                print()
                print("Success!")
                print()
                break
        
            if songSelection.isnumeric():
                if int(songSelection) < 1 or int(songSelection) > len(trackIDs):
                    print("invalid song number, please try again\n")
                else:
                    songSelection = int(songSelection) - 1
                    trackurl = trackArt[songSelection]
                    webbrowser.open(trackurl)
                    continue
                    
            if songSelection == "z":
                break
                
    choice = input("\nInput 0: To create another playlist\nInput 1: To exit\n")
        
    # Break loop end program
    if choice == "1":
        break
    
    
print()
print("Bye!")
print()
# print json data clearly: print(json.dumps(VARIABLE, sort_keys=True, indent=4))

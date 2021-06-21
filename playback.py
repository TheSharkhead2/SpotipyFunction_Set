""" 
This file comprises of functions that have to do with data on currently playing music. 
"""

def basic_song_info(spObject):
    """ 
    Return basic data for currently playing song. This is intended for use with 
    programs displaying the currently playing song and associated data. 

    Parameters 
    ----------
    spObject: Spotipy API Object 
        Spotipy object with scope of: 'user-read-currently playing'

    Returns
    -------
    artist: str 
        The artist name as a string 
    songName: str 
        The name of the song as a string 
    albumName: str 
        The name of the album as a string 
    songID: str 
        The Spotify song id as a string
    isPlaying: bool
        Boolean denoting whether Spotify is currently playing or not
    """

    trackInfo = spObject.current_user_playing_track() #get track info for current track
    #future addition: error handling for errors with collecting data... ie: detect if user object needs re-authentication/if user not playing music 

    artist = trackInfo["item"]["artists"][0]["name"] #get first artist listed 
    songName = trackInfo["item"]["name"] #get song name
    albumName = trackInfo["item"]["album"]["name"] #get album name
    
    songID = trackInfo['item']['id'] #get song's track id
    isPlaying = trackInfo['item']['is_playing'] #get song's current play status

    return ((artist, songName, albumName, songID, isPlaying))

def song_image_info(spObject):
    """
    Return data around the currently playing song's album image and artist image.
    This includes information on the various images' size and url.

    Parameters
    ----------
    spObject: Spotipy API Object
        Spotipy object with the scope of: 'user-read-currently-playing'

    Returns
    -------
    albumImageData: list
        List containing dictionaries for all available images for the given album. Each dictionary has the format
        {height: height, url: url, width:width}

    artistImageData: list
        List containing dictionaries for all available images for the first listed artist. Each dictionary has the 
        format {height: height, url:url, width: width}
    """

    trackInfo = spObject.current_user_playing_track() #get track info for current track

    albumImageData = trackInfo['item']['album']['images'] #get album image list
    artistImageData = spObject.search(q="artist:" + trackInfo['item']['artists'][0]["name"], type="artist")["artists"]["items"][0]["images"] #get artist image list

def playback_time_info(spObject, format="min-sec"):
    """
    Return data about the current time in the currently playing song.

    Parameters
    ----------
    spObject: Spotipy API Object
        Spotipy object with the scope of: 'user-read-currently-playing'

    format: string
        "min-sec" or "ms" - output string format

    Returns
    -------
    currentProgress: string
        String of the current position in the song, formatted according to format.

    totalLength: string
        String of the total length of the song, formatted according to format.
    """

    trackInfo = spObject.current_user_playing_track() #get track info for current track

    #yes, I could technically do this more effeciently using a function for time conversion, but I didn't want to write all the stuff introducing a function. sue me.

    #get the current progress and total track length
    currentProgress = trackInfo["progress_ms"]
    totalLength = trackInfo["item"]["duration_ms"]

    #if requested, convert the times to minute:second format
    if format == "min-sec":
        
        #converting time for currentProgress
        currentProgress = currentProgress/1000
        minutes, seconds = round(currentProgress/60), round(currentProgress - round(currentProgress/60)*60)
        if seconds < 10 and seconds >= 1:
            seconds = "0" + str(seconds)
        elif seconds < 1:
            seconds = "00"
        currentProgress = f"{minutes}:{seconds}"

        #converting time for totalLength
        totalLength = totalLength/1000
        minutes, seconds = round(totalLength/60), round(totalLength - round(totalLength/60)*60)
        if seconds < 10 and seconds >= 1:
            seconds = "0" + str(seconds)
        elif seconds < 1:
            seconds = "00"
        totalLength = f"{minutes}:{seconds}"
    
    #return strings as formatted
    return currentProgress, totalLength

def get_song_attributes(spObject):
    """ 
    Return a list of song attributes from the Spotify API, including: 
    ["artist", "album", "track_name", "track_id", "danceability", "energy", 
    "key", "loudness", "mode", "speechiness", "instrumentalness", "liveness", 
    "valence", "tempo", "duration_ms", "time_signature"]
    More informantion on each audio feature here:
    https://developer.spotify.com/documentation/web-api/reference/#object-audiofeaturesobject

    Parameters
    ----------
    spObject: Spotipy API Object 
        Spotipy object with at least the scope of: 'user-read-currently-playing'

    Returns
    -------
    audioFeatures: dict
        Dictionary mapping all audio features to coorisponding values for said 
        features for currently playing song 

    """
    
    #define list containing all the audio features being requested
    playlist_features_list = ["artist", "album", "track_name", "track_id", 
                             "danceability", "energy", "key", "loudness", "mode", "speechiness",
                             "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"] 

    trackInfo = spObject.current_user_playing_track() #get info on current track from Spotipy

    songFeatures = {} #create empty dict for storing information

    #extract basic song data into dict
    songFeatures["artist"] = trackInfo["item"]["artists"][0]["name"]
    songFeatures["album"] = trackInfo["item"]["album"]["name"]
    songFeatures["track_name"] = trackInfo["item"]["name"]
    songFeatures["track_id"] = trackInfo["item"]["id"]
    #Get audio features into dict
    audio_features = spObject.audio_features(songFeatures["track_id"])[0] #information on these here: https://developer.spotify.com/documentation/web-api/reference/#object-audiofeaturesobject
    for feature in playlist_features_list[4:16]:
        songFeatures[feature] = audio_features[feature]         

    return songFeatures
    


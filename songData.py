"""
This file contains a class that has functions for more information on songs, artists, albums, etc. 

"""

#importing libraries 
from .authenticator import Authenticator, ReauthenticationDecorator

class SongData(Authenticator):
    """
    This class is a conglomerate of functions relating to song/artist/album/other data querries in the 
    Spotipy library (Spotify API python port). This class inherits from the Authenticator class and can 
    therefore reauthenticate the API access token when need be. Each function that needs this 
    functionality should have the decorator: @ReauthenticationDecorator.reauthorization_check. As this 
    is a child of the Authenticator class, it also requires the same input parameters when initializing 
    the class.

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):

        super().__init__(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope)

    @ReauthenticationDecorator.reauthorization_check
    def related_artists(self, artistID):
        """
        This function simply returns spotipy.artist_related_artists() with minimal formatting. Thie means
        it returns a list of similar artists to a specified artist id. 

        Parameters
        ----------

        artistID: str
            Spotify artist ID, URI, or URL

        Returns
        -------

        relatedArtists: list
            List of related artists to specified artist. Each entry is a dict containing the name and id of
            the artist.

        """

        relatedArtistsRaw = self.spotipyObject.artist_related_artists(artist_id=artistID) #get all the raw imformation from spotipy function
        relatedArtistsRaw = relatedArtistsRaw['artists'] #only take artists (returns list of artists inside dict with nothing else)

        relatedArtists = [] #new empty list to put new, formatted artists into 
        for artist in relatedArtistsRaw:
            relatedArtists.append({'name' : artist['name'], 'id' : artist['id']}) #take only name and id

        return relatedArtists
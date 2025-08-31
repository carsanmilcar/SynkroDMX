
"""Example script for authenticating and creating a Spotipy client."""

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Verify that required credentials are present
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET or not SPOTIFY_REDIRECT_URI:
    raise ValueError(
        "Missing one of the required environment variables: "
        "SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI."
    )

# Define the necessary scope
# Minimum for current track:
scope = "user-read-currently-playing"
# Optional (recommended) for player state and queue:
# scope = "user-read-currently-playing user-read-playback-state"

# Initialize the Spotipy client with OAuth
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope,
    cache_path=".cache-spotify",  # Make sure it's ignored in .gitignore
)
sp = spotipy.Spotify(auth_manager=auth_manager)


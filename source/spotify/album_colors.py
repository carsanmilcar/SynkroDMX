import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO
from colorthief import ColorThief

# ===========================
# Configuration and Setup
# ===========================

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Verify that required credentials are present
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET or not SPOTIFY_REDIRECT_URI:
    raise ValueError("Missing one of the required environment variables: "
                     "SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI.")

# Define the necessary scope
scope = "user-read-currently-playing"

# Initialize the Spotipy client with OAuth
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope,
    cache_path=".cache-spotify"  # Ensure this is in your .gitignore
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ===========================
# Function to Retrieve Album Colors
# ===========================

def get_current_album_colors():
    """
    Retrieves the dominant color and a palette of colors from the currently playing track's album cover.

    Returns:
        dict: A dictionary containing the dominant color and the color palette.
              Example:
              {
                  "dominant_color": (R, G, B),
                  "palette": [(R1, G1, B1), (R2, G2, B2), ...]
              }
    """
    # Get the currently playing track
    current_track = sp.current_user_playing_track()

    if current_track and current_track.get('item'):
        # Extract the album images
        images = current_track['item']['album']['images']
        # Typically images[0] is the largest image
        if images:
            album_cover_url = images[0]['url']
            print("Currently playing album cover URL:", album_cover_url)
            
            # ===========================
            # Download the Album Cover Image into Memory
            # ===========================
            try:
                response = requests.get(album_cover_url)
                response.raise_for_status()  # Raise an error for bad status codes
                image_data = response.content
                image_stream = BytesIO(image_data)
                print("Album cover downloaded into memory.")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading the album cover: {e}")
                return None
            
            # ===========================
            # Extract Color Palette from In-Memory Image
            # ===========================
            try:
                color_thief = ColorThief(image_stream)
                # Get the dominant color
                dominant_color = color_thief.get_color(quality=1)
                # Get a palette of 5 colors
                palette = color_thief.get_palette(color_count=5, quality=1)
                print("Dominant color (RGB):", dominant_color)
                print("Color palette (RGB):", palette)
                
                # Create a vector containing all colors
                color_vector = {
                    "dominant_color": dominant_color,
                    "palette": palette
                }
                return color_vector
            except Exception as e:
                print(f"Error extracting color palette: {e}")
                return None
        else:
            print("No album images found for the currently playing track.")
            return None
    else:
        print("No track is currently playing.")
        return None

# ===========================
# Main Execution
# ===========================

if __name__ == "__main__":
    colors = get_current_album_colors()
    if colors:
        print("\nRetrieved Album Colors:")
        print(colors)
    else:
        print("\nFailed to retrieve album colors.")

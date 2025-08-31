
from __future__ import annotations

import os
from typing import Optional
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client(
    scope: str = "user-read-currently-playing",
    cache_path: Optional[str] = ".cache-spotify",
) -> spotipy.Spotify:
    """
    Crea un cliente Spotipy leyendo credenciales de entorno.
    Requiere SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI.
    """
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        raise ValueError(
            "Faltan variables de entorno: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI."
        )

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=cache_path,
    )
    return spotipy.Spotify(auth_manager=auth_manager)

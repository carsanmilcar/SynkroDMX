# SpotifyDMX

# Spotify DMX Sync

**Spotify DMX Sync** is a system designed to synchronize DMX-controlled lights with music played on Spotify. By leveraging Spotify's API for audio analysis and DMX protocols, this project enables dynamic lighting scenes that adapt to the tempo, loudness, and sections of any song.

---

## Features

- **Spotify Integration:**
  - Fetch audio analysis data (tempo, loudness, sections, key, etc.) from Spotify.
  - Map musical features to predefined lighting patterns.

- **DMX Control:**
  - Control lighting devices using DMX commands.
  - Support for intensity, colors (RGB/CMY), movement, and strobe effects.

- **Real-Time Synchronization:**
  - Sync lighting scenes to beats, sections, and transitions in music.
  - Smooth transitions between lighting scenes.

- **Modular Design:**
  - Flexible architecture for adding new lighting devices or effects in the future.

---

## Repository Structure

```plaintext
SpotifyDMX/
├── README.md                  # Project description
├── requirements.txt           # Python dependencies
├── main.py                    # Main entry point
├── source/                    # Source code folder
│   ├── __init__.py            # Source package initializer
│   ├── spotify/               # Spotify API integration module
│   │   ├── __init__.py
│   │   └── spotify_integration.py
│   ├── dmx/                   # DMX hardware control module
│   │   ├── __init__.py
│   │   └── dmx_control.py
│   └── scenes/                # Lighting scenes management module
│       ├── __init__.py
│       └── scene_manager.py
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   ├── test_spotify.py
│   ├── test_dmx.py
│   └── test_scenes.py
├── docs/                      # Documentation
│   ├── api_reference.md       # API reference
│   └── architecture.md        # System architecture description
└── assets/                    # Static files like examples or configs
    └── example_scene.json     # Example lighting scene configuration

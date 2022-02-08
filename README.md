# spotifylesystem-sync


The aim of this project is to be able to scan my filesystem's Lossless Music directory and sync playlists from spotify into m3u files.

Main goals I want to achieve include:
- Sync few **FLAC** tracks' metadata in a DB
```
  * ALBUMARTIST - Should only have 1 artist
  * ARTIST - Can be a list of feat. Artists
  * ALBUM - Can be a list. ["Greatest Hits", "Self Titled"]
  * TITLE
  * LYRICS - Compressed to save space in the DB or NULL
  * STREAMHASH (MD5SUM of the audio stream only)
  * PATH - Can be a list if same track belongs to different albums
```

- Connect to spotify
- Scan and report if a list of tracks from a Spotify playlist is present in the DB
- Generate a playlist m3u file which matches a provided Spotify playlist.
- Identify duplicate and / or corrupted tracks
- Report any changes between the filesystem and the DB (Based on Modified timestamp)

---

### Desired workflow:

```bash
python3.10 spotifylesystem-sync.py --music-dir ~/Music --db-path ~/Music/MusicDB.db --spotify-client-id XYZ --spotify-client-secret ABC
```

Defaults will be read from a config.ini file which can be changed
```ini
[DEFAULT]
music-dir=~/Music
musicdb=~/Music/Music.db
spotify-client=327d9a614151423bfa2e11
spotify-secret=327d9a614151423bfa2e11
redirect-uri=http://127.0.0.1:9090
```

1) Open a simple menu asking for an action

```
1) Complete Sync filesystem to Local DB
2) Update modified files in DB
3) Generate spotify playlists locally
4) Dump missing playlist tracks

```
2) Complete Sync

```
- ERROR When a track has multiple AlbumArtists

Multiple Album Artists: ['Linkin Park', 'Steve Aoki'] in track.
Only storing the first one: Linkin Park
Check Linkin Park/2013 - A LIGHT THAT NEVER COMES/Linkin Park - A LIGHT THAT NEVER COMES.flac.

- Warning when track checksum matches existing item in DM

100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 5628/5628 [00:43<00:00, 128.56it/s]
Metadata fetched
Identical Track found!
Previous file: Arctic Monkeys/2006 - Whatever People Say I Am, That's What I'm Not/Arctic Monkeys - The View from the Afternoon.flac
Current file: Arctic Monkeys/2006 - Who the Fuck Are Arctic Monkeys/Arctic Monkeys - The View from the Afternoon.flac
Identical Track found!
Previous file: Arctic Monkeys/2007 - Brianstorm/Arctic Monkeys - Brianstorm.flac
Current file: Arctic Monkeys/2007 - Favourite Worst Nightmare/Arctic Monkeys - Brianstorm.flac
Identical Track found!


```

3) Update modified files in DB

```
- Get last modified time of DB
- Scan for files whose modified time is after last modified time of DB
- Ask for confirmation to save the DB

``` 
4) Generate spotify playlists locally

```
- Display Spotify playlists
- Select required playlist
- Match tracks in DB
- Generate m3u from matched files' PATH tag
- Dump unmatched tracks in a JSON file
- TODO: Handle multiple Albums
- TODO: Support for custom playlist
- TODO: Support for ALL liked tracks.
- TODO: Scan an exception_list file for known false negatives (ie. TITLE may not have (Bonus Version) etc"
- TODO: Maybe have spotify<TAG> column for common replacement tags instead of a whitelist file?

```


---

### TODO List:

- Create a common.py storing global vars & helper functions
- Separate individual actions to a separate file
- Handle Commandline options
- Use `configparser` module 
- Show a help menu
- Dependency checker (Windows may not work with CSqliteExt)
- Scan each unmatched query again using a whitelist/exceptions file
- common.py can load the whitelists/exceptions

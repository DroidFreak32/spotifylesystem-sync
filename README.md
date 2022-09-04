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
- (NEW!) Show personal playlists which have a particular track saved (Useful to replace playlists with a different version of a track)

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
- inverstigate why few spot playlist dont have AArtist
```python
{'ALBUM': '1-800-273-8255', 'TITLE': '1-800-273-8255', 'ARTIST': 'Our Last Night', 'SPOTIFY': 'https://open.spotify.com/track/1wp1aHirvZihTdrtdFuFv0'}
```

- Make it more pythonic by referring to other projects like: [spotify-dl](https://github.com/SathyaBhat/spotify-dl)


### Console example:
```
1) Complete Sync filesystem to Local DB
2) Update modified files in DB
3) Generate spotify playlists locally
4) Create a playlist of all saved spotify tracks
5) Export whitelist & blacklist
6) Import whitelist & blacklist
7) Cleanup duplicates in db
Q - Quit
Enter your choice: 3
Playlists found in your account:
ID: 1LinCArgs5903itZ6IEsp2 Name: White Rock Noise                         Total Tracks: 318            
ID: 3wxUTHoNAT60QsyXfCJRaG Name: My Shazam Tracks                         Total Tracks: 10             
ID: 03m0iBzmmSFmoEuKcQLDZz Name: Post Rock                                Total Tracks: 8              
ID: 18n6rIA0rAkk20PQdgcA6j Name: Arctic Monkeys being a cardiologist      Total Tracks: 22             
ID: 62V0MssVsUYGcmWp75D833 Name: Hot stuff                                Total Tracks: 24             
ID: 0K8Z3rRTTON1V348WDQz8Z Name: Something different                      Total Tracks: 18             
ID: 6ro7JwspABtrlTErGYO53a Name: Modern Instrumentals                     Total Tracks: 15             
ID: 1MyrUZxvtixPsblkXjDioP Name: Calm Waters                              Total Tracks: 45             
ID: 6MMOZBrYL07sfaPdVnQ38c Name: Rockless Bottom                          Total Tracks: 57             
ID: 2hEP8skwpqslLEVQ2E1H6f Name: Anguish!                                 Total Tracks: 43             
ID: 2fr0uT8blZ4YujtYCz8WdO Name: Old is gold                              Total Tracks: 48             
ID: 4Kb9y65b3bV1jwEGhADCC2 Name: Anime                                    Total Tracks: 26             
Enter the playlist ID: 18n6rIA0rAkk20PQdgcA6j
Querying DB for tracks: 11 / 22playlist.
Spotify URL:
https://open.spotify.com/track/086myS9r57YsLbJpU0TgK9
Spotify / DB Title:
Why'd You Only Call Me When You're High? / Why'd You Only Call Me When You're High? (Live)

PATH Arctic Monkeys/2020 - Live at the Royal Albert Hall/Arctic Monkeys - Why'd You Only Call Me When You're High_ (Live).flac

Are these the same?
Y/N/Q: n

Adding ["Why'd You Only Call Me When You're High?"] to blacklist

Querying DB for tracks: 22 / 22
Spotify URL:
https://open.spotify.com/track/3DQVgcqaP3iSMbaKsd57l5
Spotify / DB Title:
I Bet You Look Good On The Dancefloor / I Bet You Look Good on the Dancefloor (Live)

PATH Arctic Monkeys/2020 - Live at the Royal Albert Hall/Arctic Monkeys - I Bet You Look Good on the Dancefloor (Live).flac

Are these the same?
Y/N/Q: n

Adding ['I Bet You Look Good On The Dancefloor'] to blacklist


22/22 tracks Matched. 
Do you want to generate an m3u file for the matched songs?
Y/N: Y
Do you want to generate a new spotify playlist for the UNMATCHED songs?
Y/N: n
```

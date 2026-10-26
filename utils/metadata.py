import musicbrainzngs as brainz
import requests
from pathlib import Path
from mutagen.flac import FLAC, Picture
from mutagen.id3 import APIC, ID3, TCON, TDRC, TIT2, TPE1, ID3NoHeaderError
from mutagen.mp4 import MP4, MP4Cover
from utils.music import MusicFile

brainz.set_useragent('MaterialMusic', '0.1', 'itzakunas@gmail.com')

def get_artists(response: dict) -> list[str]: 

    artists = []
    for credit in response['artist-credit']:
        if isinstance(credit, dict):
            artists.append(credit['name'])

    return artists

def get_recordings(song: str, artist: str = '') -> list[dict]:
    responses = brainz.search_recordings(query=song, limit=10, artistname=artist)

    filtered = []
    for response in responses['recording-list']:

        item = {}
        item['track_id'] = response['id']
        item['release_id'] = response['release-list'][0]['id']
        item['title'] = response['title']
        item['artists'] = get_artists(response)
        filtered.append(item)

    return filtered

def get_recording(song: dict) -> dict:

    response = brainz.get_recording_by_id(id=song['track_id'], includes=['tags', 'releases'])
    recording: dict = response['recording']
    tag_list = recording.get('tag-list', [])


    tags = []
    for tag in tag_list:
        tags.append(tag['name'])

    dates = [rec['date'] for rec in recording.get('release-list', [])]
    release_date = min(dates)

    cover_bytes = requests.get(f'https://coverartarchive.org/release/{song['release_id']}/front-500')

    song['tags'] = tags
    print(tags)
    song['release_date'] = release_date
    song['cover_bytes'] = cover_bytes.content if cover_bytes.ok else None

    return song

def _mime(data: bytes) -> str:
    return 'image/png' if data.startswith(b'\x89PNG') else 'image/jpeg'


def write_recording(file: MusicFile) -> bool:
    path: Path = file.file_path
    cover = file.cover_bytes
    ext = path.suffix.lower()

    try:
        if ext == '.mp3':
            try:
                tags = ID3(path)
            except ID3NoHeaderError:
                tags = ID3()

            if file.title:
                tags.setall('TIT2', [TIT2(encoding=3, text=file.title)])
            if file.artist:
                tags.setall('TPE1', [TPE1(encoding=3, text=file.artist)])
            if file.genre:
                tags.setall('TCON', [TCON(encoding=3, text=file.genre)])
            if file.release_date:
                tags.setall('TDRC', [TDRC(encoding=3, text=file.release_date)])
            if cover:
                tags.setall('APIC', [APIC(encoding=3, mime=_mime(cover),
                                          type=3, desc='Cover', data=cover)])
            tags.save(path)

        elif ext == '.flac':
            audio = FLAC(path)
            if file.title:
                audio['title'] = [file.title]
            if file.artist:
                audio['artist'] = [file.artist]
            if file.genre:
                audio['genre'] = [file.genre]
            if file.release_date:
                audio['date'] = [file.release_date]
            if cover:
                pic = Picture()
                pic.type = 3
                pic.mime = _mime(cover)
                pic.data = cover
                audio.clear_pictures()
                audio.add_picture(pic)
            audio.save()

        elif ext in ('.m4a', '.mp4'):
            audio = MP4(path)
            if file.title:
                audio['\xa9nam'] = [file.title]
            if file.artist:
                audio['\xa9ART'] = [file.artist]
            if file.genre:
                audio['\xa9gen'] = [file.genre]
            if file.release_date:
                audio['\xa9day'] = [file.release_date]
            if cover:
                fmt = MP4Cover.FORMAT_PNG if _mime(cover) == 'image/png' else MP4Cover.FORMAT_JPEG
                audio['covr'] = [MP4Cover(cover, imageformat=fmt)]
            audio.save()

        else:
            return False

        return True
    except Exception as err:
        print(f'Failed to write tags for {path}: {err}')
        return False
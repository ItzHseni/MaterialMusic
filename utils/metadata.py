import musicbrainzngs as brainz
import requests

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

    response = brainz.get_recording_by_id(id=song['track_id'], includes=['tags'])
    recording: dict = response['recording']
    tag_list = recording.get('tag-list', [])


    tags = []
    for tag in tag_list:
        tags.append(tag['name'])

    cover_bytes = requests.get(f'https://coverartarchive.org/release/{song['release_id']}/front-500')

    song['tags'] = tags
    song['cover_bytes'] = cover_bytes

    return song

def write_recording(file, data: dict) -> bool:
    return
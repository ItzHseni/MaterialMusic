from platformdirs import user_cache_dir
from pathlib import Path
import hashlib

from mpris_server.adapters import DEFAULT_ADAPTER_NAME, MprisAdapter
from mpris_server.events import EventAdapter
from mpris_server.base import PlayState
from mpris_server.server import Server

from utils.music import MusicClass, MusicFile, MusicFiles
import mpv
import threading

player: mpv.MPV = mpv.MPV(video=False, input_default_bindings=False)

ART_DIR = Path(user_cache_dir(appname='MaterialMusic')) / 'art'
ART_DIR.mkdir(parents=True, exist_ok=True)

def art_url(file: MusicFile):

    if not file.cover_bytes:
        return None
    
    name = hashlib.md5(str(file.file_path).encode()).hexdigest()
    ext = ".png" if file.cover_bytes.startswith(b"\x89PNG") else ".jpg"

    path = ART_DIR / (name + ext)
    if not path.exists():
        path.write_bytes(file.cover_bytes)

    return path.as_uri()

class Adapter(MprisAdapter):

    def __init__(self, files: MusicClass, name = DEFAULT_ADAPTER_NAME):
        super().__init__(name)

        self.files = files.files

        for file in files.files:
            player.playlist_append(str(file.file_path))

        player.playlist_pos = 0

    def get_playstate(self):
        if player.idle_active:
            return PlayState.STOPPED
        
        return PlayState.PAUSED if player.pause else PlayState.PLAYING
    
    def play(self):
        player.pause = False

    def pause(self):
        player.pause = True

    def resume(self):
        player.pause = False

    def next(self):
        player.command("playlist-next")

    def previous(self):
        player.command("playlist-prev")

    def get_current_position(self):
        return int((player.time_pos or 0) * 1_000_000)


    def can_control(self): return True
    def can_play(self): return True
    def can_pause(self): return True
    def can_go_next(self): return True
    def can_go_previous(self): return True
    
    def metadata(self):

        position = player.playlist_pos

        if position is None or position < 0 or position >= len(self.files):
            return {"mpris:trackid": "/org/mpris/MediaPlayer2/TrackList/NoTrack"}

        file: MusicFile = self.files[position]

        md = {
            "mpris:trackid": f"/track/{position}",
            "mpris:length": int((file.duration or 0) * 1_000_000),
            "xesam:title": file.title or file.file_path.stem,
            "xesam:artist": [file.artist or "Unknown Artist"],
            "xesam:url": file.file_path.resolve().as_uri(),
        }
        if file.genre:
            md["xesam:genre"] = [file.genre]
        if file.release_date:
            md["xesam:contentCreated"] = str(file.release_date)
        url = art_url(file)
        if url:
            md["mpris:artUrl"] = url
        return md

server = Server('MaterialMusic', adapter=Adapter(files=MusicFiles, name='MaterialMusic'))
events = EventAdapter(root=server.root, player=server.player)

def _on_pause(name, value):
    if events:
        events.on_playpause()


def _on_track(name, value):
    if events:
        events.on_title()


def start(files: MusicClass):
    global server, events
    player.pause = True

    adapter = Adapter(files=files, name='MaterialMusic')
    server = Server('MaterialMusic', adapter=adapter)
    events = EventAdapter(root=server.root, player=server.player)

    player.observe_property("pause", _on_pause)
    player.observe_property("playlist-pos", _on_track)

    threading.Thread(target=server.loop, daemon=True).start()


def toggle():
    player.pause = not player.pause


def play_index(index: int):
    player.playlist_pos = index
    player.pause = False
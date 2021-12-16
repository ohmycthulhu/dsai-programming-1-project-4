import simpleaudio as sa
import copy


class Audio:
    def __init__(self, path):
        self._audio = sa.WaveObject.from_wave_file(path)
        self._bytes_sample = self._audio.bytes_per_sample * self._audio.num_channels
        self._bytes_per_sec = self._audio.sample_rate * self._bytes_sample
        self._audio_track = copy.deepcopy(self._audio.audio_data)
        self._duration = len(self._audio_track) / self._bytes_per_sec
        self._playing = None

    def play(self, seconds=0):
        if self._playing is not None:
            self.stop()
        self._move_audio(seconds)
        self._playing = self._audio.play()

    def stop(self):
        if self._playing is not None:
            self._playing.stop()
            self._playing = None

    def _move_audio(self, seconds):
        ind = int(seconds * self._bytes_per_sec)
        ind_offset = ind - ind % self._bytes_sample
        self._audio.audio_data = self._audio_track[ind_offset:]

    @property
    def duration(self):
        return self._duration

    @property
    def track(self):
        return self._audio_track

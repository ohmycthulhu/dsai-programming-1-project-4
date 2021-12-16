import tkinter
import json
from audio import Audio
from equalizer import Equalizer
from control_buttons import AudioControlButtons, CommentControls


window = tkinter.Tk()

with open('config.json') as file:
    config = json.load(file)

filename, comments = config['sound'], config['comments']

comments = sorted(comments, key=lambda x: x['start'], reverse=True)

audio = Audio(filename)


def update_comments(_comments):
    global comments
    comments = _comments
    with open('config.json', 'w') as f:
        json.dump({**config, 'comments': comments}, f)


def get_comment(curr_duration):
    for s in comments:
        if s['start'] <= curr_duration:
            return s['text']
    return ''


def save_comment(comment, start):
    new_comment = {'text': comment, 'start': start}
    update_comments([*comments, new_comment])


window.title(config['name'])
is_paused = False


def play():
    global is_playing, is_paused
    is_playing, is_paused = True, False
    audio.play(duration)


def pause():
    global is_playing, is_paused
    is_playing, is_paused = False, True
    audio.stop()


def add_comment(comment):
    save_comment(comment, duration)


def clear_all_comments():
    update_comments([])


equalizer = Equalizer(window, 300, 100, audio.track, audio.duration)
equalizer.grid(row=1, column=1, columnspan=2)

str_subtitle = tkinter.StringVar()
txt_subtitle = tkinter.Label(window, textvariable=str_subtitle)
txt_subtitle.grid(row=2, column=1, columnspan=2)


comment_controls = CommentControls(window, 3)
comment_controls.on('new_comment', add_comment)
comment_controls.on('open', lambda: is_playing and pause())
comment_controls.on('close', lambda: is_paused and play())


audio_controls = AudioControlButtons(window, 5)
audio_controls.on('play', play)
audio_controls.on('pause', pause)


tkinter.Button(window, text='Delete comments', command=clear_all_comments).grid(row=5, column=1, columnspan=2)


duration, step = 0, 100
is_playing = False


def main():
    global duration, is_playing
    comment = get_comment(duration)
    if comment is not None:
        str_subtitle.set(comment)

    equalizer.duration = duration

    if is_playing:
        duration += step / 1000

        if duration > audio.duration:
            is_playing = False
            duration = 0
    window.after(step, main)


main()
window.mainloop()

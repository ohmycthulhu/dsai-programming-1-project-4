import tkinter
import json
from audio import Audio
from equalizer import Equalizer
from control_buttons import AudioControlButtons, CommentControls

# Create window
window = tkinter.Tk()

# Read and interpret the configuration
with open('config.json') as file:
    config = json.load(file)

filename, comments = config['sound'], config['comments']
comments = sorted(comments, key=lambda x: x['start'], reverse=True)

# Set title
window.title(config['name'])

# Declare global scalars
is_playing, is_paused = False, False
duration, step = 0, 100

# Initialize Audio class instance
audio = Audio(filename)


# Functions for interacting with comments
# Synchronizes global comments and configuration file
def update_comments(_comments):
    global comments
    comments = sorted(_comments, key=lambda x: x['start'], reverse=True)
    with open('config.json', 'w') as f:
        json.dump({**config, 'comments': comments}, f)


# Gets the first comment within given time
def get_comment(t):
    for s in comments:
        if s['start'] <= t:
            return s['text']
    return ''


# Saves the comment with given time
def save_comment(comment, start):
    new_comment = {'text': comment, 'start': start}
    update_comments([*comments, new_comment])


def add_comment(comment):
    save_comment(comment, duration)


def clear_all_comments():
    update_comments([])


# Audio controls
def play():
    global is_playing, is_paused
    is_playing, is_paused = True, False
    audio.play(duration)


def pause():
    global is_playing, is_paused
    is_playing, is_paused = False, True
    audio.stop()


# Widgets initialization
# Equalizer for displaying the sound track
equalizer = Equalizer(window, 300, 100, audio.track, audio.duration)
equalizer.grid(row=1, column=1, columnspan=2)

# Subtitles for showing the comment by time
str_subtitle = tkinter.StringVar()
txt_subtitle = tkinter.Label(window, textvariable=str_subtitle)
txt_subtitle.grid(row=2, column=1, columnspan=2)


# Comments' controls for showing input and adding new comments
comment_controls = CommentControls(window, 3)
comment_controls.on('new_comment', add_comment)
comment_controls.on('open', lambda: is_playing and pause())
comment_controls.on('close', lambda: is_paused and play())


# Audio controls for controlling the playback
audio_controls = AudioControlButtons(window, 5)
audio_controls.on('play', play)
audio_controls.on('pause', pause)


# Big button for clearing all comments
tkinter.Button(window, text='Delete comments', command=clear_all_comments).grid(row=5, column=1, columnspan=2)


# Mainloop
def main():
    global duration, is_playing

    # Synchronize comment with given time
    comment = get_comment(duration)
    if comment is not None:
        str_subtitle.set(comment)

    # Update equalizer widget
    equalizer.duration = duration

    # Increase duration if audio is playing
    if is_playing:
        duration += step / 1000

        if duration > audio.duration:
            is_playing = False
            duration = 0

    # Plan next main run
    window.after(step, main)


main()
window.mainloop()

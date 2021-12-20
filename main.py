import tkinter
import json
import os
from audio import Audio
from equalizer import Equalizer
from control_buttons import AudioControlButtons, CommentControls

CONFIG_FILE = 'config.json'
COMMENTS_FILE = 'comments.json'

# Create window
window = tkinter.Tk()

# Read and interpret the configuration
with open(CONFIG_FILE) as file:
    config = json.load(file)

filename = config['sound']


if os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE) as f:
        comments = json.load(f)
else:
    comments = []
comments = sorted(comments, key=lambda x: x['start'], reverse=True)

# Set title
window.title(config['name'])

# Declare global scalars
is_playing, is_paused = False, False
current_time, step = 0, 100

# Initialize Audio class instance
audio = Audio(filename)


# Functions for interacting with comments
# Synchronizes global comments and configuration file
def update_comments(_comments):
    global comments
    comments = sorted(_comments, key=lambda x: x['start'], reverse=True)
    with open(COMMENTS_FILE, 'w') as f:
        json.dump({'comments': comments}, f)


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
    save_comment(comment, current_time)


def clear_all_comments():
    update_comments([])


# Audio controls
def play():
    global is_playing, is_paused
    is_playing, is_paused = True, False
    audio.play(current_time)


def pause():
    global is_playing, is_paused
    is_playing, is_paused = False, True
    audio.stop()


def format_time(t):
    minutes = int(t // 60)
    seconds = int(t) % 60
    return f"{minutes}:{seconds if seconds >= 10 else '0' + str(seconds)}"


# Widgets initialization
# Equalizer for displaying the sound track
equalizer = Equalizer(window, 600, 100, audio.track, audio.duration)
equalizer.grid(row=1, column=1, columnspan=2)

# Information about duration
str_time = tkinter.StringVar()
txt_time = tkinter.Label(window, textvariable=str_time)
txt_time.grid(row=2, column=2)

# Subtitles for showing the comment by time
str_subtitle = tkinter.StringVar()
txt_subtitle = tkinter.Label(window, textvariable=str_subtitle)
txt_subtitle.grid(row=3, column=1, columnspan=2)


# Comments' controls for showing input and adding new comments
comment_controls = CommentControls(window, 4)
comment_controls.on('new_comment', add_comment)
comment_controls.on('open', lambda: is_playing and pause())
comment_controls.on('close', lambda: is_paused and play())


# Audio controls for controlling the playback
audio_controls = AudioControlButtons(window, 6)
audio_controls.on('play', play)
audio_controls.on('pause', pause)


# Big button for clearing all comments
tkinter.Button(window, text='Delete comments', command=clear_all_comments).grid(row=7, column=1, columnspan=2)


# Mainloop
def main():
    global current_time, is_playing

    # Synchronize comment with given time
    comment = get_comment(current_time)
    if comment is not None:
        str_subtitle.set(comment)

    # Update equalizer widget
    equalizer.time = current_time

    # Set time
    str_time.set(f"{format_time(current_time)} / {format_time(audio.duration)}")

    # Increase current_time if audio is playing
    if is_playing:
        current_time += step / 1000

        if current_time > audio.duration:
            is_playing = False
            current_time = 0

    # Plan next main run
    window.after(step, main)


main()
window.mainloop()

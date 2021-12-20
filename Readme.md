# Comments on audio file
This is the code for the Project 4 of Programming 1.

## Table of contents

- [How to run](#how-to-run)
- [The structure of the project](#the-structure-of-the-project)

## How to run
The project contains virtual Python environment with all needed packages.
To run the project, you can use:
```venv/bin/python3 main.py```

## The structure of the project
The program contains of the 3 custom widgets and 1 custom class.
The widgets are used to simplify UI control and enhance user experience.
The list of the widgets are below:
- `AudioControlButtons` - encapsulates the buttons for controlling the audio.
It doesn't control the certain audio, but rather emits the events.
- `CommentControls` - encapsulates the buttons for controlling the comment section,
which allows adding new comments.
- `Equalizer` - provides user interface and _fancy_ equalizer
for the visualizing the audio playback. It initialized by audio data
and controlled by setting the time of playback.

The only other class encapsulates usage of the audio files.
`Audio` class encapsulates `simpleaudio` usage.


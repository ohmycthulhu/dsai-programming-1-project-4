import tkinter as tk
import numpy as np


# Widget for displaying the audio equalizer
class Equalizer:
    ACTIVE_COLOR = 'red'
    INACTIVE_COLOR = 'blue'
    STRIPE_WIDTH = 2
    STRIPE_SEP = 4

    def __init__(self, window, width, height, audio, duration):
        self._canvas = tk.Canvas(window, width=width, height=height)
        self._stripes = self._generate_stripes(self._canvas, audio, width, height, duration)
        self._duration = duration
        self._time = 0

    def grid(self, **kwargs):
        self._canvas.grid(**kwargs)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._update_color()

    def _update_color(self):
        for stripe in self._stripes:
            stripe.color = self.ACTIVE_COLOR if stripe.timecode <= self._time else self.INACTIVE_COLOR

    @staticmethod
    def _generate_stripes(canvas, audio, width, height, duration):
        values = np.array([x for x in audio])
        padding = width // 20
        y_pos = height / 2
        max_height = height * 9 // 10
        min_height = height * 2 // 10
        max_value = np.max(values)
        results = []
        stripes_count = (width - 2 * padding) // (Equalizer.STRIPE_WIDTH + Equalizer.STRIPE_SEP)
        time_step = duration / stripes_count

        for i in range(stripes_count):
            ind = int(len(values) * (i / stripes_count))
            curr_height = max(values[ind] * max_height / max_value, min_height)
            results.append(
                Stripe(
                    canvas=canvas,
                    x=(padding + i * (Equalizer.STRIPE_WIDTH + Equalizer.STRIPE_SEP) + Equalizer.STRIPE_WIDTH / 2),
                    y=y_pos,
                    width=Equalizer.STRIPE_WIDTH,
                    height=curr_height,
                    color=Equalizer.INACTIVE_COLOR,
                    timecode=i*time_step
                )
            )

        return results


class Stripe:
    def __init__(self, canvas, x, y, height, width, color, timecode):
        self._canvas = canvas
        self._color = color
        self._timecode = timecode
        self._figure = canvas.create_rectangle(x - width / 2, y - height / 2, x + width / 2, y + height / 2, fill=color, border=None)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._update_color()

    @property
    def timecode(self):
        return self._timecode

    def _update_color(self):
        self._canvas.itemconfig(self._figure, fill=self._color)

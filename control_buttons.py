import tkinter as tk
from event_raiser import EventRaiser


class AudioControlButtons(EventRaiser):
    def __init__(self, window, row):
        super().__init__()

        self._row = row
        self._play = tk.Button(window, text='Play', command=self._play_handler)
        self._pause = tk.Button(window, text='Pause', command=self._pause_handler)

        self.show()

    def show(self):
        self._play.grid(row=self._row, column=1)
        self._pause.grid(row=self._row, column=2)

    def hide(self):
        self._play.grid_forget()
        self._pause.grid_forget()

    def _play_handler(self):
        self._emit('play')

    def _pause_handler(self):
        self._emit('pause')


class CommentControls(EventRaiser):
    def __init__(self, window, row):
        super().__init__()
        self._row = row
        self._btn_add = tk.Button(window, text='Create', command=self._add_handler)
        self._btn_clear = tk.Button(window, text='Cancel', command=self._clear_handler)
        self._btn_display = tk.Button(window, text='Add comment', command=self._display_handler)
        self._input = tk.Text(window, width=40, height=1)
        self.hide()

    def show(self):
        self._input.grid(row=self._row, column=1, columnspan=2)
        self._btn_add.grid(row=self._row+1, column=1)
        self._btn_clear.grid(row=self._row+1, column=2)
        self._btn_display.grid_forget()
        self._emit('open')

    def hide(self):
        self._input.grid_forget()
        self._btn_add.grid_forget()
        self._btn_clear.grid_forget()
        self._btn_display.grid(row=self._row, column=2)
        self._emit('close')

    def _create_comment(self, comment):
        self._emit('new_comment', comment)
        self.hide()

    def _clear(self):
        self._input.delete('1.0', tk.END)

    def _add_handler(self):
        inp = self._input.get('1.0', tk.END).strip()
        if inp:
            self._create_comment(inp)
            self._clear()

    def _clear_handler(self):
        self._clear()

    def _display_handler(self):
        self.show()


# Class for working with event listeners and emitters
class EventRaiser:
    def __init__(self):
        self._listeners = {}

    def on(self, event_name, handler):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    def off(self, event_name):
        if event_name in self._listeners:
            self._listeners[event_name] = []

    def _emit(self, event_name, *payload):
        if event_name not in self._listeners:
            return

        for handler in self._listeners[event_name]:
            handler(*payload)

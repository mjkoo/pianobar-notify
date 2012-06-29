#pianobar-notify

A simple script to create dbus notification bubbles with album art and song information from [pianobar](https://github.com/PromyLOPh/pianobar/).

Forked from the jreese's [similar script](https://github.com/jreese/pianobar-python), although the behavior of this script now differs significantly. It supports album art, caches album art on disk, and now uses dbus notifications rather than the old style pynotify notifications. Backwards compatibility is not maintained with the old style notifications, although this is a possibility for a later improvement.

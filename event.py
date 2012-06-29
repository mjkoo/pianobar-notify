#! /usr/bin/python

# Copyright (C) 2012 Maxwell J. Koo <mjkoo90@gmail.com>
#
# Based on code originally by John Reese, LeetCode.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import dbus
import hashlib
import sys
import urllib2

from os import path

class Event:
    """
    Basic pianobar event handler to interpret event_command output to actions
    useful to the rest of the python wrapper, including notification messages.
    """

    def __init__(self):
        """
        Initialize the pianobar event handler and dbus notify
        """

        obj_path = "/org/freedesktop/Notifications"
        bus_name = iface_name = "org.freedesktop.Notifications"
        bus = dbus.SessionBus()
        obj = bus.get_object(bus_name, obj_path)

        self.iface = dbus.Interface(obj, iface_name)
        self.timeout = 5000

    def execute(self, type, params={}):
        """
        Read event parameters from stdin and handle events appropriately.
        """

        # Error from pianobar, disregard
        if params["pRet"] != "1":
            return

        # Handle specific events
        if type == "songstart":
            title = params["title"]
            artist_album = "by %s on %s" % (params["artist"], params["album"])
            filename = "~/.config/pianobar/covers/%s.jpg" % hashlib.sha1(params["coverArt"]).hexdigest()
            cover = self.fetch_cover(params["coverArt"], filename)
    
            self.iface.Notify("", 0, cover, title, artist_album, [], [], self.timeout)

    def fetch_cover(self, url, filename="~/.config/pianobar/album.jpg"):
        """
        Fetches album art from the URL specified by pianobar, and saves to disk.
        """

        filename = path.abspath(path.expanduser(filename))
        
        if not path.exists(filename):
            with open(filename, "wb") as f:
                f.write(urllib2.urlopen(url).read())

        return "file://%s" % filename


if __name__ == "__main__":
    # Read event type from command arguments
    if len(sys.argv) < 2:
        print "error reading event type from command arguments"

    type = sys.argv[1]

    # Read parameters from input
    params = {}
    for s in sys.stdin.readlines():
        param, value = s.split("=", 1)
        params[param.strip()] = value.strip()

    # Call the event handler
    Event().execute(type, params)


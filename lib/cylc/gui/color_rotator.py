#!/usr/bin/env python2

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2018 NIWA & British Crown (Met Office) & Contributors.
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
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class ColorRotator(object):

    COLORS = ('#fcc', '#cfc', '#bbf', '#ffb')

    def __init__(self, colors=COLORS):
        self.colors = colors
        self.current_color = 0

    def get_color(self):
        index = self.current_color
        if index == len(self.colors) - 1:
            index = 0
        else:
            index += 1
        self.current_color = index
        return self.colors[index]

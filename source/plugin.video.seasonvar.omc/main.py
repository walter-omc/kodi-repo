#!/usr/bin/python
# coding: utf-8

#
# 
#
# Distributed under terms of the MIT license.
#
import os
import sys
import xbmcaddon

a = xbmcaddon.Addon()
p = a.getAddonInfo('path')
sys.path.insert(1, os.path.join(p, 'resources', 'site-packages'))


if __name__ == '__main__':
    import plugin_video.screen as screen
    from kodi import Plugin

    screen.render(Plugin(*sys.argv))

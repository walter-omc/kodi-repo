# -*- coding: utf-8 -*-

import os
import sys
import xbmcaddon

a = xbmcaddon.Addon()
p = a.getAddonInfo('path')
sys.path.insert(1, os.path.join(p, 'core'))


if __name__ == '__main__':
    import view.screen as screen
    from kodi import Plugin

    screen.render(Plugin(*sys.argv))


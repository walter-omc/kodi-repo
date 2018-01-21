# -*- coding: utf-8 -*-

import os, re, sys, json, urllib, hashlib, traceback
from defines import *
import time
import pprint
import pickle


class DevelDebugTools():

    def log(self, obj, filename='dev_log'):
        dname = "/home/osmc/.kodi/addons/plugin.video.filmix.net.dev/debug"
        fname = dname + '/' + filename
        fh = open(fname, 'a')
        # pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
        pprint(obj, stream=fh)
        
        fh.close()


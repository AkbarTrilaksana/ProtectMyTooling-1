#!/usr/bin/python3

# To be used as a default proxy logging facility.

import time
import sys, os

class Logger:
    options = {
        'debug': False,
        'colors': False,
        'verbose': False,
        'log': sys.stdout,
    }

    colors_map = {
        'red':      31, 
        'green':    32, 
        'yellow':   33,
        'blue':     34, 
        'magenta':  35, 
        'cyan':     36,
        'white':    37, 
        'grey':     38,
    }

    colors_dict = {
        'error': colors_map['red'],
        'fatal': colors_map['red'],
        'info': colors_map['white'],
        'good': colors_map['green'],
        'debug': colors_map['magenta'],
        'other': colors_map['grey'],
    }

    def __init__(self):
        pass

    def __init__(self, options = None):
        if options != None:
            self.options.update(options)

    @staticmethod
    def with_color(c, s):
        if not c:
            return s
        return "\x1b[%dm%s\x1b[0m" % (c, s)

    @staticmethod
    def colorize(txt, col):
        if not Logger.options['colors']:
            return txt
            
        return Logger.with_color(Logger.colors_map[col], txt)

    # Invocation:
    #   def out(txt, mode='info ', fd=None, color=None, noprefix=False, newline=True):
    @staticmethod
    def out(txt, fd, mode='info ', **kwargs):
        if txt == None or fd == 'none':
            return 
        elif fd == None:
            raise Exception('[ERROR] Logging descriptor has not been specified!')

        args = {
            'color': None, 
            'noprefix': False, 
            'newline': True,
        }
        args.update(kwargs)

        if args['color']:
            col = args['color']
            if type(col) == str and col in Logger.colors_map.keys():
                col = Logger.colors_map[col]

        else:
            col = Logger.colors_dict.setdefault(mode, Logger.colors_map['grey'])

        if not args['color']:
            col = ''

        if not Logger.options['colors']:
            col = ''

        if args['noprefix']:
            mode = ''
        
        nl = ''
        if 'newline' in args:
            if args['newline']:
                nl = '\n'

        if type(fd) == str:
            with open(fd, 'a') as f:
                f.write(mode + txt + nl)
                f.flush()

            sys.stdout.write(Logger.with_color(col, mode + txt) + nl)
            sys.stdout.flush()

        else:
            fd.write(Logger.with_color(col, mode + txt) + nl)

    # Info shall be used as an ordinary logging facility, for every desired output.
    def info(self, txt, forced = False, **kwargs):
        if (self.options['verbose'] or \
            self.options['debug'] or (type(self.options['log']) == str and self.options['log'] != 'none')):
            Logger.out(txt, self.options['log'], '[.] ', **kwargs)
        elif forced:
            Logger.out(txt, self.options['log'], '[.] ', **kwargs)

    def dbg(self, txt, **kwargs):
        if self.options['debug']:
            Logger.out(txt, self.options['log'], '[dbg] ', **kwargs)

    def err(self, txt, **kwargs):
        Logger.out(txt, self.options['log'], '[-] ', color='magenta', **kwargs)

    def ok(self, txt, **kwargs):
        Logger.out(txt, self.options['log'], '[+] ', color='green', **kwargs)

    def fatal(self, txt, **kwargs):
        Logger.out(txt, self.options['log'], '[!] ', color='red', **kwargs)
        os._exit(1)

#!/usr/bin/env python
##
##
##
##
##

import sys, time, os, os.path, subprocess, signal
from vnc2flv.video import str2clip
from flvrec import flvrec


def h264rec(output_stream, host='localhost', port=5900,
           framerate=15, keyframe=120,
           preferred_encoding=(0,), pwdfile=None,
           blocksize=32, clipping=None,
           cmdline=None,
           debug=0, verbose=1):

    ## okay. so we basically need to create a bufferedrandom, pass that into the
    ## flvrec function
    ##
    ## on a separate thread, pass the stream as stdin to ffmpeg with the settings we want.
    ##
    ## On SIGTERM, wait for ffmpeg to quit, then quit

    #pure test
    #stream = open('testfile.flv', 'wb')
    stream = output_stream
    return flvrec(stream, host, port,
           framerate, keyframe,
           preferred_encoding, pwdfile,
           blocksize, clipping,
           cmdline, debug, verbose)







def main(argv):
    import getopt, vnc2flv
    def usage():
        print argv[0], vnc2flv.__version__
        print ('usage %s [-d] [-q] [-o filename] [-r framerate] [-K keyframe]'
               ' [-e vnc_encoding] [-P vnc_pwdfile] -[N]'
               ' [-B blocksize] [-C clipping] [-S subprocess]'
               ' [host[:display] port]]' % argv[0])
        return 100

    try:
        (opts, args) = getopt.getopt(argv[1:], 'dqo:r:K:t:e:P:NB:C:S:')
    except getopt.GetoptError:
        return usage()

    debug = 0
    verbose = 1
    #filename = 'h264%s.mp4' % time.strftime('%Y%m%d%H%M')
    filename = 'test.flv'
    framerate = 15
    keyframe = 120
    preferred_encoding = (0,)
    pwdfile = None
    cursor = True
    blocksize = 32
    clipping = None
    cmdline = None
    (host, port) = ('localhost', 5900)
    for (k ,v) in opts:
        if k == '-d': debug += 1
        elif k == '-q': verbose -= 1
        elif k == '-o': filename = v
        elif k == '-r': framerate = int(v)
        elif k == '-K': keyframe = int(v)
        elif k == '-e': preferred_encoding = tuple( int(i) for i in v.split(',') )
        elif k == '-P': pwdfile = v
        elif k == '-N': cursor = False
        elif k == '-B': blocksize = int(v)
        elif k == '-C': clipping = str2clip(v)
        elif k == '-S': cmdline = v
    if not cursor:
        preferred_encoding += (-232, -239,)
    if 1 <= len(args):
        if ':' in args[0]:
            i = args[0].index(':')
            host = args[0][i] or 'localhost'
            port = int(args[0][i+1:]) + 5900
        else:
            host = args[0]

    if 2 <= len(args) :
        port = int(args[1])

    fp = open(filename, 'wb')
    return h264rec(fp, host, port, framerate=framerate, keyframe=keyframe,
                  preferred_encoding=preferred_encoding, pwdfile=pwdfile,
                  blocksize=blocksize, clipping=clipping, cmdline=cmdline,
                  debug=debug, verbose=verbose)


if __name__ == '__main__':
    sys.exit(main(sys.argv))


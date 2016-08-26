import argparse
import logging
import os
import threading
import socket

import colorlog
import requests
from plexapi.server import PlexServer

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
  '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger('[PlexTrafficDriver]')
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--skip-push', action='store_true',
                      help="Don't run any real commands")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  parser.add_argument("--stop-all", help="stop all travis builds",
                      action="store_true", default=False)
  parser.add_argument("--baseurl", help="baseurl", type=str, required=True)
  parser.add_argument("--token", help="token", type=str, required=True)
  parser.add_argument("--concurrency", type=int, required=True)

  return parser.parse_args()


def play_movie(url, i):
  logger.info('thread {} started: {}'.format(i, url))
  while True:
    total = 0
    mb = 1024*1024 
    last = 0
    try:
      r = requests.get(url, stream=True, timeout=2)
      for line in r.iter_lines(chunk_size=1024):
        total += len(line)
        if int(total/mb) > last:
          print("{}: {} mb".format(i, total/mb))
          last = int(total/mb)
    except socket.timeout as e:
      pass

if __name__ == '__main__':
  args = parse_args()
  if args.verbose:
    logger.setLevel(logging.DEBUG)

  existing_browsers = set()

  plex = PlexServer(baseurl=args.baseurl, token=args.token)  # Defaults to localhost:32400

  threads = set()

  i = 0
  for video in plex.search('the'):
  # for video in plex.library.section('Movies'):
    # print('%s (%s)' % (video.title, video.TYPE))
    if i == args.concurrency:
      break
    url = video.getStreamURL(videoResolution='800x600')
    t = threading.Thread(target=play_movie, args=(url, i))
    threads.add(t)
    t.start()
    i += 1
  
  for t in threads:
    t.join()

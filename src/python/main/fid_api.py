from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import argparse
import logging
import socket
import threading
import time

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
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                      action="store_true")
  parser.add_argument("--baseurl", help="baseurl", type=str, required=True)
  parser.add_argument("--token", help="token", type=str, required=True)
  parser.add_argument("--concurrency", type=int, required=True)

  return parser.parse_args()


def play_movie(url, i, run_event):
  logger.info('thread {} started: {}'.format(i, url))
  mb = 1024 * 1024
  while run_event.is_set():
    total = 0
    last = 0
    try:
      r = requests.get(url, stream=True, timeout=2)
      for line in r.iter_lines(chunk_size=1024):
        if not run_event.is_set():
          break
        total += len(line)
        if int(total / mb) > last:
          print("{}: {} mb".format(i, total / mb))
          last = int(total / mb)
    except socket.timeout as e:
      pass

  logger.info('exit thread {}'.format(i))


if __name__ == '__main__':
  args = parse_args()
  if args.verbose:
    logger.setLevel(logging.DEBUG)

  existing_browsers = set()

  plex = PlexServer(baseurl=args.baseurl, token=args.token)  # Defaults to localhost:32400

  run_event = threading.Event()
  run_event.set()
  threads = set()

  for (i, video) in enumerate(plex.search('the')):
    if i == args.concurrency:
      break
    url = video.getStreamURL(videoResolution='800x600')
    t = threading.Thread(target=play_movie, args=(url, i, run_event))
    threads.add(t)
    t.start()

  try:
    while 1:
      time.sleep(.1)
  except KeyboardInterrupt:
    logger.info("exit")
    run_event.clear()
    for t in threads:
      t.join()

import argparse
import json
import logging
import os
import threading

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

  return parser.parse_args()


def play_movie(url):
  r = requests.get(url, stream=True)
  for line in r.iter_lines():
    # filter out keep-alive new lines
    if line:
      print(len(line))


if __name__ == '__main__':
  args = parse_args()
  if args.verbose:
    logger.setLevel(logging.DEBUG)

  existing_browsers = set()

  plex = PlexServer(baseurl=args.baseurl, token=args.token)  # Defaults to localhost:32400

  f = open(os.devnull, "w")
  # zookeeper.set_log_stream(f)
  threads = set()

  for video in plex.search('Game'):
    # print('%s (%s)' % (video.title, video.TYPE))
    url = video.getStreamURL(videoResolution='800x600')
    t = threading.Thread(target=play_movie, args=(url,))
    threads.add(t)
    t.start()

    break

  for t in threads:
    t.join()

  for b in existing_browsers:
    b.quit()

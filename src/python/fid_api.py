import argparse
import json
import logging
import os

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


if __name__ == '__main__':
  args = parse_args()
  if args.verbose:
    logger.setLevel(logging.DEBUG)

  existing_browsers = set()

  plex = PlexServer(baseurl=args.baseurl, token=args.token)  # Defaults to localhost:32400

  f = open(os.devnull, "w")
  # zookeeper.set_log_stream(f)

  for video in plex.search('Game'):
    # print('%s (%s)' % (video.title, video.TYPE))
    url = video.getStreamURL(videoResolution='800x600')
    r = requests.get(url, stream=True)
    for line in r.iter_lines():
      # filter out keep-alive new lines
      if line:
        print(line)
        
    break



    # threads = set()
    # for movie_url in MOVIES:
    #   browser = webdriver.Chrome(executable_path=get_chromedrive_binary())
    #   # browser = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
    #   # browser = webdriver.Firefox()
    #   # browser.set_window_size(1120, 550)
    #   existing_browsers.add(browser)
    #   t = threading.Thread(target=play_movie, args=(browser, movie_url, args))
    #   threads.add(t)
    #   t.start()
    #
    # for t in threads:
    #   t.join()
    #
    # for b in existing_browsers:
    #   b.quit()

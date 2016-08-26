# Plex Traffic Driver
Drives traffic to stress test plex server.


2. In project root dir:

  `./pants binary src/python/main`
  `./dist/main.pex --baseurl=<e.g http://x.x.x.x:32400> --token=<token> --concurrency=<number of concurrent streams>`

   You can find the token by following [this process](https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token)

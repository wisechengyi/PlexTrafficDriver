# Plex Traffic Driver
Drives traffic to stress test plex server.


## In project root dir:

`./pants binary src/python/main`
  
`./dist/main.pex --baseurl=<e.g http://x.x.x.x:32400> --token=<token> --concurrency=<number of concurrent streams>`

You can find the token by following [this process](https://support.plex.tv/hc/en-us/articles/204059436-Finding-your-account-token-X-Plex-Token)

Example output:
```
$ ./dist/main.pex --baseurl=<url> --token=<token> --concurrency=2
INFO:[PlexTrafficDriver]:thread 0 started: http://...:32400/video/:/transcode/universal/foo...
INFO:[PlexTrafficDriver]:thread 1 started: http://...:32400/video/:/transcode/universal/bar...
0: 1.00006389618 mb
1: 1.00014877319 mb
0: 2.0001115799 mb
0: 3.00008106232 mb
1: 2.00019264221 mb
0: 4.00000858307 mb
^CINFO:[PlexTrafficDriver]:exit
INFO:[PlexTrafficDriver]:exit thread 1
INFO:[PlexTrafficDriver]:exit thread 0
```

# TPlumber
TPlumber optimizes resources for Travis CI dependent projects by pushing commits to multiple forks, circumventing the limit of workers in Travis CI per github account.

Disclaimer: This tool only offers the above functionality. Whether you can/should do it depends on your contract with Travis CI.

## Getting Started

1. Manually setup multiple github accounts and fork your project into those accounts, then [sync the forked projects with Travis](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI%3A).

  * Depending how many workers are needed, Travis CI limits OSS projects to have 5 workers per account. E.g. 2 accounts for 10 workers.

2. For each account
  * obtain [Github token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) with access `repo -> public repo`
  * obtain travis ci access token by `curl -i -H 'Content-Type: application/json' -d '{"github_token":"<github token>"}' -H 'User-Agent: Travis/1.0' https://api.travis-ci.org/auth/github`
  * save them for the next step
  
3. Setup credentials

  In your project repo, touch `.token.json` with the following content. Do **NOT** add it to git. (Even if you don't care about security, Github will revoke the tokens if commited to repo.)
  ```
  [
    ["<github account>", "<repo name>", "<github token>", "<travis ci token>"],
    ...(additional accounts go here)
  ]
  ```

3. `git clone https://github.com/wisechengyi/TPlumber.git`

4. `cd TPlumber; ./pants binary src/python:main`

5. In your project directory, execute `<path/to/TPlumber>/dist/main.pex`

  Sample output:
  ```
  $ ./dist/main.pex 
  INFO:[TPlumber]:Starting branch: fiddle
  	Switched to a new branch 'travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_0_wluld'
  	 * [new branch]      head -> travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_0_wluld
  	Switched to branch 'fiddle'
  INFO:[TPlumber]:Delete tmp branch: travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_0_wluld
  	Switched to a new branch 'travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_1_xyigu'
  	 * [new branch]      head -> travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_1_xyigu
  	Switched to branch 'fiddle'
  INFO:[TPlumber]:Delete tmp branch: travis_tmp_br_bbe12f88ea072af5a017f5af1de067dad6349126_1_xyigu
  (Urls below will be opened in browser)
  INFO:[TPlumber]:Build found. Url: https://travis-ci.org/usernameA/repoA/builds/144084316
  INFO:[TPlumber]:Build found. Url: https://travis-ci.org/usernameB/repoA/builds/144084334
  
  $ ./dist/main.pex  --stop-all
  INFO:[TPlumber]:Build https://travis-ci.org/usernameA/repoA/builds/144084316 aborted
  INFO:[TPlumber]:Build https://travis-ci.org/usernameB/repoA/builds/144084334 aborted
  ```

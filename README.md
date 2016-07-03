# Travis Hack
Optimizes CI resources for Travis-CI dependent projects by pushing commits to multiple forks, circumventing the limit of workers in Travis CI per github account.

## Getting Started

1. Setup multiple github accounts and fork your project into those accounts.

  * Depending how many shards you want. Travis CI limits OSS projects to have 5 workers per account. E.g. 2 accounts for 10 workers.

2. For each account, [get its github token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/), save it for next step. 
  
3. Setup credentials

  In your project repo, touch `.token.json`
  ```
  {
    "<github_username_A>": {
      "repo": "<project repo name>",
      "github_token": "<github token A>",
      "travis_ci_token": "<travis ci token A >"
    },
    "<github_username_B>": {
      "repo": "<project repo name>",
      "github_token": "<github token B>",
      "travis_ci_token": "<travis ci token B>"
    }
  }
  ```
  travic ci token can be obtained by 
  `curl -i -H 'Content-Type: application/json' -d '{"github_token":"<github token>"}' -H 'User-Agent: Travis/1.0' https://api.travis-ci.org/auth/github`

3. `git clone https://github.com/wisechengyi/travis_hack.git`

4. Run `<path to travis_hack>/travis_hack`

  Sample output:
  ```
  INFO:__EXP__:Current branch: hack
  Switched to a new branch 'exploit_0fdd071b32db87900dc123a4a082b1e5a87f0625_0_goobj'
   * [new branch]      head -> exploit_0fdd071b32db87900dc123a4a082b1e5a87f0625_0_goobj
  Switched to a new branch 'exploit_c7c650094b9accc8e1ff4e5db42f277b54c454a1_1_hkrje'
   * [new branch]      head -> exploit_c7c650094b9accc8e1ff4e5db42f277b54c454a1_1_hkrje
  INFO:__EXP__:Build found. Url: https://travis-ci.org/usernameA/repoA/builds/141947066
  INFO:__EXP__:Build found. Url: https://travis-ci.org/usernameB/repoA/builds/141947079
  Switched to branch 'hack'
  ```

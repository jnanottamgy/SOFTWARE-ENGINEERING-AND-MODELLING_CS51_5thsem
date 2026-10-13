# Repository rules

## Git identity (mandatory)

Everything committed and pushed to this repository must be authored **and** committed as **jnanottamgy**:

- `user.name`: `jnanottamgy`
- `user.email`: `192404215+jnanottamgy@users.noreply.github.com` (the account's GitHub noreply address, so commits link to the profile)

Each session starts in a fresh container, so set this before the first commit of every session:

```sh
git config user.name "jnanottamgy"
git config user.email "192404215+jnanottamgy@users.noreply.github.com"
git config commit.gpgsign false
```

Before every push, check the identity on the commits being pushed:

```sh
git log --format='%h %an <%ae> | %cn <%ce>' origin/<branch>..HEAD
```

Never push a commit whose author or committer is anyone other than jnanottamgy.

Do not add any Claude attribution to commit messages: no `Co-Authored-By: Claude ...` trailer, no `Claude-Session: ...` link, and no other co-author or session line for Claude. Commits must show jnanottamgy as the only author.

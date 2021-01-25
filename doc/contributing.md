# Contributing to SMT-Python
Honestly, right now it's a free-for-all. Try not to break anyone else's stuff,
but be aware that Ed might mess around with yours while he's deciding on APIs,
coding standards and the like. He apologises unashamedly for this, and will try
to make sure he updates your code in line with any new policies being
implemented.

For now, just try to make sure you pull before you push, and add a useful tag.

## Tags
Only worry about these when commiting to the master branch. Don't feel you have
to use these in your own private branches.

I've found it's easier to read commit histories in `master` when the messages are
tagged. For example, "[BUGFIX] Changes name of input file" makes it obvious why
the commit was done. Tags I'd suggest using are:
- `BUGFIX` - Fixes a bug in an older version of the code
- `IMPROVEMENT` - Does the pretty much the same thing, but in a nicer way
- `ADDITION` - Adds something new that wasn't present before
- `NEW FEATURE` - Adds a significant new piece of functionality
If your commit doesn't fit into any of these, feel free to use your own - just
make it brief (12 chars or less), and try to keep consistent with tags
previously used.

## Example

```{bash}
$ git clone this.repo@github.com

<Make some changes>

$ git add <changes>
$ git commit '[USEFUL TAG] Adds a useful commit message'
$ git pull
$ git push
```

Watch this space!

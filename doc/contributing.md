# Contributing to SMT-Python

If you make changes to SMT-Python, you are free to contribtue them back into the
main codebase so that other people can make use of them too. In order to do
this, make your changes to the source code in a new branch and create a pull
request to get those changes merged back into the `master` branch.

## TLDR
```bash
$ git clone https://www.github.com/ejh516/smt-python
$ git checkout -b new-feature-name

[ Make your changes changes ]

$ git commit -m 'New-feature added'
$ git push

[ Go to https://www.github.com/ejh516/smt-python and create a pull request for 
  the new branch ]

[ Make any changes suggested by the team ]

[ Merge the pull request ]
```

## Getting a copy of the repository
In order to contribute changes, you will first need to get an up-to-date copy of
the `master` branch of the source code. If you don't already have a copy of the
code, you can clone a new copy:
```{bash}
$ git clone https://www.github.com/ejh516/smt-python
```

If you already have a copy of the repository, you can update it to the latest
version:
```bash
$ git checkout master
$ git pull
```

Once you have an up-to-date version of the repository, you can create a branch
to make your changes in. 

## Creating a new branch
In order to keep the `master` branch free from intermediate commits, it's good
practice to develop your changes in a separate branch. These changes can then
be merged back into the master branch once they are complete. To create a new
branch, use the command:
```bash
$ git checkout -b meaningful-branch-name
```

Now, any commits you make will now exist in this branch. If all your changes are
committed, you can even roll back to the unmodified version, or start working on
a different set of changes independently.
```bash
$ git checkout master
$ git checkout -b different-new-feature
```


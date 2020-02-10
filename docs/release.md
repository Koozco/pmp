# Release

1. Begin release process \
`git flow release start x.y.z`
1. Bump up version in `setup.py` (also in downlad link)
1. Commit \
`git commit -a -m'Bump up version to x.y.z'`
1. Finish it. \
`git flow release finish x.y.z`
1. Push `master` with tags \
`git checkout master` \
`git push origin master --tags`


# Release to PyPi

1. Create a source distribution \
`python setup.py sdist`
1. Upload \
`twine upload dist/*`

<Good sanity check: `pip install python-multiwinner-package --upgrade`>

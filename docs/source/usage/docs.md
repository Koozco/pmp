As a documentation tool we use Sphinx, however we stay open for any ideas suggestions,
which may improve our current setup.  
Main file format of Sphinx is _reStructuredText_, but it is also possible to render _Markdown_ in .rst files.

If you want to extend documentation, a place to start is  `docs/source`, where are stored all sources.
After adding sources, compile them with Sphinx Makefile.
```bash
cd docs
make clean html
```
Check the result in `_build/html/index.html`
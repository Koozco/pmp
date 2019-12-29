Using pmp
=========

You can use pmp twofold. If core functionalities satisfy your needs, simply install pmp with pip.
Use it as other python modules. For more details please check instructions.

.. _dev_install:

Developing pmp
--------------

During development of your projects you may need to extend or modify pmp code.

.. mdinclude:: usage/usage.md

Working with docs
-----------------

As a documentation tool we use Sphinx, however we stay open for any ideas suggestions,
which may improve our current setup.
Main file format of Sphinx is *reStructuredText*, but it is also possible to render *Markdown* in .rst files.

If you want to extend documentation, a place to start is  ``docs/source``, where are stored all sources.
After adding sources, compile them with Sphinx Makefile.
::

    cd docs
    make clean html

Check the result in ``_build/html/index.html``

Note: **Depending on your OS it may be necessary not only to install sphinx by pip, but also by OS package manager.**
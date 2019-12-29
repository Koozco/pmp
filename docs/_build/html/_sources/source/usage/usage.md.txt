**We strongly encourage you to use virtualenv during development.**

Install `virtualenv` and test installation.
```
pip install virtualenv
virtualenv --version
```

Clone project and enter it's directory, then create virtual environment for pmp.
```
git clone https://github.com/Koozco/pmp.git
cd pmp
virtualenv pmp_venv    
```

In order to use this venv please remember to use:
`source pmp_venv/bin/activate`

And for deactivation `deactivate`

Install pmp in `editable mode`, so all changes you make in code will be reflected in module's behaviour.
```
pip install -e .
```
Virtual env will allow you to separate this installation and it's dependencies from your globaly installed python.

Enjoy!

Integer linear programming
==========================

PMP allows you to use Cplex and Gurobi as ILP backends.

Gurobi instalation tips
-----------------------

Visit `official Gurobi site <http://www.gurobi.com>`_, get proper license and download installator
dedicated for your operating system.

In order to install required python interface ``gurobipy`` run it's setup script:
::

    cd GUROBI_INSTALATION_DIR
    python setup.py install

Please note it is important to run this script inside gurobi's directory.

Cplex instalation tips
----------------------

Visit `official IBM Cplex site <https://www.ibm.com/products/ilog-cplex-optimization-studio>`_, get proper license and download installator
dedicated for your operating system.

Now install Cplex python interface.
::

    pip install cplex


Please note:
**If you are using virtualenv, you may need to recreate your venv after installing this dependencies.**

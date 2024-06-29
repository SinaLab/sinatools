.. highlight:: shell

===============
Getting Started
===============

Installation
------------

You will need Python 3.10.8 (64-bit) as well as
`the Rust compiler <https://www.rust-lang.org/learn/get-started>`_ installed.


Install using pip
^^^^^^^^^^^^^^^^^

To install sinatools, run this command in your terminal:

.. code-block:: console

    $ pip install sinatools

This is the preferred method to install sinatools, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Install from source
^^^^^^^^^^^^^^^^^^^

The sources for sinatools can be downloaded from the `Github repo`_

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/SinaLab/sinatools/

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/SinaLab/sinatools/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/SinaLab/sinatools/
.. _tarball: https://github.com/SinaLab/sinatools/tarball/master


Installing data
^^^^^^^^^^^^^^^

To install the data sets required by SinaTools See :doc:`reference/packages`.


By default, data is stored in
``C:\Users\your_user_name\AppData\Roaming\sinatools``.


Next Steps
----------

To get started, you can follow along
`the Guided Tour <https://colab.research.google.com/>`_
for a quick overview of the components provided by SinaTools.

See :doc:`cli_tools` for information on using the command-line tools or 
:doc:`api` for information on using the Python API.

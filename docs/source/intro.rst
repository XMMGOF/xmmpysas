Introduction to pySAS
=====================

--------------
What is pySAS?
--------------

pySAS is the official Python wrapper for XMM-Newton's `Science Analysis System`_ 
(SAS). It allows a SAS user to use Python to analize XMM-Newton data, using 
either Python scripts or a Jupyter Notebook.

.. _Science Analysis System: https://www.cosmos.esa.int/web/xmm-newton/what-is-sas

-----------------------
How do I install pySAS?
-----------------------

Before you can use pySAS you first have to install SAS following the  
`installation instructions <https://www.cosmos.esa.int/web/xmm-newton/download-and-install-sas>`_.

**Note**: pySAS contains a function to download and update XMM-Newton 
calibration files. You can have pySAS download the calibration files for you. 

Then pySAS can be installed using *pip*.

.. code-block::

    pip install xmmpysas

**Note**: Make sure you install **xmmpysas**. There is different Python module 
called *pysas* that has nothing to with pySAS for XMM-Newton.

pySAS will occationally be updated with bug fixes and new features. You can 
update pySAS to the latest version using:

.. code-block::

    pip install xmmpysas --upgrade

-------------------------
How do I configure pySAS?
-------------------------

Before you use pySAS for the first time you will need to configure pySAS so 
that it knows where you have SAS installed and where the XMM calibration files 
are located. After installing pySAS using *pip*, in Python run:

.. code-block:: python

    from pysas import config_pysas
    config_pysas.run_config()

This script will ask you for the full path to three directories:

* **sas_dir**: The directory where SAS is installed (i.e. /path/to/xmmsas_XX.X.X).
* **sas_ccfpath**: The directory where the calibration files are stored. If you 
  already have them downloaded, just enter the directory where they are. But if 
  you have not downloaded them yet, you will be given the option to download them 
  after the setup. The script will even create the directory for you.
* **data_dir**: All observation data files will be downloaded into this directory. 
  If the data directory does not exist it will be created for you.

After pySAS has been configured you can import pySAS like normal.

.. code-block:: python

    import pysas

---------------------------------------------
Using pySAS on Fornax, SciServer, or Datalabs
---------------------------------------------

There are **free to use** online data analysis platforms to analize astronomy 
data. These platforms are accessed through a browser and use a Jupyter Lab 
environment as an interface. Currently there are three platforms available where 
you can use pySAS.

* **Fornax**: A collaboration between NASA Goddard Space Flight Center and NASA’s 
  science archives; HEASARC, IRSA, and MAST. (`Link to get an account on Fornax <https://docs.fornax.sciencecloud.nasa.gov/quick-start/>`_)
* **SciServer**: Operated by the *Institute for Data-Intensive Engineering and 
  Science* at Johns Hopkins University. (`Link to SciServer <https://www.sciserver.org/>`_)
* **Datalabs**: Operated by the European Space Agency (ESA). (`Link to Datalabs <https://datalabs.esa.int/>`_)

Both SAS and pySAS come preinstalled on 
`Fornax <https://docs.fornax.sciencecloud.nasa.gov/quick-start/>`_, 
`SciServer <https://www.sciserver.org/>`_, and `Datalabs <https://datalabs.esa.int/>`_. 
On Fornax use the ``sas`` Python environment. On SciServer use the ``xmmsas`` 
Python environment. (**Note** June 8, 2026: The XMM SAS image on Datalabs is 
still being updated. pySAS will work, but a number of pySAS features are not 
available without some manipulation of the environment.)

On Fornax and SciServer the paths to SAS and the calibration files are 
pre-set and the user does not have to do anything. But you can set your default 
data directory by running the following:

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.simple_config()

Document last updated: |date|

.. |date| date:: %Y-%m-%d
.. _topintro:

Introduction to pySAS
=====================

--------------
What is pySAS?
--------------

pySAS is the official Python wrapper for XMM-Newton's `Science Analysis System`_ 
(SAS). It allows a SAS user to use Python to analize XMM-Newton data, using 
either Python scripts or a Jupyter Notebook.

.. _Science Analysis System: https://www.cosmos.esa.int/web/xmm-newton/what-is-sas

pySAS can be used on your own computer or can be used on an online data 
analysis platform.

There are **free to use** online data analysis platforms to analize astronomy 
data. These platforms are accessed through a browser and use a Jupyter Lab 
environment as an interface. Currently there are three online platforms 
available where you can use pySAS.

* **Fornax**: A collaboration between NASA Goddard Space Flight Center and NASA’s 
  science archives; HEASARC, IRSA, and MAST. (`Link to get an account on Fornax <https://docs.fornax.sciencecloud.nasa.gov/quick-start/>`_)
* **SciServer**: Operated by the *Institute for Data-Intensive Engineering and 
  Science* at Johns Hopkins University. (`Link to SciServer <https://www.sciserver.org/>`_)
* **Datalabs**: Operated by the European Space Agency (ESA). (`Link to Datalabs <https://datalabs.esa.int/>`_)

Both SAS and pySAS come preinstalled on 
`Fornax <https://docs.fornax.sciencecloud.nasa.gov/quick-start/>`_, 
`SciServer <https://www.sciserver.org/>`_, and `Datalabs <https://datalabs.esa.int/>`_.

:ref:`Return to top <topintro>`

------------------------------------------
How do I install pySAS on my own computer?
------------------------------------------

You can install pySAS on your local machine to do data analysis. Before you can 
use pySAS you first have to install SAS following the  
`installation instructions <https://www.cosmos.esa.int/web/xmm-newton/download-and-install-sas>`_.

**Note**: pySAS contains a function to download and update XMM-Newton 
calibration files. When you configure pySAS you have the option to download the 
calibration files. :ref:`See below for instructions <configure>`.

Then pySAS can be installed using *pip*.

.. code-block::

    pip install xmmpysas

**Note**: Make sure you install **xmmpysas**. There is different Python module 
called *pysas* that has nothing to with pySAS for XMM-Newton.

pySAS will occationally be updated with bug fixes and new features. You can 
update pySAS to the latest version using:

.. code-block::

    pip install xmmpysas --upgrade

:ref:`Return to top <topintro>`

.. _configure:

---------------------------------------------
How do I configure pySAS on my local machine?
---------------------------------------------

**Note**: Configuring pySAS on Fornax, SciServer, and Datalabs is different 
than configuring pySAS for your own computer. See 
:ref:`below for instructions <online>` on configuring pySAS on Fornax, SciServer, 
and Datalabs.

Before you use pySAS for data analysis you will need to configure pySAS so 
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

:ref:`Return to top <topintro>`

.. _online:

---------------------------------------------
Using pySAS on Fornax, SciServer, or Datalabs
---------------------------------------------

* On Fornax use the ``sas`` Python environment.
* On SciServer use the ``xmmsas`` Python environment. 
* On Datalabs use the ``xmmsas`` image. (**Note** July 8, 2026: The XMM SAS 
  image on Datalabs is still being updated. pySAS will work, but a number of 
  pySAS features are not available without some manipulation of the environment.)

On Fornax, SciServer, and Datalabs the paths to SAS and the calibration files 
are pre-set and the user does not have to do anything. But you still have to set 
your default data directory by running the following command in Python:

**Note** July 8, 2026: `simple_config` currently doesn't work on Datalabs.

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.simple_config()

:ref:`Return to top <topintro>`

Document last updated: |date|

.. |date| date:: %Y-%m-%d
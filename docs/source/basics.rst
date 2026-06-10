The Basics of pySAS
===================

This page provides a brief overview of how to use pySAS.

To learn how to use SAS to do X-ray analysis with pySAS there are 
`Jupyter Notebooks available on GitHub <https://github.com/XMMGOF/pysas_docs>`_ 
with several examples. You can clone the repository with the example 
notebooks by running the following command in a directory of your choosing:

.. code-block::

    git clone https://github.com/XMMGOF/pysas_docs.git

There have been several updates to pySAS between versions 1.4 and 2.0. Most of 
the functionality is the same, but there are some differences.

**Contents:**

#. :ref:`beginning`
#. :ref:`obsid`
#. Downloading Observation Data Files
#. Calling SAS Tasks
#. Input Arguments
#. :ref:`configuration`
#. Default pySAS Data Directory Structure
#. Output Logging
#. Extra Log Output from pySAS
#. Calling SAS Tasks from the Command Line

.. _beginning:

--------------------------------------
Initializing SAS and Configuring pySAS
--------------------------------------

In order for SAS to work certain environment variables need to be initialized. 
If you are running SAS from the command line this is done by sourcing either 
`setsas.sh` or `setsas.csh`. When pySAS has been configured it will 
**automatically** initialize SAS for you. 

When you start pySAS **for the first time** on a local machine, run the 
configuration script as follows:

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
  If the data directory does not exist it will be created for you. If no 
  directory is set then pySAS will use the current working directory.

On Fornax, SciServer, and Datalabs the paths to SAS and the calibration files 
are pre-set and the user does not have to do anything. But you still have to set 
your default data directory by running the following:

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.simple_config()

After this, when you import pySAS all necessary environment variables will 
automatically be set.

.. code-block:: python

    import pysas

For more information on configuring pySAS see the section on 
:ref:`Configuration <configuration>` below.

.. _obsid:

----------------
The ObsID Object
----------------

ObsID is a new pySAS class that makes it easier for the user to interface with 
pySAS. It contains useful functions along with links to important directories 
and files.

To work with a particular observation the user provides an Obs ID to the 
ObsID object, as follows:

.. code-block:: python

    obsid = '##########'
    my_obs = pysas.ObsID(obsid)

``my_obs`` is an 'instance' of the object 'ObsID'. The ObsID class contains 
several useful functions, information, and paths for the observation data you 
are working with.

Important information and paths are stored as variables in the ObsID class. 
These include:

obsid
    The Obs ID number used to create the ObsID object.

data_dir
    Path to base data directory where all XMM data files will be downloaded. 
    (/path/to/data_dir)

obs_dir
    Path to directory containing the data files for a single Obs ID
    (by default, data_dir/obsid).

odf_dir
    Path to directory with the raw observation data files for a single Obs ID
    (by default, obs_dir/ODF).

pps_dir
    Path to directory with the PPS data files for a single Obs ID
    (by default, obs_dir/PPS).

work_dir
    The working directory when SAS tasks will be run 
    (by default, obs_dir/work).

sas_ccf
    Link to the 'ccf.cif' file, if it exists. By default the 'ccf.cif' file 
    will be created in the work_dir.

sas_odf
    Link to the '\*SUM.SAS' file, if it exists. By default the '\*SUM.SAS' file 
    will be created in the work_dir.

files
    A dictionary with links to data files.

The 'files' dictionary will have the following keys:

::

    'sas_ccf'
    'sas_odf'
    'PNevt_list'
    'M1evt_list'
    'M2evt_list'
    'R1evt_list'
    'R2evt_list'
    'OMevt_list'

.. _downloading:

--------------------------------------------------
Downloading and Calibrating Observation Data Files
--------------------------------------------------

After creating an instance of an ObsID object you can download the corresponding 
observation data using a few different functions.

download_ODF_data()
    Can be used to download the ODF files for a single Obs ID.

download_PPS_data()
    Can be used to download the PPS files for a single Obs ID.

download_ALL_data()
    Can be used to download both the ODF and PPS files for a single Obs ID.

Alternatively you can use the function ``basic_setup``. This function will:

1. Download data by calling ``download_ODF_data``
2. Call the function ``calibrate_odf``

    A. Run ``cifbuild``
    B. Run ``odfingest``
    
3. Run ``epproc`` -OR- ``epchain``
4. Run ``emproc`` -OR- ``emchain``
5. Run ``rgsproc``

If the ODF files have previously been downloaded and are in the default data 
directory, then upon creating the ObsID object (i.e. "my_obs = pysas.ObsID(obsid)") 
pySAS will automatically find and link all important summary and calibration 
files, and also all previously generated event lists made by epproc, emproc, 
and rgsproc.

If your data is still proprietary pySAS can still download it, but depending on 
whether you are getting your data from the XSA (ESA) or the HEASARC (NASA) the 
information you need to provide will be different.

To download proprietary data from the XSA at ESA using any of the download 
functions or `basic_setup` you need to set the input `proprietary` to `True`, 
as shown below.

.. code-block:: python

    obsid = '##########'
    my_obs = pysas.ObsID(obsid)
    my_obs.basic_setup(proprietary=True)

The data request is made using astroquery and astroquery will ask for the user's 
Cosmos username and password. The ESA module for astroquery allows many more 
inputs for specifying exactly what XMM data to download. All of those inputs can 
be passed in as additional arguments. Those inputs will be passed on to 
astroquery.

Proprietary data from the HEASARC comes encrypted. Anyone can download it, but 
you need an encryption key to unpack the data. The encryption key is a 
alphanumeric string with 30 characters. You provide the encryption key to 
basic_setup and pySAS will handle the rest.

.. code-block:: python

    my_obs.basic_setup(repo='heasarc',encryption_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

.. _configuration:

-----------------------------------------
Default Configuration and the Config File
-----------------------------------------
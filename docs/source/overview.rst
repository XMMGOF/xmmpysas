.. _topoverview:

Overview of pySAS
=================

This page provides an overview of how to use pySAS.

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
#. :ref:`downloading`
#. :ref:`mytask`
#. :ref:`datadir`

.. _beginning:

--------------------------------------
Initializing SAS and Configuring pySAS
--------------------------------------

In order for SAS to work, certain environment variables need to be initialized. 
If you are running SAS from the command line this is done by sourcing either 
``setsas.sh`` or ``setsas.csh``. When pySAS has been configured it will 
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
:ref:`configuring pySAS <config>`.

:ref:`Return to top <topoverview>`

.. _obsid:

----------------
The ObsID Object
----------------

:py:class:`~pysas.obsid.ObsID` is a pySAS class that makes it easier for the 
user to interface with XMM data files. It contains useful functions along with 
links to important directories and files.

To work with a particular observation the user provides an Obs ID to the 
:py:class:`~pysas.obsid.ObsID` object, as follows:

.. code-block:: python

    obsid = '##########'
    my_obs = pysas.ObsID(obsid)

``my_obs`` is an 'instance' of the object ':py:class:`~pysas.obsid.ObsID`'. The 
:py:class:`~pysas.obsid.ObsID` class contains several useful functions, 
information, and paths for the observation data you are working with.

Important information and paths are stored as variables in the 
:py:class:`~pysas.obsid.ObsID` class. These include:

obsid
    The Obs ID number used to create the :py:class:`~pysas.obsid.ObsID` object.

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

:ref:`Return to top <topoverview>`

.. _downloading:

--------------------------------------------------
Downloading and Calibrating Observation Data Files
--------------------------------------------------

After creating an instance of an :py:class:`~pysas.obsid.ObsID` object you can 
download the corresponding observation data using a few different functions.

download_ODF_data()
    Can be used to download the ODF files for a single Obs ID.

download_PPS_data()
    Can be used to download the PPS files for a single Obs ID.

download_ALL_data()
    Can be used to download both the ODF and PPS files for a single Obs ID.

Alternatively you can use the function :py:class:`~pysas.obsid.ObsID.basic_setup`. 
This function will:

1. Download data by calling :py:class:`~pysas.obsid.ObsID.download_ODF_data`
2. Call the function :py:class:`~pysas.obsid.ObsID.calibrate_odf`

    A. Run ``cifbuild``
    B. Run ``odfingest``
    
3. Run ``epproc`` -OR- ``epchain``
4. Run ``emproc`` -OR- ``emchain``
5. Run ``rgsproc``

If the ODF files have previously been downloaded and are in the default data 
directory, then upon creating the :py:class:`~pysas.obsid.ObsID` object 
(i.e. "my_obs = pysas.ObsID(obsid)") pySAS will automatically find and link all 
important summary and calibration files, and also all previously generated event 
lists made by ``epproc``, ``emproc``, and ``rgsproc``.

If your data is still proprietary pySAS can still download it, but depending on 
whether you are getting your data from the XSA (ESA) or the HEASARC (NASA) the 
information you need to provide will be different.

To download proprietary data from the XSA at ESA using any of the download 
functions or :py:class:`~pysas.obsid.ObsID.basic_setup` you need to set the 
input ``proprietary`` to ``True``, as shown below.

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

:ref:`Return to top <topoverview>`

.. _mytask:

-----------------
Calling SAS Tasks
-----------------

All standard SAS tasks are called using the :py:class:`~pysas.sastask.MyTask` 
object in pySAS.

.. code-block:: python

    from pysas import MyTask

:py:class:`~pysas.sastask.MyTask` takes two inputs, the first is the name of the 
SAS task as a string. The second is a dictionary with the input arguments for 
the SAS task. If there are no input arguments then the dictionary will be empty:

.. code-block:: python

    MyTask('sasversion', {}).run()

Each input argument will take the form of a 'key' (parameter name) and 'value' 
(parameter value) pair. Each parameter value should be a single string.

.. code-block:: python

    inargs = {'table'           : 'event_list.fits',
              'withfilteredset' : 'yes',
              'expression'      : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'",
              'filteredset'     : 'filtered_event_list.fits',
              'filtertype'      : 'expression', 
              'keepfilteroutput': 'yes',
              'updateexposure'  : 'yes',
              'filterexposure'  : 'yes'}

    MyTask('evselect', inargs).run()

Note: Some inputs require single quotes to be preserved in the string. 
This can be done using double quotes to form the string. i.e. 
``"'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'"``

If you need to pass in command line options to a SAS task, add it to the 
dictionary with the key ``options``. For example,

.. code-block:: python

    inargs = {'options'         : '--verbosity 6 --noclobber'
              'table'           : 'event_list.fits',
              'withfilteredset' : 'yes',
              'expression'      : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'",
              'filteredset'     : 'filtered_event_list.fits',
              'filtertype'      : 'expression', 
              'keepfilteroutput': 'yes',
              'updateexposure'  : 'yes',
              'filterexposure'  : 'yes'}

    MyTask('evselect', inargs).run()

:ref:`Return to top <topoverview>`

.. _datadir:

--------------------------------------
Default pySAS Data Directory Structure
--------------------------------------

pySAS assumes your XMM data is kept in a single directory data_dir. 
For example,

.. code-block:: python

    data_dir = '/path/to/data_dir/'

If you are running pySAS on SciServer the path to data_dir may be somthing like: 
``/home/idies/workspace/Temporary/rtanner/scratch/xmm_data/``. If you are running 
pySAS on your local machine or on Fornax the path may be something like: 
``/home/rtanner/xmm_stuff/xmm_data/``.

Once the ``data_dir`` is set pySAS will download data files for individual 
Obs IDs into their own directory. With data from multiple Obs IDs your 
``data_dir`` would look like this:

.. code-block::

    └── data_dir
        ├── 0104860501
        ├── 0112200301
        ├── 0123700101
        ├── 0400550201
        ├── 0790830101
        ├── ...

The directory for each individual Obs ID can (but it doesn't have to) contain 
subdirectories for ODF and PPS files, and a work directory. A single Obs ID 
directory may have subdirectories for just ODF files and a work directory, or a 
PPS directory and a work directory, or all three directories, depending on what 
level of data files you downloaded. The overall structure might look something 
like this:

.. code-block::

    └── data_dir
        ├── 0104860501
        │   ├── ODF
        │   ├── PPS
        │   └── work
        ├── 0112200301
        │   ├── ODF
        │   └── work
        ├── 0123700101
        │   ├── ODF
        │   └── work
        ├── 0400550201
        │   ├── PPS
        │   └── work
        ├── 0790830101
        │   ├── ODF
        │   ├── PPS
        │   └── work
        └── ...

You should run SAS tasks inside the work directory for the Obs ID you are 
working with. It is possible to run SAS tasks from any directory, but whichever 
directory you are in when you run a SAS task, that is where SAS will output any 
new files.

In some cases it is convenient to create a subdirectory within the work 
directory if the SAS tasks you are running will generate a very large number of 
output files. For example, if you are working with Optical Monitor data the 
file structure for the Obs ID you are working with may look like this:

.. code-block::

    ├── 0400550201
    │   ├── ODF
    │   ├── PPS
    │   ├── work
    │   │   └── OM_files

:ref:`Return to top <topoverview>`

Document last updated: |date|

.. |date| date:: %Y-%m-%d
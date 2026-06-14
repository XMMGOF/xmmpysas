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
#. :ref:`downloading`
#. :ref:`mytask`
#. :ref:`inputs`
#. :ref:`configuration`
#. :ref:`datadir`
#. :ref:`logging`
#. :ref:`pysasverbosity`
#. :ref:`sascommands`

.. _beginning:

--------------------------------------
Initializing SAS and Configuring pySAS
--------------------------------------

In order for SAS to work certain environment variables need to be initialized. 
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
functions or ``basic_setup`` you need to set the input ``proprietary`` to 
``True``, as shown below.

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

.. _mytask:

-----------------
Calling SAS Tasks
-----------------

All standard SAS tasks are called using the MyTask object in pySAS.

.. code-block:: python

    from pysas import MyTask

``MyTask`` takes two inputs, the first is the name of the SAS task as a string. 
The second is a dictionary with the input arguments for the SAS task. If there 
are no input arguments then the dictionary will be empty:

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
dictionary with they key ``options``. For example,

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

.. _inputs:

---------------
Input Arguments
---------------

As noted above, for all SAS tasks, input arguments should be in a dictionary, 
with each parameter value a single string.

For example,

.. code-block:: python
    inargs = {'table'            : 'event_list.fits', 
              'withfilteredset'  : 'yes', 
              'expression'       : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'", 
              'filteredset'      : 'filtered_event_list.fits', 
              'filtertype'       : 'expression', 
              'keepfilteroutput' : 'yes', 
              'updateexposure'   : 'yes', 
              'filterexposure'   : 'yes'}

    MyTask('evselect', inargs).run()

or it could even be written like this:

.. code-block:: python

    inargs = {}
    inargs['table']            = 'event_list.fits'
    inargs['withfilteredset']  = 'yes'
    inargs['expression']       = "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'"
    inargs['filteredset']      = 'filtered_event_list.fits'
    inargs['filtertype']       = 'expression'
    inargs['keepfilteroutput'] = 'yes'
    inargs['updateexposure']   = 'yes'
    inargs['filterexposure']   = 'yes'

    MyTask('evselect', inargs).run()

Then if a single input needs to be changed and the same SAS task run again the 
user could simply use:

.. code-block:: python

    inargs['expression'] = "'(PATTERN <= 12)&&(PI in [4000:12000])&&#XMMEA_EM'"
    MyTask('evselect', inargs).run()

For versions of pySAS before v2.0, the input arguments were passed in as a list. 
And in pySAS v2.0 you can still pass in the input arguments as a list. 
pySAS v2.0 is fully backwards compatible.

.. code-block:: python

    inargs = ['table=event_list.fits', 
              'withfilteredset=yes', 
              "expression='(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'", 
              'filteredset=filtered_event_list.fits', 
              'filtertype=expression', 
              'keepfilteroutput=yes', 
              'updateexposure=yes', 
              'filterexposure=yes']

    MyTask('evselect', inargs).run()

While the values for all input arguments should be in string format, 
pySAS v2.0 will accept numbers, as shown below. These numbers will be 
converted into strings automatically.

.. code-block:: python

    inargs = {}
    inargs['spectrumset'] = 'R1_spectra.fits'
    inargs['rmfset']      = 'rmf1_file.fits'
    inargs['evlist']      = 'R1_event_list'
    inargs['emin']        = 0.4
    inargs['emax']        = 2.5
    inargs['rows']        = 4000

    MyTask('rgsrmfgen', inargs).run()

Also in pySAS v2.0 'yes/no' parameters can be passed in as a Python boolean:

.. code-block:: python

    inargs = {'table'            : 'event_list.fits', 
              'withfilteredset'  : True, 
              'expression'       : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'", 
              'filteredset'      : 'filtered_event_list.fits', 
              'filtertype'       : 'expression', 
              'keepfilteroutput' : True, 
              'updateexposure'   : True, 
              'filterexposure'   : True}

    MyTask('evselect', inargs).run()

The user can get all the default parameters for any SAS task by using:

.. code-block:: python

    task_name = 'insert_task_name'
    inargs = pysas.param.get_input_params(task_name)

This will return a special obejct that behaves just like a normal Python 
dictionary with all possible input arguments for a given SAS task, along 
with their default values. The user can modify the values in this dictionary 
and pass it back in to MyTask.

Note: This is still experimental. We have tested this, but it is possible to 
run into some unexpected behavior. We are aware of at least one (!) case with 
unexpected behavior for an uncommonly used SAS task.


.. _configuration:

-----------------------------------------
Default Configuration and the Config File
-----------------------------------------

Default settings for pySAS are stored in a configuration file. pySAS uses the 
standard Python configuration module ``configparser``.

The configuration file for SAS can be found in the user's HOME directory 
(or the ``XDG_CONFIG_HOME`` directory which is usually the user's HOME 
directory) inside the hidden directory ``.config``, then inside the sas 
directory. The configuration file will be named ``sas.cfg``. It can be opened 
and edited by any text editor.

.. code-block::

    $HOME/.config/sas/sas.cfg

You can see the contents of your config file by running the following command.

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.show_config_file()

The output will look something like this:

.. code-block:: python

    [DEFAULT]
    suppress_warning = 1
    verbosity = 4
    pysas_verbosity = WARNING
    repo = ESA

    [sas]
    sas_dir = /opt/envs/sas/xmmsas_22.1.0-a8f2c2afa-20250304
    sas_ccfpath = /opt/support-data/xmm_ccf
    data_dir = /home/jovyan/xmm_data
    repo = fornax
    pysas_verbosity = DEBUG

The values in ``[sas]`` will override the ``[DEFAULT]`` values. These values 
can be edited by hand, but it is strongly recommended to use the methods 
included with pySAS to change the default values.

The config file contains default settings for ``verbosity`` (the amount of 
output from running SAS), a default data directory, and a default repository 
from which to download data.

The default data directory can be set or changed later using the function 
``set_setting_and_save``. For example,

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.set_setting_and_save('data_dir', '/path/to/new/data_dir')

All other default settings can also be set in the same way.

At any time the user can reset all defaults using the following command:

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.reset_to_defaults()

There are four default settings:

suppress_warning
    Default = 1. SAS environment variable ranging from 1-10 controlling the 
    amount of warnings produced by SAS tasks.

verbosity
    Default = 4. SAS environment variable ranging from 1-10 controlling the 
    amount of information produced by SAS tasks.

pysas_verbosity
    Default = WARNING. pySAS environment variable controlling the amount of 
    information displayed by pySAS. See the section Extra Log Output from pySAS 
    for more information.

repo
    Default = ESA. The repository to use to download XMM data. 
    Options are: ESA, HEASARC, AWS, Fornax (only available on Fornax), and 
    SciServer (only available on SciServer).

After configuring pySAS (see :ref:`beginning` above) there will be three 
additional settings:

sas_dir
    The installation directory of SAS.

sas_ccfpath
    The directory containing XMM calibration files.

data_dir
    Directory where your observation data will be downloaded 
    (see Default pySAS Data Directory Structure).


.. _datadir:

--------------------------------------
Default pySAS Data Directory Structure
--------------------------------------

pySAS assumes your XMM data is kept in a single directory data_dir. 
For example,

.. code-block:: python

    data_dir = '/path/to/data_dir/'

If you are running pySAS on SciServer the path to data_dir may be somthing like: 
``/home/idies/workspace/Temporary/rjtanner/scratch/xmm_data/``. If you are running 
pySAS on your local machine the path may be something like: 
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


.. _logging:

--------------
Output Logging
--------------

The ObsID class accepts inputs to control output logging. The inputs to 
ObsID are:

.. code-block::

    obsid (required)
    data_dir    = None
    logfilename = None
    tasklogdir  = None
    output_to_terminal = True
    output_to_file     = False

obsid 
    (Required) The 10-digit observation ID number for the observation you 
    are working with.

data_dir
    Directory where you want the XMM data downloaded.

logfilename
    If defined, then all output will be written to this file (but only if 
    ``output_to_file=True``). If no file name is given then the name of the log 
    file will be ``ObsID_+the Obs ID`` you are working with. Any SAS tasks run 
    using ``basic_setup`` (i.e. ``cifbuild``, ``odfingest``, ``emproc``, 
    ``epproc``, and ``rgsproc``) will have their output written to their own 
    file in the ``work_dir``.

tasklogdir
    The directory where output log files will be written. If not defined then 
    it will use the ``data_dir`` for all top level Python related output, and 
    ``work_dir`` for all other SAS tasks.

output_to_terminal
    If True then output will be written to the terminal, if False then not.

output_to_file
    If True then output will be written to a log file, if False then not.

If you are running an individual task, for example ``evselect``, the ``MyTask`` 
object also accepts the same logging inputs as the ``ObsID`` class.

.. code-block::

    taskname (required)
    inargs   (required)
    logfilename = None, 
    tasklogdir  = None,
    output_to_terminal = True, 
    output_to_file     = False

The difference is that ``logfilename`` will default to the task name, and 
``tasklogdir`` will default to the current working directory (which should be 
the ``work_dir`` since that is where you will be running SAS tasks).


.. _pysasverbosity:

---------------------------
Extra Log Output from pySAS
---------------------------

SAS has its own verbosity that controls how much output is generated. If you 
change the verbosity for all of SAS it will also change the verbosity for 
pySAS accordingly. BUT, it is possible to set the verbosity for pySAS 
separately. pySAS has default configurations, and one of the options is 
``pysas_verbosity``. This is information specifically for pySAS, and not the 
individual SAS tasks you may be running. The levels of verbosity for pySAS 
are:

.. code-block::

    CRITICAL : Similar to SAS verbosity of '1'
    ERROR    : Similar to SAS verbosity of '2' or '3'
    WARNING  : Similar to SAS verbosity of '4' or '5'
    INFO     : Similar to SAS verbosity of '6' or '7'
    DEBUG    : Similar to SAS verbosity of '8', '9', or '10'

The default verbosity is set to ``WARNING``. You can set the verbosity for 
pySAS by using the command,

.. code-block:: python

    pysas.sas_cfg.set_setting_and_save('pysas_verbosity', value)

with the 'value' set to whatever level you need.


.. _sascommands:

---------------------------------------
Calling SAS Tasks from the Command Line
---------------------------------------

Underneath what pySAS is doing is running SAS tasks as a Python subprocess. It 
calls each SAS task as if you were running the SAS command from the command line 
in a terminal. If you were to run SAS tasks from the command line this is what 
it would look like:

Calling a SAS task takes the general form:

.. code-block::

    task_name input1=value1 input2=value2 input3=value3 ...

For example, to call ``epproc`` with no inputs (which means using the default 
inputs):

.. code-block::

    epproc

Or to call ``epproc`` with a single input:

.. code-block::

    epproc withoutoftime=yes

A slightly more complex call using the command ``evselect`` with more inputs 
may look like:

.. code-block::

    evselect table=mos1.fits withimageset=yes imageset=image.fits xcolumn=X 
    ycolumn=Y imagebinning=imageSize ximagesize=600 yimagesize=600

In the most extreme cases a very complex task call of ``evselect`` may look 
like this (all on one line at the command prompt):

Note: It is unusual to have this many inputs. This lists all possible inputs, 
including the defaults, for ``evselect``.

.. code-block::

    evselect table='P0123700101M1S001MIEVLI0000.FTZ' keepfilteroutput='no' 
    withfilteredset='no' filteredset='filtered.fits' destruct='yes' 
    flagcolumn='EVFLAG' flagbit='-1' filtertype='expression' dssblock='' 
    expression='true' writedss='yes' cleandss='no' updateexposure='yes' 
    filterexposure='yes' blockstocopy='' attributestocopy='' energycolumn='PHA' 
    withzcolumn='no' zcolumn='WEIGHT' withzerrorcolumn='no' 
    zerrorcolumn='EWEIGHT' ignorelegallimits='no' withimageset='yes' 
    imageset='image.fits' xcolumn='X' ycolumn='Y' imagebinning='imageSize' 
    ximagebinsize='1' yimagebinsize='1' squarepixels='no' ximagesize='600' 
    yimagesize='600' withxranges='no' ximagemin='1' ximagemax='640' 
    withyranges='no' yimagemin='1' yimagemax='640' withimagedatatype='no' 
    imagedatatype='Real64' withcelestialcenter='no' raimagecenter='0' 
    decimagecenter='0' withspectrumset='no' spectrumset='spectrum.fits' 
    spectralbinsize='5' withspecranges='no' specchannelmin='0' 
    specchannelmax='11999' nonStandardSpec='no' withrateset='no' 
    rateset='rate.fits' timecolumn='TIME' timebinsize='1' withtimeranges='no' 
    timemin='0' timemax='1000' maketimecolumn='no' makeratecolumn='no' 
    withhistogramset='no' histogramset='histo.fits' histogramcolumn='TIME' 
    histogrambinsize='1' withhistoranges='no' histogrammin='0' 
    histogrammax='1000'

There are several valid ways to format the inputs. For example, the following 
are all valid ways of including an input:

.. code-block::

    rgsproc withsrc=F
    rgsproc withsrc=no
    rgsproc withsrc='no'
    rgsproc withsrc="no"

Some inputs require spaces. In that case the entire input value must be inside 
either 'single' or "double" quotes. For example:

.. code-block::

    rgsproc withsrc=no orders='1 2 3'
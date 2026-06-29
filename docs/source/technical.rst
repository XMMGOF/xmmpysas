.. _toptechnical:

Technical Information for Advanced Users
========================================

This page contains techinical information related to SAS and pySAS in excessive 
detail. Here is a list of this page's contents:

#. :ref:`config`
#. :ref:`inputs`
#. :ref:`logging`
#. :ref:`pysasverbosity`
#. :ref:`oldnewpysas`
#. :ref:`sascommands`

.. _config:

-----------------------------------------
Default Configuration and the Config File
-----------------------------------------

Default settings for pySAS are stored in a configuration file. pySAS uses the 
standard Python configuration module ``configparser``.

When you import pySAS it will read the configuration file and set environment 
variables based on that. After you have imported pySAS you can change the 
configuration settings without changing the configuration file. Those changes 
will stay in effect until you import pySAS again (i.e. you restart the Python 
kernal). If you make any changes to the configuration file they will not take 
effect until you import pySAS again (i.e. after restarting the Python kernal).

The configuration file for SAS can be found in the user's HOME directory 
(or the ``XDG_CONFIG_HOME`` directory which is usually the user's HOME 
directory) inside the hidden directory ``.config``, then inside the sas 
directory. The configuration file will be named ``sas.cfg``. It can be opened 
and edited by any text editor (but this is not recommended, pySAS has functions 
to make changes to the config file).

.. code-block::

    $HOME/.config/sas/sas.cfg

Configuration settings are controled by the top level object 
:py:class:`~pysas.config_pysas.sas_config` that can be accessed either by 
importing it directly, i.e.

.. code-block:: python

    from pysas import sas_cfg

or by accessing it after importing pySAS.

.. code-block:: python

    import pysas
    pysas.sas_cfg.{function command}

The :py:class:`~pysas.config_pysas.sas_config` object has several functions to 
let you control the config file. You can see the contents of your config file by 
running the following command.

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

You can view the current configuration settings by running the following command:

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.show_current_config()

In *almost* all cases the current configuration settings will be exactly the 
same as what is in the config file, but if you modified the settings after 
importing pySAS then the current settings will not match what is in the config 
file. Having them be different is not something that happens by accident and is 
very rare. This is mentioned because a few of the tutorial Jupyter notebooks 
will explicitly modify the current configuration settings, but will **not** 
change the config file.

The config file contains default settings for ``verbosity`` (the amount of 
output from running SAS), a default data directory, and a default repository 
from which to download data.

The default data directory can be set or changed using the function 
:py:class:`~pysas.config_pysas.sas_config.set_setting_and_save`. For example,

.. code-block:: python

    from pysas import sas_cfg
    sas_cfg.set_setting_and_save('data_dir', '/path/to/new/data_dir')

This will change the default data_dir, **but it will not create it!** If you 
change the default data directory you have to make sure the directory exists!

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
    information displayed by pySAS. See the section :ref:`pysasverbosity` 
    for more information.

repo
    Default = ESA. The repository to use to download XMM data. 
    Options are: ESA, HEASARC, AWS, Fornax (only available on Fornax), and 
    SciServer (only available on SciServer).

After configuring pySAS there will be three additional settings:

sas_dir
    The installation directory of SAS.

sas_ccfpath
    The directory containing XMM calibration files.

data_dir
    Directory where your observation data will be downloaded 
    (see :ref:`datadir`).

:ref:`Return to top <toptechnical>`

.. _inputs:

---------------
Input Arguments
---------------

As noted above, for all SAS tasks input arguments should be in a dictionary, 
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

:ref:`Return to top <toptechnical>`

.. _logging:

--------------
Output Logging
--------------

The :py:class:`~pysas.obsid.ObsID` class accepts inputs to control output 
logging. The inputs to :py:class:`~pysas.obsid.ObsID` are:

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
    Directory where you want the XMM data downloaded. If not given then pySAS 
    will use the default data directory set by the config file.

logfilename
    If defined, then all output will be written to this file (but only if 
    ``output_to_file=True``). If no file name is given then the name of the log 
    file will be ``ObsID_+the Obs ID`` you are working with. Any SAS tasks run 
    will have their output written to their own file in the ``work_dir``.

tasklogdir
    The directory where output log files will be written. If not defined then 
    it will use the ``data_dir`` for all top level Python related output, and 
    ``work_dir`` for all other SAS tasks.

output_to_terminal
    If True then output will be written to the terminal, if False then not.

output_to_file
    If True then output will be written to a log file, if False then not.

If you are running an individual task, for example ``evselect``, the 
:py:class:`~pysas.sastask.MyTask` object also accepts the same logging inputs as 
the :py:class:`~pysas.obsid.ObsID` class.

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

:ref:`Return to top <toptechnical>`

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

:ref:`Return to top <toptechnical>`

.. _oldnewpysas:

-------------------
pySAS v1.4 vs. v2.0
-------------------

Up to (at least) SAS 23 the original version of pySAS (v1.4) comes with SAS. 
When you install SAS the original pySAS is located in 
'``{SAS install directory}/lib/python/pysas/``'. If you initialize SAS from the 
command line by sourcing either ``setsas.sh`` or ``setsas.csh``, it will add 
the original pySAS directory to your system PATH and PYTHONPATH variables. This 
will override any calls to the version of pySAS installed using `pip`. To use 
the current version of pySAS that is installed using `pip` you will have to 
remove '``{SAS install directory}/lib/python/pysas/``' from your PATH and 
PYTHONPATH variables.

If you we previously using pySAS v1.4 which comes with SAS, this next section 
gives a quick explanation of the major differences.

* The 'Wrapper' has been deprecated and replaced by :py:class:`~pysas.sastask.MyTask`.
* MyTask accepts the options `output_to_terminal` and `output_to_file`
* Input arguments can be passed in as either a dictionary or a list

To implement these changes make the following modification to your code.

Change these lines from this:

.. code-block:: python

    from pysas.wrapper import Wrapper as w
    w('Task Name',inargs).run()

to this:

.. code-block:: python

    from pysas import MyTask
    MyTask('Task Name',inargs).run()

Everything else should work the same.

:ref:`Return to top <toptechnical>`

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

:ref:`Return to top <toptechnical>`

Document last updated: |date|

.. |date| date:: %Y-%m-%d
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

Contents

Initializing SAS and Configuring pySAS
The ObsID Object
Downloading Observation Data Files
Calling SAS Tasks
Input Arguments
Default Configuration and the Config File
Default pySAS Data Directory Structure
Output Logging
Extra Log Output from pySAS
Calling SAS Tasks from the Command Line


4. Calling SAS Tasks
All standard SAS tasks are called using the MyTask object in pySAS.

from pysas import MyTask
MyTask takes two inputs, the first is the name of the SAS task as a string. The second is a dictionary with the input arguments for the SAS task. If there are no input arguments then the dictionary will be empty:

MyTask('sasversion', {}).run()
Each input argument will take the form of a 'key' (parameter name) and 'value' (parameter value) pair. Each parameter value should be a single string.

inargs = {'table'           : 'event_list.fits',
          'withfilteredset' : 'yes',
          "expression"      : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'",
          'filteredset'     : 'filtered_event_list.fits',
          'filtertype'      : 'expression', 
          'keepfilteroutput': 'yes',
          'updateexposure'  : 'yes',
          'filterexposure'  : 'yes'}

MyTask('evselect', inargs).run()
Note: Some inputs require single quotes to be preserved in the string. This can be done using double quotes to form the string. i.e. "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'"
If you need to pass in command line options to a SAS task, add it to the dictionary with they key 'options'. For example,

inargs = {'options'         : '--verbosity 6 --noclobber'
          'table'           : 'event_list.fits',
          'withfilteredset' : 'yes',
          "expression"      : "'(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'",
          'filteredset'     : 'filtered_event_list.fits',
          'filtertype'      : 'expression', 
          'keepfilteroutput': 'yes',
          'updateexposure'  : 'yes',
          'filterexposure'  : 'yes'}

MyTask('evselect', inargs).run()

5. Input Arguments
As noted above, for all SAS tasks, input arguments should be in a dictionary, with each parameter value a single string.

For example,

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
Then if a single input needs to be changed and the same SAS task run again the user could simply use:

inargs['expression'] = "'(PATTERN <= 12)&&(PI in [4000:12000])&&#XMMEA_EM'"
MyTask('evselect', inargs).run()
For versions of pySAS before v2.0, the input arguments were passed in as a list. And in pySAS v2.0 you can still pass in the input arguments as a list. pySAS v2.0 is fully backwards compatible.

inargs = ['table=event_list.fits', 
          'withfilteredset=yes', 
          "expression='(PATTERN <= 12)&&(PI in [200:4000])&&#XMMEA_EM'", 
          'filteredset=filtered_event_list.fits', 
          'filtertype=expression', 
          'keepfilteroutput=yes', 
          'updateexposure=yes', 
          'filterexposure=yes']

MyTask('evselect', inargs).run()
While the values for all input arguments should be in string format, pySAS v2.0 will accept numbers, as shown below. These numbers will be converted into strings automatically.

inargs = {}
inargs['spectrumset'] = 'R1_spectra.fits'
inargs['rmfset']      = 'rmf1_file.fits'
inargs['evlist']      = 'R1_event_list'
inargs['emin']        = 0.4
inargs['emax']        = 2.5
inargs['rows']        = 4000

MyTask('rgsrmfgen', inargs).run()
Also in pySAS v2.0 'yes/no' parameters can be passed in as a Python boolean:

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

task_name = 'insert_task_name'
inargs = pysas.param.get_input_params(task_name)
This will return a special obejct that behaves just like a normal Python dictionary with all possible input arguments for a given SAS task, along with their default values. The user can modify the values in this dictionary and pass it back in to MyTask.

Note: This is still experimental. We have tested this, but it is possible to run into some unexpected behavior. We are aware of at least one (!) case with unexpected behavior for an uncommonly used SAS task.

6. Default Configuration and the Config File
Default settings for pySAS are stored in a configuration file (unless you are running pySAS on SciServer). pySAS uses the standard Python configuration module configparser.

The configuration file for SAS can be found in the user's HOME directory (or the XDG_CONFIG_HOME directory which is usually the user's HOME directory) inside the hidden directory .config, then inside the sas directory. The configuration file will be named sas.cfg. It can be opened and edited by any text editor.

$HOME/.config/sas/sas.cfg
You can see the contents of your config file by running the following cell.

from pysas import sas_cfg
sas_cfg.show_config_file()
[DEFAULT]
suppress_warning = 1
verbosity = 4
pysas_verbosity = WARNING
repo = ESA

[sas]
sas_dir = /opt/envs/sas/xmmsas_22.1.0-a8f2c2afa-20250304
sas_ccfpath = /opt/support-data/xmm_ccf
repo = fornax
data_dir = /home/jovyan/xmm_data
pysas_verbosity = DEBUG


The values in [sas] will override the [DEFAULT] values. These values can be edited by hand, but it is strongly recommended to use the methods included with pySAS to change the default values.

The config file contains default settings for verbosity (the amount of output from running SAS), a default data directory, and a default repository from which to download data.

The default data directory can be set or changed later using the function set_setting_and_save. For example,

from pysas import sas_cfg
sas_cfg.set_setting_and_save('data_dir', '/path/to/new/data_dir')
All other default settings can also be set in the same way.

At any time the user can reset all defaults using the following command:

from pysas import sas_cfg
sas_cfg.reset_to_defaults()
There are four default settings:

suppress_warning: Default = 1, A SAS environment variable ranging from 1-10 controlling the amount of warnings produced by SAS tasks.
verbosity: Default = 4, A SAS environment variable ranging from 1-10 controlling the amount of information produced by SAS tasks.
pysas_verbosity: Default = WARNING, A pySAS environment variable controlling the amount of information displayed by pySAS. See the section Extra Log Output from pySAS for more information.
repo: Default = ESA, The repository to use to download XMM data. Options are: ESA, HEASARC, AWS, Fornax (only available on Fornax), and SciServer (only available on SciServer).
After configuring pySAS (see Initializing SAS and Configuring pySAS above) there will be three additional settings:

sas_dir: The installation directory of SAS.
sas_ccfpath: The directory containing XMM calibration files.
data_dir: Directory where your observation data will be downloaded (see Default pySAS Data Directory Structure).

7. Default pySAS Data Directory Structure
pySAS assumes your XMM data is kept in a single directory data_dir. For example,

data_dir = '/path/to/data_dir/'
If you are running pySAS on SciServer the path to data_dir may be somthing like: /home/idies/workspace/Temporary/rjtanner/scratch/xmm_data/. If you are running pySAS on your local machine the path may be something like: /home/rtanner/xmm_stuff/xmm_data/.

Once the data_dir is set pySAS will download data files for individual Obs IDs into their own directory. With data from multiple Obs IDs your data_dir would look like this:

└── data_dir
    ├── 0104860501
    ├── 0112200301
    ├── 0123700101
    ├── 0400550201
    ├── 0790830101
    ├── ...
The directory for each individual Obs ID can (but it doesn't have to) contain subdirectories for ODF and PPS files, and a work directory. A single Obs ID directory may have subdirectories for just ODF files and a work directory, or a PPS directory and a work directory, or all three directories, depending on what level of data files you downloaded. The overall structure might look something like this:

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
You should run SAS tasks inside the work directory for the Obs ID you are working with. It is possible to run SAS tasks from any directory, but whichever directory you are in when you run a SAS task, that is where SAS will output any new files.

In some cases it is convenient to create a subdirectory within the work directory if the SAS tasks you are running will generate a very large number of output files. For example, if you are working with Optical Monitor data the file structure for the Obs ID you are working with may look like this:

├── 0400550201
│   ├── ODF
│   ├── PPS
│   ├── work
│   │   └── OM_files

8. Output Logging
The ObsID class accepts inputs to control output logging. The inputs (with defaults) to ObsID are:

obsid (required)
data_dir    = None
logfilename = None
tasklogdir  = None
output_to_terminal = True
output_to_file     = False
obsid is required and has to be the 10-digit observation ID number for the observation you are working with.
data_dir is the directory where you want the XMM data downloaded.
logfilename, if this is defined, then all output will be written to this file (but only if output_to_file=True). If no file name is given then the name of the log file will be 'ObsID_'+the Obs ID you are working with. Any SAS tasks run using basic_setup (i.e. cifbuild, odfingest, emproc, epproc, and rgsproc) will have their output written to their own file in the work_dir.
tasklogdir is the directory where output log files will be written. If not defined then it will use the data_dir for all top level Python related output, and work_dir for all other SAS tasks.
output_to_terminal, if True then output will be written to the terminal, if False then not.
output_to_file, if True then output will be written to a log file, if False then not.
If you are running an individual task, for example evselect, the MyTask object also accepts the same logging inputs as the ObsID class.

taskname (required)
inargs   (required)
logfilename = None, 
tasklogdir  = None,
output_to_terminal = True, 
output_to_file     = False
The difference is that logfilename will default to the task name, and tasklogdir will default to the current working directory (which should be the work_dir since that is where you will be running SAS tasks).


9. Extra Log Output from pySAS
SAS has its own verbosity that controls how much output is generated. If you change the verbosity for all of SAS it will also change the verbosity for pySAS accordingly. BUT, it is possible to set the verbosity for pySAS separately. pySAS has default configurations, and one of the options is pysas_verbosity. This is information specifically for pySAS, and not the individual SAS tasks you may be running. The levels of verbosity for pySAS are:

- CRITICAL : Similar to SAS verbosity of '1'
- ERROR    : Similar to SAS verbosity of '2' or '3'
- WARNING  : Similar to SAS verbosity of '4' or '5'
- INFO     : Similar to SAS verbosity of '6' or '7'
- DEBUG    : Similar to SAS verbosity of '8', '9', or '10'
The default verbosity is set to WARNING. You can set the verbosity for pySAS by using the command,

pysas.sas_cfg.set_setting_and_save('pysas_verbosity', value)
with the 'value' set to whatever level you need. Below we can see the difference it makes.

import pysas
obsid = '0079570201'
# Current default pySAS verbosity of 'WARNING'
pysas.sas_cfg.get_setting('pysas_verbosity')
# Output with the current pySAS verbosity
my_obs = pysas.ObsID(obsid)
my_obs.basic_setup(overwrite   = True,
                   run_epproc  = False,
                   run_emproc  = False,
                   run_rgsproc = False,
                   cifbuild_opts  = {'options':'-V 1'},
                   odfingest_opts = {'options':'-V 1'})
# Change the pySAS verbosity to 'INFO'
# This will only change the setting temporarily for this session.
# Once you restart the kernal it will return to the default value.
pysas.sas_cfg.set_setting('pysas_verbosity','INFO')
pysas.sas_cfg.get_setting('pysas_verbosity')
# Output with higher level of pySAS verbosity
my_obs = pysas.ObsID(obsid)
my_obs.basic_setup(overwrite   = True,
                   run_epproc  = False,
                   run_emproc  = False,
                   run_rgsproc = False,
                   cifbuild_opts  = {'options':'-V 1'},
                   odfingest_opts = {'options':'-V 1'})
If you want to change the default pySAS verbosity to INFO then uncomment the next line and run the cell. This will change the default in the configuration file.

#pysas.sas_cfg.set_setting_and_save('pysas_verbosity', 'INFO')

10. Calling SAS Tasks from the Command Line
Underneath what pySAS is doing is running SAS tasks as a Python subprocess. It calls each SAS task as if you were running the SAS command from the command line in a terminal. If you were to run SAS tasks from the command line this is what it would look like:

Calling a SAS task takes the general form:

task_name input1=value1 input2=value2 input3=value3 ...
For example, to call epproc with no inputs (which means using the default inputs):

epproc
Or to call epproc with a single input:

epproc withoutoftime=yes
A slightly more complex call using the command evselect with more inputs may look like:

evselect table=mos1.fits withimageset=yes imageset=image.fits xcolumn=X ycolumn=Y imagebinning=imageSize ximagesize=600 yimagesize=600
In the most extreme cases a very complex task call of evselect may look like this (all on one line at the command prompt):

Note: It is unusual to have this many inputs. This lists all possible inputs, including the defaults, for evselect.
evselect table='P0123700101M1S001MIEVLI0000.FTZ' keepfilteroutput='no' withfilteredset='no' filteredset='filtered.fits' destruct='yes' flagcolumn='EVFLAG' flagbit='-1' filtertype='expression' dssblock='' expression='true' writedss='yes' cleandss='no' updateexposure='yes' filterexposure='yes' blockstocopy='' attributestocopy='' energycolumn='PHA' withzcolumn='no' zcolumn='WEIGHT' withzerrorcolumn='no' zerrorcolumn='EWEIGHT' ignorelegallimits='no' withimageset='yes' imageset='image.fits' xcolumn='X' ycolumn='Y' imagebinning='imageSize' ximagebinsize='1' yimagebinsize='1' squarepixels='no' ximagesize='600' yimagesize='600' withxranges='no' ximagemin='1' ximagemax='640' withyranges='no' yimagemin='1' yimagemax='640' withimagedatatype='no' imagedatatype='Real64' withcelestialcenter='no' raimagecenter='0' decimagecenter='0' withspectrumset='no' spectrumset='spectrum.fits' spectralbinsize='5' withspecranges='no' specchannelmin='0' specchannelmax='11999' nonStandardSpec='no' withrateset='no' rateset='rate.fits' timecolumn='TIME' timebinsize='1' withtimeranges='no' timemin='0' timemax='1000' maketimecolumn='no' makeratecolumn='no' withhistogramset='no' histogramset='histo.fits' histogramcolumn='TIME' histogrambinsize='1' withhistoranges='no' histogrammin='0' histogrammax='1000'
There are several valid ways to format the inputs. For example, the following are all valid ways of including an input:

rgsproc withsrc=F
rgsproc withsrc=no
rgsproc withsrc='no'
rgsproc withsrc="no"
Some inputs require spaces. In that case the entire input value must be inside either 'single' or "double" quotes. For example:

rgsproc withsrc=no orders='1 2 3'
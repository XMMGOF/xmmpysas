Running 'basic_setup'
=====================

'download_ODF_data' inputs (with defaults):

            repo             = 'esa'
            data_dir         = None
            overwrite        = False
            proprietary      = False
            credentials_file = None
            encryption_key   = None

        'calibrate_odf' inputs (with defaults):
               
            obs_dir        = None
            sas_ccf        = None
            sas_odf        = None
            cifbuild_opts  = {}
            odfingest_opts = {}
            recalibrate    = False

        Input arguments for 'epproc', 'emproc', and 'rgsproc' can also be 
        passed in using 'epproc_args', 'emproc_args', or 'rgsproc_args' 
        respectively (or 'epchain_args' and 'emchain_args'). By defaut 
        'epproc', 'emproc', and 'rgsproc' will not rerun if output files 
        are found, but they can be forced to rerun by setting 'rerun=True' 
        as an input to 'basic_setup'.

        Examples for use:

            my_obs.basic_setup()

                - Uses the defaults.

            my_obs.basic_setup(repo='heasarc')

                - Uses the defaults, but downloads data from the HEASARC.

            my_obs.basic_setup(overwrite=True)

                - Will erase any previous data files for the Obs ID and 
                  download a fresh set of data files.

            my_obs.basic_setup(recalibrate=True)

                - Will rerun cifbuild and odfingest to generate new 
                  ccf.cif and \*SUM.SAS files.

            my_obs.basic_setup(rerun=True)

                - Will **not** download new files, but will rerun 'epproc',
                  'emproc', and 'rgsproc' and create new event lists.

            my_obs.basic_setup(repo='heasarc',
                               epproc_args=['withoutoftime=yes'])

                - Downloads data from the HEASARC and runs 'epproc' with the
                  'withoutoftime' option.

            my_obs.basic_setup(run_epchain=True,
                               run_emchain=True)

                - Will run 'epchain' and 'emchain' instead of 'epproc' and
                  'emproc'.

            my_obs.basic_setup(run_epproc=False,
                               run_emproc=False)

                - Will not run 'epproc' or 'emproc'. Will only run 'rgsproc'
                  by default.

            my_obs.basic_setup(run_epproc=False,
                               run_emproc=True,
                               run_rgsproc=False)

                - Will only run 'emproc', **not** 'epproc' or 'rgsproc'.

            my_obs.basic_setup(repo='heasarc',encryption_key='XXXXXXXXXXXXXXX')

                - Uses the defaults, but downloads *proprietary* data from 
                  the HEASARC. Must provide an encryption key, an alpha-numeric
                  string with 30 characters.

            my_obs.basic_setup(proprietary=True)

                - Uses the defaults, but downloads *proprietary* data from 
                  the XSA at ESA. Astroquery will ask for user's Cosmos
                  username and password.
.. _tophelpful:

===========================
Helpful Functions for pySAS
===========================

This page contains a collection of functions used in various pySAS tutorial 
notebooks. It is a reference of helpful functions that users can modify to use 
in creating their own pySAS analysis scripts. We include any additional imports 
needed to run that function beyond the standard pySAS imports:

.. code-block:: python

    import pysas
    from pysas import MyTask

--------
Plotting
--------

+++++++++++++++
Plot Event List
+++++++++++++++

Input is an event list. Optional filtering expression can be passed in. Uses 
``evselect`` to create a FITS image file. Plots the FITS image file. Color map 
limits can be set (``vmin`` and ``vmax``).

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    plt.style.use(astropy_mpl_style)

    def make_fits_image(event_list_file, 
                        image_file='image.fits', 
                        expression=None, 
                        vmin=1.0, 
                        vmax=1e2):
        
        inargs = {'table'        : event_list_file, 
                  'withimageset' : True,
                  'imageset'     : image_file, 
                  'xcolumn'      : 'X', 
                  'ycolumn'      : 'Y', 
                  'imagebinning' : 'imageSize', 
                  'ximagesize'   : 600, 
                  'yimagesize'   : 600}
        
        if expression != None:
            inargs['expression'] = expression

        MyTask('evselect', inargs).run()

        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)

        ax = plt.subplot(projection=wcs)
        plt.imshow(hdu.data, origin='lower', norm='log', vmin=vmin, vmax=vmax)
        ax.set_facecolor("black")
        plt.grid(color='blue', ls='solid')
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.colorbar()
        plt.show()

:ref:`Return to top <tophelpful>`

++++++++++++++++++++
Plot for Timing Mode
++++++++++++++++++++

Input is an event list. Optional filtering expression can be passed in. Uses 
``evselect`` to create a FITS image file. Plots the FITS image file. 

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    plt.style.use(astropy_mpl_style)

    def make_fits_image(event_list_file, 
                        image_file='image.fits', 
                        expression=None):
        
        inargs = {'table'         : event_list_file,
                  'withimageset'  : 'yes',
                  'imageset'      : image_file,
                  'xcolumn'       : 'RAWX',
                  'ycolumn'       : 'RAWY',
                  'imagebinning'  : 'binSize',
                  'ximagebinsize' : '1',
                  'yimagebinsize' : '1'}

        if expression != None:
            inargs['expression'] = expression
        
        MyTask('evselect', inargs, output_to_terminal = False).run()

        hdu = fits.open(image_file)[0]
        plt.imshow(hdu.data, origin='lower', norm='log')
        plt.colorbar()
        plt.show()

        return image_file

:ref:`Return to top <tophelpful>`

++++++++++++++++
Plot Light Curve
++++++++++++++++

Input is an event list. Optional filtering expression can be passed in. Uses 
``evselect`` to create a FITS light curve file. Plots the FITS light curve file.

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.table import Table
    plt.style.use(astropy_mpl_style)

    def plot_light_curve(event_list_file, 
                         light_curve_file='ltcrv.fits', 
                         expression=None):
                        
        inargs = {'table'          : event_list_file, 
                  'withrateset'    : 'yes', 
                  'rateset'        : light_curve_file, 
                  'maketimecolumn' : 'yes', 
                  'timecolumn'     : 'TIME', 
                  'timebinsize'    : '100', 
                  'makeratecolumn' : 'yes'}
        
        if expression != None:
            inargs['expression'] = expression

        MyTask('evselect', inargs).run()

        ts = Table.read(light_curve_file,hdu=1)
        plt.plot(ts['TIME'],ts['RATE'])
        plt.xlabel('Time (s)')
        plt.ylabel('Count Rate (ct/s)')
        plt.show()

:ref:`Return to top <tophelpful>`

++++++++++++++++++++++++++++++++++++
Plot Grouped Spectra and XSPEC Model
++++++++++++++++++++++++++++++++++++

Input is a grouped spectra object with arf, rmf, and background filenames 
already in the header.

.. code-block:: python

    # Imports needed
    import xspec
    from matplotlib.ticker import StrMethodFormatter
    import matplotlib.pyplot as plt

    def plot_data_model(spectrum,plot_file_name='data_model_plot.png'):

        xspec.Plot.device='/null'
        xspec.Plot.xAxis = 'keV'

        # Pull off data for main plot
        xspec.Plot('data')
        energy = xspec.Plot.x()
        counts = xspec.Plot.y()
        folded = xspec.Plot.model()
        xErrs = xspec.Plot.xErr()
        yErrs = xspec.Plot.yErr()

        # Pull off data for ratio plot
        xspec.Plot('ratio')
        ratio = xspec.Plot.y()
        r_xerror = xspec.Plot.xErr()
        r_yerror = xspec.Plot.yErr()

        # Get bin edges for "stairs" plot
        bin_edges = []
        for i in spectrum.energies: bin_edges.append(i[0])
        bin_edges.append(spectrum.energies[-1][1])

        # Make the figure and two subplots
        fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True, height_ratios=[2.5, 1],figsize=(9, 7))

        # Main plot
        ax0.errorbar(energy, counts, yerr=yErrs, xerr=xErrs, linestyle='', marker='')
        ax0.stairs(folded,bin_edges, color='r')
        ax0.set_xscale('log')
        ax0.set_yscale('log')
        ax0.set_xlim([bin_edges[0], bin_edges[-1]])
        ax0.tick_params(top=True,axis="x",direction="in",which='both')
        ax0.tick_params(axis="y",direction="in",which='both',right=True)
        ax0.set_ylabel('counts sec$^{-1}$ keV$^{-1}$')
        ax0.set_title('Data and Folded Model')

        # Ratio plot
        ax1.errorbar(energy, ratio, yerr=r_yerror, xerr=r_xerror, linestyle='', marker='')
        ax1.axhline(y=1, color='g')
        ax1.set_xscale('log')
        ax1.tick_params(top=True,axis="x",direction="in",which='both')
        ax1.tick_params(axis="y",direction="in",which='both')
        ax1.xaxis.set_major_formatter(StrMethodFormatter('{x:.1f}'))
        ax1.xaxis.set_minor_formatter(StrMethodFormatter('{x:.1f}'))
        ax1.set_xlabel('Energy (keV)')
        ax1.set_ylabel('Ratio')

        # This puts the plots together with no space in between
        plt.subplots_adjust(hspace=.0)

        # Save plot to file
        fig.savefig(plot_file_name)

        return fig, ax0, ax1

:ref:`Return to top <tophelpful>`

++++++++++++++++++++
Plot Zoomed in Image
++++++++++++++++++++

Input is an image file. By defualt it will zoom in on the center. Alternatively 
you can pass in the x, y coordinates (in pixels) where you want to zoom in.

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    plt.style.use(astropy_mpl_style)

    def plot_zoom_in(image_file, 
                     zoom=4, 
                     x=None, 
                     y=None, 
                     vmin=1.0, 
                     vmax=10.0):

        # Open file
        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)
        im_shape = hdu.shape
        if x is None:
            x_center = int(im_shape[0]/2)
        else:
            x_center = x
        if y is None:
            y_center = int(im_shape[1]/2)
        else:
            y_center = y
        
        # Define the zoomed-in region
        xmin, xmax = x_center-int(x_center/(2*zoom)), x_center+int(x_center/(2*zoom))
        ymin, ymax = y_center-int(y_center/(2*zoom)), y_center+int(y_center/(2*zoom))

        print((xmin, xmax))
        print((ymin, ymax))

        # Plot
        ax = plt.subplot(projection=wcs)
        plt.imshow(hdu.data, origin='lower', norm='log', vmin=vmin, vmax=vmax)
        ax.set_facecolor("black")
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        plt.grid(color='blue', ls='solid')
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.colorbar()
        plt.show()

:ref:`Return to top <tophelpful>`


++++++++++++++++++++++++++++++
Plot Single Region (Zoomed In)
++++++++++++++++++++++++++++++

Input is an event list, RA (in degrees), Dec (in degrees), and radius (in 
arcseconds). Plots a zoomed in image around the source region.

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    plt.style.use(astropy_mpl_style)

    def plot_region(image_file, 
                    ra, 
                    dec, 
                    radius, 
                    vmin=1.0, 
                    vmax=1000.0, 
                    zoom = 1.0):
        
        # Define region
        center = SkyCoord(ra, dec)
        region = CircleSkyRegion(center, radius)
        
        # Open file
        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)

        # Convert region to artist object
        pixel_region = region.to_pixel(wcs)
        artist = pixel_region.as_artist(color='lime')

        # Set image limits
        # This sets the bounds of the lower left (ll) and upper right (ur) of the plot.
        # NOTE: The calculation for the ll and ur of RA is reversed from the
        # calculation for the ll and ur of the DEC (+,- vs. -,+).
        # This preserves the correct orientation of the image.
        ra_ll  = ra+100*radius/zoom
        ra_ur  = ra-100*radius/zoom
        dec_ll = dec-100*radius/zoom
        dec_ur = dec+100*radius/zoom
        ra_lim  = [ra_ll.value, ra_ur.value]
        dec_lim = [dec_ll.value, dec_ur.value]
        # The third value "0" sets the "origin", or the index of the first pixel value.
        # It is "0" because Python starts counting at "0".
        (xmin, xmax), (ymin, ymax) = wcs.all_world2pix(ra_lim, dec_lim, 0)

        # Plot
        ax = plt.subplot(projection=wcs)
        plt.imshow(hdu.data, origin='lower', norm='log', vmin=vmin, vmax=vmax)
        ax.set_facecolor("black")
        ax.add_artist(artist)
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        plt.grid(color='blue', ls='solid')
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.colorbar()
        plt.show()

:ref:`Return to top <tophelpful>`

++++++++++++++++++++++++++++++++++++++++
Plot Multiple Regions from a Source List
++++++++++++++++++++++++++++++++++++++++

Inputs are a source list (``eml_list``) created using ``edetect_chain``, and the 
image file used to run ``edetect_chain``.

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from regions import CircleSkyRegion
    plt.style.use(astropy_mpl_style)

    def plot_regions(image_file, source_list):

        obs_regions = []
        with fits.open(source_list) as hdu:
            data = hdu[1].data[hdu[1].data['ID_BAND'] == 1]
        for i in range(len(data)):
            RA     = data['RA'][i] * u.deg
            Dec    = data['DEC'][i] * u.deg
            radius = 30.0 * u.arcsec
            obs_regions.append({'ra':RA, 'dec':Dec, 'radius':radius})

        # Open file
        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)

        # Plot
        ax = plt.subplot(projection=wcs)
        plt.imshow(hdu.data, origin='lower', norm='log', vmin=0.01, vmax=1.0)
        ax.set_facecolor("black")

        # Add regions
        for source in obs_regions:
            # Define region
            region = CircleSkyRegion(SkyCoord(source['ra'], source['dec']), source['radius'])
            pixel_region = region.to_pixel(wcs)
            # Convert region to artist object
            artist = pixel_region.as_artist(color='lime')
            ax.add_artist(artist)

        plt.grid(color='blue', ls='solid')
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.colorbar()
        plt.show()

:ref:`Return to top <tophelpful>`

Same as above, but split into two functions. To be used like this:

.. code-block:: python

    my_regions = make_regions(eml_list)
    plot_regions(image_file,my_regions)


.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from regions import CircleSkyRegion
    plt.style.use(astropy_mpl_style)

    # Function to make regions
    def make_regions(source_list):
        obs_regions = []
        with fits.open(source_list) as hdu:
            data = hdu[1].data[hdu[1].data['ID_BAND'] == 1]
        for i in range(len(data)):
            RA     = data['RA'][i] * u.deg
            Dec    = data['DEC'][i] * u.deg
            radius = 30.0 * u.arcsec
            obs_regions.append({'ra':RA, 'dec':Dec, 'radius':radius})
        return obs_regions

    def plot_regions(image_file, source_list):

        # Open file
        hdu = fits.open(image_file)[0]
        wcs = WCS(hdu.header)

        # Plot
        ax = plt.subplot(projection=wcs)
        plt.imshow(hdu.data, origin='lower', norm='log', vmin=0.01, vmax=1.0)
        ax.set_facecolor("black")

        # Add regions
        for source in source_list:
            # Define region
            region = CircleSkyRegion(SkyCoord(source['ra'], source['dec']), source['radius'])
            pixel_region = region.to_pixel(wcs)
            # Convert region to artist object
            artist = pixel_region.as_artist(color='lime')
            ax.add_artist(artist)

        plt.grid(color='blue', ls='solid')
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.colorbar()
        plt.show()

:ref:`Return to top <tophelpful>`

---------
Filtering
---------

++++++++++++++
Apply a Filter
++++++++++++++

Input is an event list, and the max and min energy values for the filter.

.. code-block:: python

    # Imports needed
    from astropy.io import fits

    def filter_event_list(in_event_list,
                          pi_min,
                          pi_max,
                          filtered_event_list):

        with fits.open(in_event_list) as hdu:
            instrument = hdu[0].header['INSTRUME']

        if instrument == 'EPN':
            filter = 'XMMEA_EP'
            pattern = 4
        elif 'EMOS' in instrument:
            filter = 'XMMEA_EM'
            pattern = 12

        # Filter expression
        expression = '(PATTERN in [0:{pattern}])&&(PI in [{pi_min}:{pi_max}])&&(FLAG == 0)&&#{filter}'.format(filter=filter,pattern=pattern,pi_min=pi_min,pi_max=pi_max)

        inargs = {'table'           : in_event_list, 
                  'withfilteredset' : 'yes', 
                  'expression'      : expression, 
                  'filteredset'     : filtered_event_list, 
                  'filtertype'      : 'expression', 
                  'keepfilteroutput': 'yes', 
                  'updateexposure'  : 'yes', 
                  'filterexposure'  : 'yes'}
        
        MyTask('evselect', inargs).run()

:ref:`Return to top <tophelpful>`


++++++++++++++++++++++++++++++++++++
Make High Resolution FITS Image File
++++++++++++++++++++++++++++++++++++

Input is an event list, and the max and min energy values for the filter.

.. code-block:: python

    def make_hires_image(in_event_list,
                         pi_min,
                         pi_max,
                         out_image='image.fits'):

        # Filter expression
        expression = '(PI in [{pi_min}:{pi_max}])'.format(pi_min=pi_min,pi_max=pi_max)

        inargs = {'table'         : in_event_list+':EVENTS', 
                  'withimageset'  : 'yes',
                  'expression'    : expression, 
                  'imageset'      : out_image,
                  'imagebinning'  : 'binSize',
                  'xcolumn'       : 'X',
                  'ycolumn'       : 'Y',
                  'ximagebinsize' : 40,
                  'yimagebinsize' : 40}
        
        MyTask('evselect', inargs).run()

        return out_image

:ref:`Return to top <tophelpful>`

++++++++++++++++++
Filtering a Region
++++++++++++++++++

Input is an event list, RA (in degrees), Dec (in degrees), and radius (in 
arcseconds). Filters the event list for the given region. Can do a circle or an 
annulus.

.. code-block:: python

    # Imports needed
    import astropy.units as u

    def filter_region(input_event_list,
                      output_event_list,
                      RA,
                      Dec,
                      radius,
                      type='circle'):

        if type == 'circle':
            expression = "'((RA,DEC) in CIRCLE({0},{1},{2}))'".format(RA.value,Dec.value,radius.to(u.deg).value)
        if type == 'annulus':
            expression = "'((RA,DEC) in ANNULUS({0},{1},{2},{3}))'".format(RA.value,Dec.value,radius[0].to(u.deg).value,radius[1].to(u.deg).value)

        inargs = {'table'            : input_event_list,
                  'withfilteredset'  : 'yes',
                  'filteredset'      : output_event_list,
                  'keepfilteroutput' : 'yes',
                  'filtertype'       : 'expression',
                  'expression'       : expression}
        
        MyTask('evselect', inargs).run()

:ref:`Return to top <tophelpful>`

++++++++++++++++++++++++++++
Automatic Spectra Extraction
++++++++++++++++++++++++++++

Below we provide an example function that can be used to automatically extract 
spectra from all sources, along with background regions. As inputs it takes a 
filtered event list and the source list generated by ``edetect_chain``. The 
outputs will be a corresponding source event list, background event list, source 
spectrum, background spectrum, RMF, ARF, and binned spectrum file for each 
source. The files for each source will start with ‘MMMsXXX’ where MMM is the 
instrument and XXX is the source number.

**Note**: This will generate spectra from duplicate sources. The size of the 
region used for source extraction uses a default value, along with the size of 
the background region. There are a few other default assumptions that may or may 
not be appropriate depending on the individual sources.

.. code-block:: python

    # Imports needed
    import matplotlib.pyplot as plt
    from astropy.visualization import astropy_mpl_style
    from astropy.io import fits
    from astropy.wcs import WCS
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from regions import CircleSkyRegion

    def extract_spectra_from_source(filtered_event_list,eml_list_file):

        with fits.open(eml_list_file) as hdu:
            instrument = hdu[0].header['INSTRUME']
            data = hdu[1].data[hdu[1].data['ID_BAND'] == 1]
        if instrument == 'EPN':
            specchannelmax = 20479
        elif 'EMOS' in instrument:
            specchannelmax = 11999
        for i in range(len(data)):
            # File names
            source_event_list = instrument+'s{:03}_event_list.fits'.format(i)
            bkg_event_list    = instrument+'s{:03}_bkg_event_list.fits'.format(i)
            source_spectra    = instrument+'s{:03}_spectra.fits'.format(i)
            bkg_spectra       = instrument+'s{:03}_bkg_spectra.fits'.format(i)
            rmf_file          = instrument+'s{:03}_rmf.fits'.format(i)
            arf_file          = instrument+'s{:03}_arf.fits'.format(i)
            grouped_spectra   = instrument+'s{:03}_spectra_grouped.fits'.format(i)

            # Add source region and background annulus
            RA      = data['RA'][i] * u.deg
            Dec     = data['DEC'][i] * u.deg
            radiusi = 10.0 * u.arcsec
            radiuso = 20.0 * u.arcsec
            circle  = "CIRCLE({0},{1},{2})".format(RA.value,Dec.value,radiusi.to(u.deg).value)
            annulus = "ANNULUS({0},{1},{2},{3})".format(RA.value,Dec.value,radiusi.to(u.deg).value,radiuso.to(u.deg).value)

            # Extract spectrum from source
            inargs = {'table'           : filtered_event_list,
                      'energycolumn'    : 'PI',
                      'withfilteredset' : 'yes',
                      'filteredset'     : source_event_list,
                      'keepfilteroutput': 'yes',
                      'filtertype'      : 'expression',
                      'expression'      : "'((RA,DEC) in {0})".format(circle),
                      'withspectrumset' : 'yes',
                      'spectrumset'     : source_spectra,
                      'spectralbinsize' : '5',
                      'withspecranges'  : 'yes',
                      'specchannelmin'  : '0',
                      'specchannelmax'  : specchannelmax}
            
            MyTask('evselect', inargs).run()

            # Extract spectrum from background
            inargs = {'table'           : filtered_event_list,
                      'energycolumn'    : 'PI',
                      'withfilteredset' : 'yes',
                      'filteredset'     : bkg_event_list,
                      'keepfilteroutput': 'yes',
                      'filtertype'      : 'expression',
                      'expression'      : "'((RA,DEC) in {0})'".format(annulus),
                      'withspectrumset' : 'yes',
                      'spectrumset'     : bkg_spectra,
                      'spectralbinsize' : '5',
                      'withspecranges'  : 'yes',
                      'specchannelmin'  : '0',
                      'specchannelmax'  : specchannelmax}
            
            MyTask('evselect', inargs).run()

            # Generate rmf for source
            inargs = {'rmfset'      : rmf_file,
                      'spectrumset' : source_spectra}
            
            MyTask('rmfgen', inargs).run()

            # Generate arf for source
            inargs = {'arfset'         : arf_file,
                      'spectrumset'    : source_spectra,
                      'withrmfset'     : 'yes',
                      'rmfset'         : rmf_file,
                      'withbadpixcorr' : 'yes',
                      'badpixlocation' : filtered_event_list,
                      'setbackscale'   : 'yes'}
            
            MyTask('arfgen', inargs).run()

            # Bin events in spectrum and link arf and rmf
            inargs = {'spectrumset' : source_spectra,
                      'groupedset'  : grouped_spectra,
                      'arfset'      : arf_file,
                      'rmfset'      : rmf_file,
                      'backgndset'  : bkg_spectra,
                      'mincounts'   : '30'}
            
            MyTask('specgroup', inargs).run()

:ref:`Return to top <tophelpful>`

Document last updated: |date|

.. |date| date:: %Y-%m-%d
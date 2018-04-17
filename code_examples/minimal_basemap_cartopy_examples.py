import numpy as np
import matplotlib.pyplot as pl
import netCDF4 as nc4

from mpl_toolkits.basemap import Basemap

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

pl.close('all'); pl.ion()

# Dummy data
lon,lat = np.meshgrid(np.linspace(-9,19,128),np.linspace(43,60,128))
ts = np.cos(lon/4) + np.sin(lat)

if (True):
    # ---------------------------------
    # Plot without any projection
    # ---------------------------------

    pl.figure(figsize=(8,6))
    pl.pcolormesh(lon, lat, ts, cmap=pl.cm.nipy_spectral)

if (True):
    # ---------------------------------
    # Basemap example
    # ---------------------------------

    pl.figure(figsize=(8,6))

    # Setup Basemap
    m = Basemap(width=2200000,height=2200000,
                rsphere=(6378137.00,6356752.3142),\
                resolution='l', area_thresh=10., projection='lcc',\
                lat_0=51.967, lon_0=4.9)

    # Option one (specify latlon=True)
    m.pcolormesh(lon, lat, ts, latlon=True, cmap=pl.cm.nipy_spectral)

    # Option two (do manual coordinate transform)
    x, y = m(lon, lat)
    pl.pcolormesh(x, y, ts, cmap=pl.cm.nipy_spectral)

    m.drawparallels(np.arange(-80.,81.,5.), linewidth=0.5)
    m.drawmeridians(np.arange(-180.,181.,5.), linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)
    m.drawcountries(linewidth=0.5)

if (True):
    # ---------------------------------
    # Cartopy example
    # ---------------------------------

    def add_feature(name, category, color='k', linewidth=1, scale='10m'):
        ax = pl.gca()
        feature = cfeature.NaturalEarthFeature(
            category=category, name=name, scale=scale, facecolor='none')
        ax.add_feature(feature, edgecolor=color, linewidth=linewidth)

    pl.figure(figsize=(8,6))

    # Create axes object in Lambert projection
    lcc = ccrs.LambertConformal(central_longitude=4.9, central_latitude=51.967, standard_parallels=(52.5,52.5))
    ax = pl.axes(projection=ccrs.LambertConformal(central_longitude=4.9, central_latitude=51.967))

    #add_feature('admin_1_states_provinces_scale_rank', 'cultural', linewidth=0.5, color='k')
    #add_feature('roads', 'cultural', color='0.3', linewidth=0.5)
    add_feature('lakes', 'physical', linewidth=0.5)
    add_feature('coastline', 'physical', linewidth=0.5)
    add_feature('admin_0_boundary_lines_land', 'cultural', linewidth=0.5)

    pl.pcolormesh(lon, lat, ts, cmap=pl.cm.nipy_spectral, transform=ccrs.PlateCarree())

    ax.set_extent([-9, 19, 41, 61])

    ax.gridlines(linestyle='--', linewidth=0.5, color='k')

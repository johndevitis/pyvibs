import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm



def plot_interp(coords, shape, bcoords, xres=50, yres=50, projections=True):
    """
    plot interpolated 3d surface based on vertical modal amplitude.
    optoinal add of contoured projections on the axes limits as well
    """

    coords = np.append(coords,bcoords, axis=0)
    shape = np.append(shape, np.zeros(bcoords.shape[0]))

    X = np.linspace(min(coords[:,0]), max(coords[:,0]), xres)
    Y = np.linspace(min(coords[:,1]), max(coords[:,1]), yres)

    X,Y = np.meshgrid(X, Y)

    Z = griddata(coords[:,:2], shape, (X,Y), method='cubic')


    fig = plt.figure(figsize=(12,6))
    C = cm.terrain

    ax = fig.gca(projection='3d')

    xx = np.min(X), np.max(X)
    yy = np.min(Y), np.max(Y)
    zz = np.nanmin(Z), np.nanmax(Z)

    # plot trisurf
    if False:
        ax.plot_trisurf(X.flatten(),Y.flatten(),Z.flatten(), antialiased=True,
                        linewidth=0,vmin=zz[0], vmax=zz[1], shade=False, cmap=C)

    # plot wireframe
    if False: ax.plot_wireframe(X,Y,Z, alpha=0.33)

    # plot projects
    if projections:
        ax.contourf(X, Y, Z, zdir='x', offset=xx[0], alpha=0.2, cmap=C)
        ax.contourf(X, Y, Z, zdir='y', offset=yy[1], alpha=0.2, cmap=C)
        ax.contourf(X, Y, Z, zdir='z', offset=zz[0], alpha=0.6, cmap=C)

    ax.plot(coords[:,0],coords[:,1],np.ones_like(shape)*zz[0],
            linestyle='none', marker='x')


    if True:
        ax.plot_surface(X, Y, Z,
                    rstride=1,
                    cstride=1,
                    alpha=0.4,
                    antialiased=False,
                    shade=False,
                    zorder=10,
                    color='slateblue',
                    linewidth=0)


    ax.set_xlabel('Longitudinal Dimension, X')
    ax.set_xlim3d(*xx)
    ax.set_ylabel('Transverse Dimension, Y')
    ax.set_ylim3d(*yy)
    ax.set_zlabel('Vertical Dimension, Z')
    ax.set_zlim3d(*zz)

    return fig

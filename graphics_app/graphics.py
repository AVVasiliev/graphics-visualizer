import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import sys
import os
import uuid
from graphics_app import IMAGES_FOLDER

COLORMAP = {
    "hot": cm.hot,
    "inferno": cm.inferno,
    "rainbow": cm.rainbow
}


def create_3d_graphic(filename, colormap=cm.hot):
    file = open(filename, 'r')
    x = list()
    y = list()
    z = list()
    n = 0
    for line in file:
        xx, yy, zz = line.split()
        x.append(float(xx))
        y.append(float(yy))
        z.append(float(zz))
        n = n+1
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(x, y, z, cmap=colormap)
    image_name = '{}.png'.format(str(uuid.uuid4()))
    image_path = os.path.join(IMAGES_FOLDER, image_name)
    plt.savefig(image_path)
    return image_name, image_path

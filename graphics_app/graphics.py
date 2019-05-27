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
    file_id = str(uuid.uuid4())
    image_path_png = os.path.join(IMAGES_FOLDER, 'png', '{}.png'.format(file_id))
    image_path_pdf = os.path.join(IMAGES_FOLDER, 'pdf', '{}.pdf'.format(file_id))
    image_path_eps = os.path.join(IMAGES_FOLDER, 'eps', '{}.eps'.format(file_id))
    plt.savefig(image_path_png)
    plt.savefig(image_path_eps, format='eps', dpi=1000)
    plt.savefig(image_path_pdf, format='pdf', dpi=1000)

    return '{}.png'.format(file_id), image_path_png

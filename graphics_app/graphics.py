import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from scipy import interpolate
import sys
import os
import uuid
from graphics_app import IMAGES_FOLDER
from graphics_app.utils import transpose

COLORMAP = {
    "hot":      cm.hot,
    "inferno":  cm.inferno,
    "rainbow":  cm.rainbow,
    "viridis":  cm.viridis,
    "plasma":   cm.plasma,
    "magma":    cm.magma,
    "cividis":  cm.cividis
}

COLORM2D = {
    "blue":     "b",
    "green":    "g",
    "red":      "r",
    "cyan":     "c",
    "magenta":  "m",
    "yellow":   "y",
    "black":    "k",
    "white":    "w"
}

PICT_TYPES = {
    "2D": "2D",
    "3D": "3D",
    "2D with colors": "2D with colors"
}

RESOLUTION = {
    "300 dpi": 300,
    "600 dpi": 600,
    "1200 dpi": 1200
}

COLUMN_NAMES = [
    {'name': 'x', 'checked': True},
    {'name': 'y', 'checked': True}
]
for i in range(1, 20):
    COLUMN_NAMES.append({'name': f"f{i}", 'checked': False})


def create_3d_graphic(filename, colormap=cm.hot, dpi="300 dpi"):
    dpi_value = RESOLUTION[dpi]
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
    plt.savefig(image_path_eps, format='eps', dpi=dpi_value)
    plt.savefig(image_path_pdf, format='pdf', dpi=dpi_value)
    plt.clf()
    return file_id, image_path_png


def create_2d_graphic(data,  active_column, dpi="300 dpi", color2d="b", grid2d=False):
    dpi_value = RESOLUTION[dpi]
    data_transpose = transpose(data)
    print(data_transpose)
    x = data_transpose[0]
    for i in range(1, len(data_transpose)):
        if active_column[i]['checked']:
            plt.plot(x, data_transpose[i], color=color2d)
    plt.grid(grid2d)
    file_id = str(uuid.uuid4())
    image_path_png = os.path.join(IMAGES_FOLDER, 'png', '{}.png'.format(file_id))
    image_path_pdf = os.path.join(IMAGES_FOLDER, 'pdf', '{}.pdf'.format(file_id))
    image_path_eps = os.path.join(IMAGES_FOLDER, 'eps', '{}.eps'.format(file_id))
    plt.savefig(image_path_png)
    plt.savefig(image_path_eps, format='eps', dpi=dpi_value)
    plt.savefig(image_path_pdf, format='pdf', dpi=dpi_value)
    plt.clf()

    return file_id, image_path_png


def create_2d_contour(filename, dpi="300 dpi"):
    dpi_value = RESOLUTION[dpi]
    x, y, z = np.genfromtxt(filename, unpack=True)
    N = 100
    xi = np.linspace(x.min(), x.max(), N)
    yi = np.linspace(y.min(), y.max(), N)
    zi = interpolate.griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')

    fig = plt.figure()
    plt.contour(xi, yi, zi)
    plt.xlabel("X")
    plt.ylabel("Y")
    file_id = str(uuid.uuid4())
    image_path_png = os.path.join(IMAGES_FOLDER, 'png', '{}.png'.format(file_id))
    image_path_pdf = os.path.join(IMAGES_FOLDER, 'pdf', '{}.pdf'.format(file_id))
    image_path_eps = os.path.join(IMAGES_FOLDER, 'eps', '{}.eps'.format(file_id))
    plt.savefig(image_path_png)
    plt.savefig(image_path_eps, format='eps', dpi=dpi_value)
    plt.savefig(image_path_pdf, format='pdf', dpi=dpi_value)
    plt.clf()
    return file_id, image_path_png

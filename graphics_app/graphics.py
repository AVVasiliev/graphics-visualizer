import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from scipy import interpolate
import os
import uuid
from graphics_app import IMAGES_FOLDER

COLORMAP = {
    "hot":      cm.hot,
    "inferno":  cm.inferno,
    "rainbow":  cm.rainbow,
    "viridis":  cm.viridis,
    "plasma":   cm.plasma,
    "magma":    cm.magma,
    "cividis":  cm.cividis
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


def create_3d_graphic(data, colormap=cm.hot, dpi="300 dpi"):
    dpi_value = RESOLUTION[dpi]
    data_transpose = np.transpose(data)
    x = data_transpose[0]
    y = data_transpose[1]
    z = data_transpose[2]
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


def create_2d_graphic(data,  active_column, dpi="300 dpi", grid2d=False):
    dpi_value = RESOLUTION[dpi]
    data_transpose = np.transpose(data)
    x = data_transpose[0]
    for i in range(1, len(data_transpose)):
        if active_column[i]['checked']:
            plt.plot(x, data_transpose[i])
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


def create_2d_contour(data, dpi="300 dpi"):
    dpi_value = RESOLUTION[dpi]
    data_transpose = np.transpose(data)
    x = data_transpose[0]
    y = data_transpose[1]
    z = data_transpose[2]
    N = 100
    xi = np.linspace(x.min(), x.max(), N)
    yi = np.linspace(y.min(), y.max(), N)
    zi = interpolate.griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')

    plt.figure()
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

import numpy as np

from IPython.display import HTML
import trimesh
import k3d

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm


def show_mesh(vertices, faces, width=500, height=500):
    new_mesh = trimesh.base.Trimesh(vertices, faces, process=False)
    new_mesh.fix_normals()
    mesh_html = new_mesh.show(height=height).data
    # <--- trimesh developpers had an alternative hand attachment points
    #  specify plot width
    mesh_html = mesh_html.replace('width="100%"', f'width="{width}px"', 1)
    #  fix broken aspect ratio
    mesh_html = mesh_html.replace('render();window.addEventListener', 'camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();renderer.setSize(window.innerWidth,window.innerHeight);controls.handleResize();render();window.addEventListener')
    #  auto fit viewport to object
    mesh_html = mesh_html.replace('render();window.addEventListener', 'autoFit(scene,camera,controls);render();window.addEventListener')
    #  make zooming more responsive
    mesh_html = mesh_html.replace('zoomSpeed=1.2', 'zoomSpeed=5')
    
    return HTML(mesh_html)


def get_colors(value, cmap):
    hex_colors = []
    norm = mpl.colors.Normalize(vmin=value.min(), vmax=value.max())
    cmap = cmap
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    for i in value:
#         hex_colors.append(m.to_rgba(i))
        hex_colors.append(int(mpl.colors.to_hex(m.to_rgba(i)).replace('#','0x'),16))
    hex_colors = np.array(hex_colors, 'uint32')
    return(hex_colors)

def show_points(points, colors=[], normals=None, point_size=0.1, line_width=0.00001):
    plot = k3d.plot(grid_visible=False, axes_helper=0)
    if normals is not None:
        normal_vectors = k3d.vectors(points, normals, line_width=line_width, use_head=False)
        plot += normal_vectors
    point_cloud = k3d.points(points, colors=colors, point_size=point_size, shader='flat')
    plot += point_cloud
    plot.display()
    return None
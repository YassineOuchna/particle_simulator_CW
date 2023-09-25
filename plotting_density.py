import matplotlib.pyplot as plt
import matplotlib

fig = plt.figure()


def plotting(X, t, geo):
    plt.clf()
    plt.plot(X, t)
    plt.pause(1/300)
    plt.ioff()


def move_figure(f, loc_x, loc_y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (loc_x, loc_y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((loc_x, loc_y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move((loc_x, loc_y))

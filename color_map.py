import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt


data1 = np.random.random((4,4))
attempt= {'red':
                ((0.0,  1, 1),\
                (0.5, 0.9, 0.9),\
                (0.75, 0.8, 0.8),\
                (0.95, 1.0, 1.0),\
                (1.0, 1, 1.0)),\
        'green':\
                ((0.0, 1, 1),\
                (0.5, 0.8, 0.8),\
                   (0.75, 0.1, 0.1),
                   (0.95, 0.1,0.1),
                   (1.0, 0,0)),
         'blue':  ((0.0, 1, 1),
                   (0.5, 0.8, 0.8),
                   (0.75, 0.1, 0.1),
                   (0.95, 0.1,0.1),
                   (1.0, 0.0, 0.0)),
        'alpha': ((0.0, 0, 0),
                   (0.3,0.1, 0.1),
                    (0.75,0.2, 0.2),
                   (0.95,0.3, 0.3),
                    (1.0, 1, 1)),
          }
mia = LinearSegmentedColormap('mia', attempt)
plt.register_cmap(cmap=mia)
plt.pcolormesh(data1, cmap=mia)
plt.colorbar()

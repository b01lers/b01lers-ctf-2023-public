#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from SECRET import FLAG

class Yarn:
    def __init__(self, ply):
        self.ply = ply
        self.n_dims = 2
        self.n_winds = 1 << (self.n_dims * ply)

    def fold(self, dot):
        x = 0
        y = 0
        take_up = dot
        skein = 1
        while skein < (1 << (self.ply)):
            block_x = 1 & (take_up // 2)
            block_y = 1 & (take_up ^ block_x)
            x, y = self.twist(x, y, block_x, block_y, skein)
            x += skein * block_x
            y += skein * block_y
            take_up = take_up // 4
            skein *= 2
        return (x, y)

    def twist(self, x, y, block_x, block_y, n_twists):
        if block_y == 0:
            if block_x == 1:
                x, y = self.flip(x, y, n_twists)

            cross = x
            x = y
            criss = cross
            y = criss
        return (x, y)

    def flip(self, x, y, n_twists):
        return ((n_twists-1) - x, (n_twists-1) - y)

    def hash_to_curve(self, msg):
        msgl = bytes_to_long(bytes(msg, 'ascii'))
        enc_msg = msgl % self.n_winds
        return self.fold(dot=enc_msg)

    def render_fabric(self, dot=None):
        # Plot all possible values of (x,y)
        dots = np.zeros((self.n_winds, 2), dtype='uint')
        cmap = matplotlib.cm.get_cmap('coolwarm')
        for d in range(self.n_winds):
            (x, y) = self.fold(dot=d)
            dots[d][0] = x
            dots[d][1] = y

        # dash-dot style, with (x,y) = (0,0) at lower-left of plot (default)
        for d in range(self.n_winds-1):
            plt.plot([dots[d,0], dots[d+1,0]], [dots[d,1], dots[d+1,1]], '.-', color=cmap(d/self.n_winds))

        title = '%d-ply fabric' % self.ply + ('' if dot is None else ' with dot d=%d at (x,y)=(%d,%d)' % (dot, dots[dot][0], dots[dot][1]))
        # Highlight the dot if specified
        if dot is not None:
            plt.plot(dots[dot][0], dots[dot][1], color='black', markersize=6, marker='o')
        plt.title(title)
        plt.xlabel('x_dim')
        plt.ylabel('y_dim')
        plt.show()


if __name__ == "__main__":
    curve = Yarn(ply=112)
    x, y = curve.hash_to_curve(FLAG)
    print("H(FLAG) = (%d, %d)" % (x,y))

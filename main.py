import cv2 as cv
import numpy as np
from utils import signal as us
from utils import shapes as yo
from matplotlib import pyplot as plt

def norm(this):
    """ Squeeze to 0-1 """
    this -= this.min()
    this /= this.max()
    return this

def funky_image(XX, YY, tick):
    """ Generate some funk """
    timeshift = 0.3 + 0.3 * np.sin(7.*tick/500)
    phi = np.pi * 2 * tick/2500.0
    the = np.pi * 2 * tick/1250.0
    r_shift = 2 + 1.5 * np.cos(the)
    ax_shift = r_shift * np.cos(phi)
    ay_shift = r_shift * np.sin(phi)

    a_hahn = yo.Hahn(k = 11, r = 33)
    a_hahn.set_x_shift(ax_shift)
    a_hahn.set_y_shift(ay_shift)
    Za = a_hahn.get(XX, YY, tick)

    bx_shift = 2. * np.cos(phi - np.pi)
    by_shift = 2. * np.sin(phi - np.pi)

    b_hahn = yo.Hahn(k = 5)
    b_hahn.set_x_shift(bx_shift)
    b_hahn.set_y_shift(by_shift)
    Zb = b_hahn.get(XX, YY, tick)

    cx_shift = 2. * np.cos(phi - np.pi/2)
    cy_shift = 2. * np.sin(phi - np.pi/2)

    c_hahn = yo.Hahn(k = 2)
    c_hahn.set_x_shift(cx_shift)
    c_hahn.set_y_shift(cy_shift)
    Zc = c_hahn.get(XX, YY, tick)

    Z = 3 * norm(Za) + \
            norm(Zb) * 1.5 * (1 + 0.5 * np.cos(phi - np.pi/2)) + \
            norm(Zc) * 2 * np.cos(phi) ** 2

    # le normalizatione
    Z -= Z.min()
    Z /= Z.max()
    Z *= 256.

    # OpenCV likes uint8
    return np.uint8(Z)

def main():
    """ blurp """
    # blompf notes sample PITCH | START | DURATION | VOLUME
    notes = [[45, 0, 8, 70],
             [43, 8, 16, 69],
             [43, 24, 8, 70],
             [47, 32, 4, 70],
             [52, 36, 4, 69],
             [55, 40, 2, 69],
             [59, 42, 2, 67],
             [64, 44, 4, 69]]

    if False:
        x_res = 1080
        y_res = 720
    else:
        x_res = 540
        y_res = 540

    for tick in range(500):
        print tick

        xspan = 4.5 + np.cos(8.0 * tick/100)
        yspan = 4.5 + np.sin(8.0 * tick/100)
        x = np.linspace(-xspan, xspan, x_res)
        y = np.linspace(-yspan, yspan, y_res)
        XX, YY = np.meshgrid(x, y)

        ZZ = funky_image(XX, YY, 5*tick)
        filename = 'imgs/{}.png'.format(1e7 + tick)
        img = cv.applyColorMap(ZZ, cv.COLORMAP_OCEAN)
        cv.imwrite(filename, img)

if __name__ == '__main__':
    main()

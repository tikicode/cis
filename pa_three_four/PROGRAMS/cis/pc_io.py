import pandas as pd
import numpy as np


def import_rigid_body(fName):
    """Method for importing rigid body design data

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    np.ndarray
         Point clouds representing the xyz coordinates of the marker LEDs in body coordinates and the xyz coordinates
         of the tip in body coordinates
    """
    headers = pd.read_csv(fName, header=None, names=["Nm", np.nan], nrows=1)
    # number of headers
    Nm = int(headers["Nm"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    marker_leds = np.array(text[["xi", "yi", "zi"]][:Nm])
    tip_in_body = np.array(text[["xi", "yi", "zi"]][Nm:])
    return marker_leds, tip_in_body


def import_surface_mesh(fName):
    """Method for importing body surface definition data

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    np.ndarray
         Point clouds representing the xyz coordinates of vertices in CT coordinates and the xyz coordinates of the

    """
    headers = pd.read_csv(fName, header=None, names=["Nv", np.nan], nrows=1)
    # number of vertices
    Nv = int(headers["Nv"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1, nrows=Nv)
    ct_vertices = np.array(text[["xi", "yi", "zi"]][:])
    headers = pd.read_csv(fName, header=None, names=["Nt", np.nan], skiprows=Nv + 1, nrows=1)
    Nt = int(headers["Nt"][0])
    text = pd.read_csv(fName, header=None, names=["i1", "i2", "i3", "n1", "n2", "n3"], skiprows=Nv + 2, nrows=Nt)
    triangles = np.array(text[["i1", "i2", "i3", "n1", "n2", "n3"]][:])
    return ct_vertices, triangles, Nv


def import_sample_readings(fName, Na, Nb):
    """Method for importing sample readings

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    np.ndarray
         Point clouds representing frames of xyz coordinates of A body LED markers, B body LED markers, and D
         (unneeded) body LED markers
    """
    headers = pd.read_csv(fName, header=None, names=["Ns", "Nsamps", np.nan], nrows=1)
    # number of leds and samples
    Ns = int(headers["Ns"][0])
    Nsamps = int(headers["Nsamps"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    A_readings, B_readings, D_readings = [], [], []
    for i in range(Nsamps):
        A_readings.append(np.array(text[["xi", "yi", "zi"]][i * Ns: Na + i * Ns]))
        B_readings.append(np.array(text[["xi", "yi", "zi"]][Na + i * Ns: Na + Nb + i * Ns]))
        D_readings.append(np.array(text[["xi", "yi", "zi"]][Na + Nb + i * Ns: Na + Nb + Ns + i * Ns]))
    return A_readings, B_readings, D_readings


def output_pa34(output_dir, name, cs, ds, mag_dif, samples):
    """Method for outputting PA34 data

    Parameters
    _________
    output_dir : str
        The directory to output the data
    name : str
        The name of the data output file
    cs : np.ndarray
        The xyz coordinates on the surface mesh found from F_reg * d_k
    ds : np.ndarray
        The xyz coordinates of the tip with respect to rigid body B
    mag_dif : np.ndarray
        The magnitude of the difference between the tip in CT coordinates and the tip in DCS coordinates
    """

    f = open(f"{output_dir}/{name}-output.txt", 'w')
    f.write('{0} {1}\n'.format(samples, name + "-output-1.txt"))
    for n in range(samples):
        f.write('  {0}   {1}   {2}        {3}   {4}   {5}     {6}\n'.format(format(ds[n][0], '.2f'),
                                                                            format(ds[n][1], '.2f'),
                                                                            format(ds[n][2], '.2f'),
                                                                            format(cs[n][0], '.2f'),
                                                                            format(cs[n][1], '.2f'),
                                                                            format(cs[n][2], '.2f'),
                                                                            format(mag_dif[n], '.2f')))
    f.close()
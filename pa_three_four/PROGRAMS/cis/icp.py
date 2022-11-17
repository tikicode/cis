import numpy as np

from .registration import registration
from .frame import Frame


def find_rigid_body_pose(a_frames, b_frames, a_tip, a_leds, b_leds):
    """
    Method for finding the rigid body pose

    Parameters
    _________
    a_frames : np.ndarray
        The xyz coordinates of A body LED markers in tracker coordinates
    b_frames : np.ndarray
        The xyz coordinates of B body LED markers in tracker coordinates
    a_tip : np.ndarray
        The xyz coordinates of the tip in tracker coordinates
    a_leds : np.ndarray
        The xyz coordinates of A body LED markers in body coordinates
    b_leds : np.ndarray
        The xyz coordinates of B body LED markers in body coordinates

    Returns
    _________
    np.ndarray
        The xyz coordinates of the pointer tip with respect to rigid body B
    """

    # find the number of frames
    Nf = len(a_frames)

    # initialize the array to store the tip coordinates
    d_k_cloud = np.zeros((Nf, 3))
    # loop through the frames
    for i in range(Nf):
        # find the rigid body poses
        F_ak = registration(a_leds, a_frames[i])
        F_bk = registration(b_leds, b_frames[i])
        # calculate the pointer tip location
        d_k = Frame.compose_transform(F_bk.invert(), Frame.compose_transform(F_ak, a_tip))
        d_k_cloud[i] = d_k

    return d_k_cloud


def find_sample_points(F_reg, d_k):
    """
    Method for finding sample points to match to the surface mesh

    Parameters
    _________
    F_reg : Frame
        Transformation of the surface mesh from the pointer tip
    d_k : np.ndarray
        The xyz coordinates of the tip with respect to rigid body B

    Returns
    _________
    np.ndarray
        The xyz coordinates of sample points estimated to be on the surface mesh
    """
    d_k = d_k.reshape(1, 3)
    sample_points = Frame.compose_transform(F_reg, d_k)

    return sample_points


def find_closest_point(mesh_vertices, indices, s_k):
    """
    Method for finding the closest point on the surface mesh

    Parameters
    _________
    mesh_vertices : np.ndarray
        The xyz coordinates of the vertices of the surface mesh
    indices : np.ndarray
        The indices of the vertices of the surface mesh
    s_k : np.ndarray
        The xyz coordinates of the sample points

    Returns
    _________
    np.ndarray
        The xyz coordinates of the closest point on the surface mesh
    """
    d_min = np.inf
    c_min = None
    for i in range(len(indices)):
        cur_c_k = find_closest_point_triangle(mesh_vertices[indices[i]], s_k)
        cur_d_k = find_euclidian_distance(cur_c_k, s_k)
        if cur_d_k < d_min:
            d_min = cur_d_k
            c_min = cur_c_k
    return c_min


def find_closest_point_triangle(vertices, s_k):
    """
    Method for finding the closest point on a triangle

    Parameters
    _________
    vertices : np.ndarray
        The xyz coordinates of the vertices of the triangle
    s_k : np.ndarray
        The xyz coordinates of the sample points

    Returns
    _________
    np.ndarray
        The xyz coordinates of the closest point on the triangle
    """
    p, q, r, = vertices
    A_minus_p = s_k - vertices[0]
    B = np.vstack(((q - p), (r - p))).T
    lam, mu = np.linalg.lstsq(B, A_minus_p.T, rcond=None)[0]
    c = p + lam * (q - p) + mu * (r - p)

    if lam < 0:
        c = project_on_segment(c, r, p)
    elif mu < 0:
        c = project_on_segment(c, p, q)
    elif lam + mu > 1:
        c = project_on_segment(c, q, r)
    return c


def project_on_segment(c, p, q):
    """
    Method for projecting a point on a segment

    Parameters
    _________
    c : np.ndarray
        The xyz coordinates of the point to be projected
    p : np.ndarray
        The xyz coordinates of the first point on the segment
    q : np.ndarray
        The xyz coordinates of the second point on the segment

    Returns
    _________
    np.ndarray
        The xyz coordinates of the projected point
    """

    if np.linalg.norm(p - q) == 0:
        return p

    t = np.dot(c - p, q - p) / np.dot(q - p, q - p)
    t = np.clip(t, 0, 1)
    return p + t * (q - p)


def find_euclidian_distance(c_k, d_k):
    """
    Method for finding the euclidian distance between the sample points and the surface mesh

    Parameters
    _________
    c_k : np.ndarray
        The xyz coordinates on the surface mesh found from F_reg * d_k
    d_k : np.ndarray
        The xyz coordinates of the tip with respect to rigid body B

    Returns
    _________
    np.ndarray
        The euclidian distance between the sample points and the surface mesh
    """

    mag_dif = np.linalg.norm(c_k - d_k, axis=1)

    return mag_dif

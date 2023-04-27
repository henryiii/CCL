__all__ = ("linear_power", "nonlin_power", "linear_matter_power",
           "nonlin_matter_power", "sigmaM", "sigmaR", "sigmaV", "sigma8",
           "kNL",)

import numpy as np

from . import DEFAULT_POWER_SPECTRUM, check, lib, warn_api


@warn_api
def linear_power(cosmo, k, a, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    r"""The linear power spectrum.

    Arguments
    ---------
    cosmo : :class:`~pyccl.Cosmology`
        Cosmological parameters.
    k : int, float or (nk,) array_like
        Wavenumber in :math:`\rm Mpc^{-1}`.
    a : int, float or (na,) array_like
        Scale factor.
    p_of_k_a : str
        Power spectrum name. Should be stored in ``cosmo``.
        The default is :py:data:`~pyccl.DEFAULT_POWER_SPECTRUM`.

    Returns
    -------
    P_L : floar or (na, nk) numpy.array
        Linear power spectrum, in units of :math:`\rm Mpc^3`.
    """
    return cosmo.get_linear_power(p_of_k_a)(k, a, cosmo)


@warn_api
def nonlin_power(cosmo, k, a, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    r"""The non-linear power spectrum.

    Arguments
    ---------
    cosmo : :class:`~pyccl.Cosmology`
        Cosmological parameters.
    k : int, float or (nk,) array_like
        Wavenumber in :math:`\rm Mpc^{-1}`.
    a : int, float or (na,) array_like
        Scale factor.
    p_of_k_a : str
        Power spectrum name. Should be stored in ``cosmo``.
        The default is :py:data:`~pyccl.DEFAULT_POWER_SPECTRUM`.

    Returns
    -------
    P_NL : floar or (na, nk) numpy.array
        Non-inear power spectrum, in units of :math:`\rm Mpc^3`.
    """
    return cosmo.get_nonlin_power(p_of_k_a)(k, a, cosmo)


def linear_matter_power(cosmo, k, a):
    r"""The linear matter power spectrum.

    Arguments
    ---------
    cosmo : :class:`~pyccl.Cosmology`
        Cosmological parameters.
    k : int, float or (nk,) array_like
        Wavenumber in :math:`\rm Mpc^{-1}`.
    a : int, float or (na,) array_like
        Scale factor.

    Returns
    -------
    P_L : floar or (na, nk) numpy.array
        Linear matter power spectrum, in units of :math:`\rm Mpc^3`.
    """
    return cosmo.linear_power(k, a, p_of_k_a=DEFAULT_POWER_SPECTRUM)


def nonlin_matter_power(cosmo, k, a):
    r"""The non-linear matter power spectrum.

    Arguments
    ---------
    cosmo : :class:`~pyccl.Cosmology`
        Cosmological parameters.
    k : int, float or (nk,) array_like
        Wavenumber in :math:`\rm Mpc^{-1}`.
    a : int, float or (na,) array_like
        Scale factor.

    Returns
    -------
    P_NL : floar or (na, nk) numpy.array
        Non-linear matter power spectrum, in units of :math:`\rm Mpc^3`.
    """
    return cosmo.nonlin_power(k, a, p_of_k_a=DEFAULT_POWER_SPECTRUM)


def sigmaM(cosmo, M, a):
    r"""Root mean squared variance of the linear power spectrum.

    Arguments
    ---------
    cosmo : :class:`~pyccl.Cosmology`
        Cosmological parameters.
    M : int, float or (nM,) array_like
        Halo mass in :math:`\rm M_{\odot}`.
    a : int, float or (na,) array_like
        Scale factor.

    Returns
    -------
    sigM : float or (na, nM) numpy.ndarray
        RMS variance of halo mass.
    """
    cosmo.compute_sigma()

    logM = np.log10(np.atleast_1d(M))
    status = 0
    sigM, status = lib.sigM_vec(cosmo.cosmo, a, logM,
                                len(logM), status)
    check(status, cosmo=cosmo)
    if np.ndim(M) == 0:
        sigM = sigM[0]
    return sigM


@warn_api
def sigmaR(cosmo, R, a=1, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    r"""RMS variance in a top-hat sphere of radius R in Mpc.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): Cosmological parameters.
        R (float or array_like): Radius; Mpc.
        a (float): optional scale factor; defaults to a=1
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, `str` or None): 3D Power spectrum
            to integrate. If a string, it must correspond to one of the
            non-linear power spectra stored in `cosmo` (e.g.
            `'delta_matter:delta_matter'`).

    Returns:
        float or array_like: RMS variance in the density field in top-hat \
            sphere; Mpc.
    """
    psp = cosmo.parse_pk2d(p_of_k_a, is_linear=True)
    status = 0
    R_use = np.atleast_1d(R)
    sR, status = lib.sigmaR_vec(cosmo.cosmo, psp, a, R_use, R_use.size, status)
    check(status, cosmo)
    if np.ndim(R) == 0:
        sR = sR[0]
    return sR


@warn_api
def sigmaV(cosmo, R, a=1, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    """RMS variance in the displacement field in a top-hat sphere of radius R.
    The linear displacement field is the gradient of the linear density field.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): Cosmological parameters.
        R (float or array_like): Radius; Mpc.
        a (float): optional scale factor; defaults to a=1
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, `str` or None): 3D Power spectrum
            to integrate. If a string, it must correspond to one of the
            non-linear power spectra stored in `cosmo` (e.g.
            `'delta_matter:delta_matter'`).

    Returns:
        sigmaV (float or array_like): RMS variance in the displacement field \
            in top-hat sphere.
    """
    psp = cosmo.parse_pk2d(p_of_k_a, is_linear=True)
    status = 0
    R_use = np.atleast_1d(R)
    sV, status = lib.sigmaV_vec(cosmo.cosmo, psp, a, R_use, R_use.size, status)
    check(status, cosmo)
    if np.ndim(R) == 0:
        sV = sV[0]
    return sV


@warn_api
def sigma8(cosmo, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    """RMS variance in a top-hat sphere of radius 8 Mpc/h.

    .. note:: 8 Mpc/h is rescaled based on the chosen value of the Hubble
              constant within `cosmo`.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): Cosmological parameters.
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, `str` or None): 3D Power spectrum
            to integrate. If a string, it must correspond to one of the
            non-linear power spectra stored in `cosmo` (e.g.
            `'delta_matter:delta_matter'`).

    Returns:
        float: RMS variance in top-hat sphere of radius 8 Mpc/h.
    """
    sig8 = cosmo.sigmaR(8/cosmo["h"], p_of_k_a=p_of_k_a)
    if np.isnan(cosmo["sigma8"]):
        cosmo._fill_params(sigma8=sig8)
    return sig8


@warn_api
def kNL(cosmo, a, *, p_of_k_a=DEFAULT_POWER_SPECTRUM):
    """Scale for the non-linear cut.

    .. note:: k_NL is calculated based on Lagrangian perturbation theory as the
              inverse of the variance of the displacement field, i.e.
              k_NL = 1/sigma_eta = [1/(6 pi^2) * int P_L(k) dk]^{-1/2}.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): Cosmological parameters.
        a (float or array_like): Scale factor(s), normalized to 1 today.
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, `str` or None): 3D Power spectrum
            to integrate. If a string, it must correspond to one of the
            non-linear power spectra stored in `cosmo` (e.g.
            `'delta_matter:delta_matter'`).

    Returns:
        float or array-like: Scale of non-linear cut-off; Mpc^-1.
    """
    psp = cosmo.parse_pk2d(p_of_k_a, is_linear=True)
    status = 0
    a_use = np.atleast_1d(a)
    knl, status = lib.kNL_vec(cosmo.cosmo, psp, a_use, a_use.size, status)
    check(status, cosmo)
    if np.ndim(a) == 0:
        knl = knl[0]
    return knl

import sys

import sympy as sym
from scipy import *
from math import *

from scipy import integrate
from sympy import acot, cot


def ellipse_cas1(a, b):
    # applatissement_inverse 1/f
    f = rounding(1 - b / a)
    e2 = rounding(1 - (b ** 2 / a ** 2))
    e2prime = rounding((a ** 2 / b ** 2) - 1)
    alpha = rounding(sym.acos(b / a) * (400 / 360))
    c = rounding((a ** 2) / b)
    return [f, e2, e2prime, alpha, c]


def rounding(nbr: float):
    a = str(nbr)
    point = a.index(".")
    return float(a[:point + 3])


# 2 TRANSFORMATION DES COORDONNEES
# A - Transformation des coordonnees geographiques en cartesiennes
def conversion_geocarto(Phi, L, h):
    # lat et lon en derges     # altitude h en metres
    # CONVERSION SELON WGS84
    phi = radians(Phi)
    LAMBDA = radians(L)
    a = 6378137
    b = 6356752.314245179497563967
    e2 = 1 - (b ** 2 / a ** 2)
    W = 1 - (e2 * (sin(phi) ** 2))
    N = a / sqrt(W)
    x = float((h + N) * cos(LAMBDA) * cos(phi))
    y = float((h + N) * cos(phi) * sin(LAMBDA))
    z = float((h + (1 - e2) * N) * sin(phi))
    return [round(x, 2), round(y, 2), round(z, 2)]


# B - Transfromation des coordonnees cartesiennes en geographiques
def conversion_cartogeo(x, y, z):
    a = 6378137
    b = 6356752.314245179497563967
    f = 1 - (b / a)
    e2 = (2 * f) - (f ** 2)
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    u = atan((z / sqrt(x ** 2 + y ** 2) * ((1 - f) + ((a * e2) / r))))
    L = atan2(y, x)
    # Pour faciliter les calculs on va calculer le numerateur et le denominateur separement
    num = z * (1 - f) + a * e2 * (pow(sin(u), 3))
    den = (1 - f) * (sqrt(x ** 2 + y ** 2) - a * e2 * (pow(cos(u), 3)))
    phi = atan2(num, den)
    h = sqrt(x ** 2 + y ** 2) * cos(phi) + z * sin(phi) - a * sqrt(1 - e2 * pow(sin(phi), 2))
    phi = degrees(phi)
    L = degrees(L)
    return [round(phi, 2), round(L, 2), round(h, 2)]


# 3 LES TROIS LATITUDES (Géodésique, géocentrique, réduite)
def trois_latitudes_b(beta, lam):
    a = 6378137
    b = 6356752.314245179497563967
    LAMBDA = radians(lam)
    BETA = radians(beta)
    # les autres latitudes en fonction de beta
    phi = atan((a / b) * tan(BETA))
    psi = atan((b / a) * tan(BETA))
    # calcul des coordonnees cartesiennes
    X = a * cos(BETA) * cos(LAMBDA)
    Y = a * cos(BETA) * sin(LAMBDA)
    Z = b * sin(BETA)
    phi = degrees(phi)
    psi = degrees(psi)
    return [round(phi, 2), round(psi, 2), round(X, 2), round(Y, 2), round(Z, 2)]


def trois_latitudes_phi(phi, lam):
    a = 6378137
    b = 6356752.314245179497563967
    e2 = 1 - (b ** 2 / a ** 2)
    LAMBDA = radians(lam)
    PHI = radians(phi)
    W = 1 - (e2 * (sin(PHI) ** 2))
    # les autres latitudes en fonction de beta
    beta = atan((b / a) * tan(PHI))
    psi = atan((b ** 2 / a ** 2) * tan(PHI))
    # calcul des coordonnees cartesiennes
    X = (a / sqrt(W)) * cos(PHI) * cos(LAMBDA)
    Y = (a / sqrt(W)) * cos(PHI) * sin(LAMBDA)
    Z = (a * (1 - e2) * sin(PHI)) / sqrt(W)
    beta = degrees(beta)
    psi = degrees(psi)
    return [round(beta, 2), round(psi, 2), round(X, 2), round(Y, 2), round(Z, 2)]


def trois_latitudes_psi(psi, lam):
    a = 6378137
    b = 6356752.314245179497563967
    e2 = 1 - (b ** 2 / a ** 2)
    LAMBDA = radians(lam)
    PSI = radians(psi)
    beta = atan((a / b) * tan(PSI))
    phi = atan((a ** 2 / b ** 2) * tan(PSI))
    W = 1 - (e2 * (sin(phi) ** 2))
    # calcul des coordonnees cartesiennes
    OP = (a / sqrt(W)) * sqrt(1 + ((e2 - 2) * e2 * pow(sin(phi), 2)))
    X = OP * cos(PSI) * cos(LAMBDA)
    Y = OP * cos(PSI) * sin(LAMBDA)
    Z = OP * sin(PSI)
    beta = degrees(beta)
    phi = degrees(phi)
    return [round(beta, 2), round(phi, 2), round(X, 2), round(Y, 2), round(Z, 2)]


# 4 RAYONS DE COURBURE M, N , R alpha
def rayon_courbure_m(Phi):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    phi = radians(Phi)
    W = sqrt(1 - e2 * (sin(phi) ** 2))
    # rayon de courbure du meridien
    M = (a * (1 - e2)) / pow(W, 3)
    return round(M, 3)


def rayon_courbure_1er_vertical(Phi):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    phi = radians(Phi)
    W = sqrt(1 - e2 * (sin(phi) ** 2))
    N = a / W
    return round(N, 3)


def rayon_courbure_azimut(Alpha, Phi):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    alpha = radians(Alpha)
    phi = radians(Phi)
    W = sqrt(1 - e2 * (sin(phi) ** 2))
    M = rayon_courbure_m(phi)
    N = rayon_courbure_1er_vertical(phi)
    num = (M * (sin(alpha) ** 2)) + (N * (cos(alpha) ** 2))
    R = num / (M * N)
    return R


def surface_partie_terrestre(lambda1, lambda2, phi1, phi2):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    PHI1 = radians(phi1)
    PHI2 = radians(phi2)
    LAMBDA1 = radians(lambda1)
    LAMBDA2 = radians(lambda2)

    f = lambda x: cos(x) * ((1 - e2 * (sin(x) ** 2)) ** -2)
    Z = integrate.quad(f, PHI1, PHI2)

    return (b ** 2) * (LAMBDA2 - LAMBDA1) * Z[0]


def longueur_meridien(Phi):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    f = lambda x:(1 - e2 * sin(x)**2)**(-3/2)
    return round((b * integrate.quad(f, 0, radians(Phi))[0] / 1000),4)


def longueur_parallele(Phi, delta_lambda):
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)
    phi = radians(Phi)
    N = a / (1 - e2 * sin(phi)**2)

    return round((N * cos(phi) * delta_lambda),4)

def pb_direct(Phi1, Lambda1, S, A12):
    a = 6356515
    b = 6356752.3142
    phi1 = radians(Phi1)
    lambda1 = radians(Lambda1)
    a12 = radians(A12)

    # calcul de sigma12
    R = (2 * a + b) / 3
    sigma12 = S / R

    # calcul de phi2
    phi2 = asin((sin(phi1) * cos(sigma12))+(cos(phi1) * sin(sigma12) * cos(a12)))
    Phi2 = degrees(phi2)

    # calcul de lambda2
    lambda2 = lambda1 + ((acot((cot(sigma12) * cos(phi1)) - (sin(phi1) * cos(a12)))) / sin(a12))
    Lambda2 = degrees(lambda2)

    # calcul de l azimut de retour a21
    a21 = acot((cos(sigma12*cos(A12)-tan(phi1)*sin(sigma12)))/sin(A12))
    A21 = degrees(a21)

    Phi2 = rounding(Phi2)
    Lambda2 = rounding(Lambda2)
    A21 = rounding(A21)
    return [Phi2, Lambda2, A21]

# def pb_direct(phi1,l1,s,a12):
#     a = 6378137
#     f = 1 / 298.257223563
#     b = a * (1 - f)
#     R = (2 * a + b) / 3
#
#     sigma = s/R
#
#     phi1 = radians(phi1)
#     l1 = radians(l1)
#     a12 = radians(a12)
#
#     phi2 = asin(sin(phi1)*cos(sigma)+cos(phi1)*sin(sigma)*cos(a12))
#     lambda2 = acot((1/sin(a12))*cot(sigma)*sin((pi/2)-phi1)-cos((pi/2)-phi1)*cos(a12))+l1
#     a21 = acot((1/sin(a12))*cos(sigma)*cos(a12)-tan(phi1)*sin(sigma))
#
#     phi2 = degrees(phi2)
#     lambda2 = degrees(lambda2)
#     a21 = degrees(a21)
#
#     # phi2 = round(phi2,4)
#     # lambda2 = round(lambda2,4)
#     # a21 = round(a21,4)
#
#     return [phi2,lambda2,a21]

def pb_inverse(phi1, lambda1, phi2, lambda2):
    a = 6378137
    b = 6356752.3142
    phi1 = radians(phi1)
    lambda1 = radians(lambda1)
    phi2 = radians(phi2)
    lambda2 =radians(lambda2)

    delta = lambda2 - lambda1

    # calcul de sigma12
    sigma12 = acos((sin(phi1) * sin(phi2)) + (cos(phi1) * cos(phi2) * cos(delta)))

    # Pour obtenir la distance metrique entre les deux points, on multiplie cette valeur sigma12 par le rayon de la
    # sphere consideree
    R = ((2 * a) + b) / 3
    sigma12 = degrees(sigma12)
    S12 = sigma12 * R

    # calcul de l azimut d'aller a12
    a12 = acot(((tan(phi2)*cos(phi1))/sin(delta)) - (sin(phi1)*cot(delta)))

    # calcul de l azimut de retour a21]
    a21 = acot(-(((tan(phi1)*cos(phi2))/sin(delta))-(sin(phi2)*cot(delta))))

    a12= degrees(a12)
    a21 = degrees(a21)

    a12 = round(a12,4)
    a21 = round(a21,4)
    S12 = round(S12,4)

    return [a12, a21, S12]

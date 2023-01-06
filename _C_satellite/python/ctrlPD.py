import numpy as np
import satelliteParam as P


class ctrlPD:
    def __init__(self):
        ####################################################
        #       PD Control: Time Design Strategy
        ####################################################
        # tuning parameters
        tr_th = 1 # rise time for inner loop
        zeta_th = 0.9  # damping ratio for inner loop
        M = 10.0  # Time scale separation between inner and outer loop
        zeta_phi = 0.9  # damping ratio for outer loop
        # saturation limits
        self.theta_max = 30.0*np.pi/180.0  # maximum commanded base angle
        #---------------------------------------------------
        #                    Inner Loop
        #---------------------------------------------------
        # PD design for inner loop
        wn_th = 2.2 / tr_th
        #wn_th = 0.5 * np.pi / (tr_th * np.sqrt(1 - zeta_th**2))# 2.2/tr_th
        self.kp_th = wn_th**2 * (P.Js + P.Jp)
        self.kd_th = 2 * zeta_th * wn_th * (P.Js + P.Jp)
        # DC gain for inner loop
        #k_DC_th = kp_th/(P.k+kp_th)
        k_DC_th = 1
        #---------------------------------------------------
        #                    Outer Loop
        #---------------------------------------------------
        # PD design for outer loop
        tr_phi = M * tr_th  # rise time for outer loop
        #wn_phi = 0.5 * np.pi / (tr_phi * np.sqrt(1 - zeta_phi**2)) #2.2/tr_phi
        wn_phi =2.2 / tr_phi
        AA = np.array([
                    [P.k * k_DC_th, -P.b * k_DC_th * wn_phi**2],
                    [P.b * k_DC_th, P.k * k_DC_th - 2 * zeta_phi * wn_phi * P.b * k_DC_th]])    
        bb = np.array([
                    [-P.k + P.Jp * wn_phi**2],
                    [-P.b + 2 * P.Jp * zeta_phi * wn_phi]])
        tmp = np.linalg.inv(AA) @ bb
        self.kp_phi = tmp[0][0]
        self.kd_phi = tmp[1][0]
        # DC gain for outer loop
        k_DC_phi = P.k * k_DC_th * self.kp_phi / (P.k + P.k * k_DC_th * self.kp_phi)
        # Used to check the math in the matrix inversion.
        # print(np.roots([1.0, (P.b+P.b*k_DC_th*kp_phi+P.k*k_DC_th*kd_phi)/(P.Jp + P.b*k_DC_th*kd_phi),\
        #                 (P.k + P.k*k_DC_th*kp_phi)/(P.Jp + P.b*k_DC_th*kd_phi)]))
        #
        # print(np.roots([1.0, 2*zeta_phi*wn_phi, wn_phi**2]))
        # print control gains to terminal        
        print('k_DC_phi', k_DC_phi)
        print('kp_th: ', self.kp_th)
        print('kd_th: ', self.kd_th)
        print('kp_phi: ', self.kp_phi)
        print('kd_phi: ', self.kd_phi)

    def update(self, phi_r, state):
        theta = state[0][0]
        phi = state[1][0]
        thetadot = state[2][0]
        phidot = state[3][0]
        # outer loop: outputs the reference angle for theta
        # note that book recommends a feed forward term because
        # of poor DC gain on the outer loop which
        # is why we add an addition "phi_r" at the end
        theta_r = self.kp_phi * (phi_r - phi) - self.kd_phi * phidot + phi_r
        theta_r = saturate(theta_r, self.theta_max)
        # inner loop: outputs the torque applied to the base
        tau = self.kp_th * (theta_r - theta) - self.kd_th * thetadot
        return saturate(tau, P.tau_max)


def saturate(u, limit):
    if abs(u) > limit:
        u = limit * np.sign(u)
    return u

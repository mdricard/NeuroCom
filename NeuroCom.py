import numpy as np
import matplotlib.pyplot as plt
from math import degrees, asin
from BiomechTools import low_pass, zero_crossing, max_min, simpson_nonuniform, critically_damped, residual_analysis
import os.path
from os import path

class NeuroCom:
    x = np.zeros(1250)
    lf = np.zeros(1250)
    rr = np.zeros(1250)
    sh = np.zeros(1250)
    lr = np.zeros(1250)
    rf = np.zeros(1250)
    fz = np.zeros(1250)         # Vertical force lf + lr + rf + rr
    fp_cofx = np.zeros(1250)
    fp_cofy = np.zeros(1250)
    fp_cogx = np.zeros(1250)
    fp_cogy = np.zeros(1250)
    theta = np.zeros(1250)  # used to compute sway angle
    omega = np.zeros(1250)  # used to compute sway angular velocity

    def __init__(self, filename):
        with open(filename) as f:
            for i in range(7):
                f.readline()
            subj_line = f.readline().rstrip()  # remove newline character
            # ------   get subject id as string   -------------------------------
            self.subject = subj_line.split(',')[1]  # int(subj_line.split()[0])
            # ------   get subject date of birth as string   --------------------
            dob_line = f.readline().rstrip()
            self.date_of_birth = dob_line.split(',')[1]
            # ------   get subject height as float   -----------------------------
            ht_line = f.readline().rstrip()
            ht_str = ht_line.split(',')[1]
            self.ht = self.fix_string(ht_str, data_type=1) # * 2.54 / 100.0 # ht in meters
            self.cog_ht = np.float64(0.5527 * self.ht)  # cog ht is 55.27 % of ht, see NeuroCom Appendix
            for i in range(4):
                f.readline()
            # ------   get test type as string   ---------------------------------
            test_line = f.readline().rstrip()
            self.test_type = test_line.split(',')[1]
            for i in range(4):
                f.readline()
            # ------   get cond id as integer   -----------------------------------
            cond_line = f.readline().rstrip()
            cond_str = cond_line.split(',')[1]
            self.cond = self.fix_string(cond_str, data_type=0)
            # ------   get trial as integer   -------------------------------------
            trial_line = f.readline().rstrip()
            trial_str = trial_line.split(',')[1]
            self.trial = self.fix_string(trial_str, data_type=0)
            # ------   get sampling rate as integer   -----------------------------
            rate_line = f.readline().rstrip()
            rate_str = rate_line.split(',')[1]
            self.sampling_rate = self.fix_string(rate_str, data_type=0)
            f.readline()
            # ------   get sample duration   -----------------------------
            duration_line = f.readline().rstrip()
            duration_str = duration_line.split(',')[1]
            self.duration = self.fix_string(duration_str, data_type=1)
            # ------   get number of points   -----------------------------
            n_line = f.readline().rstrip()
            n_str = n_line.split(',')[1]
            self.n = self.fix_string(n_str, data_type=0)
            for i in range(4):
                f.readline()
            for row in range(self.n):
                nmbr_line = f.readline().rstrip()
                nmbr_str = nmbr_line.split(',')
                self.x[row] = self.fix_string(nmbr_str[0], data_type=1)
                self.lf[row] = self.fix_string(nmbr_str[1], data_type=1)
                self.rr[row] = self.fix_string(nmbr_str[2], data_type=1)
                self.sh[row] = self.fix_string(nmbr_str[3], data_type=1)
                self.lr[row] = self.fix_string(nmbr_str[4], data_type=1)
                self.rf[row] = self.fix_string(nmbr_str[5], data_type=1)
                self.fp_cofx[row] = self.fix_string(nmbr_str[6], data_type=1)
                self.fp_cofy[row] = self.fix_string(nmbr_str[7], data_type=1)
                self.fp_cogx[row] = self.fix_string(nmbr_str[8], data_type=1)
                self.fp_cogy[row] = self.fix_string(nmbr_str[9], data_type=1)
                self.fz[row] = self.lf[row] + self.lr[row] + self.rf[row] + self.rr[row]
        self.smooth_shear = critically_damped(raw=self.sh, sampling_rate=self.sampling_rate, filter_cutoff=20)
        self.smooth_cog_x = low_pass(raw=self.fp_cogx, sampling_rate=self.sampling_rate, filter_cutoff=6)
        self.smooth_cog_y = low_pass(raw=self.fp_cogy, sampling_rate=self.sampling_rate, filter_cutoff=6)
        self.smooth_cof_x = low_pass(raw=self.fp_cofx, sampling_rate=self.sampling_rate, filter_cutoff=6)
        self.smooth_cof_y = low_pass(raw=self.fp_cofy, sampling_rate=self.sampling_rate, filter_cutoff=6)
        self.smooth_fz = critically_damped(raw=self.fz, sampling_rate=self.sampling_rate, filter_cutoff=20)
        for i in range(self.n):
            self.theta[i] = degrees(asin(self.smooth_cog_y[i] / self.cog_ht)) - 2.3  # See NeuroCom appendix for formula

    @staticmethod
    def fix_string(messy_string, data_type):
        """
        Remove non-numeric characters from string data_type 0 is an integer, 1 is a float
        """
        numeric_part = ''.join(char for char in messy_string if char.isdigit() or char == '.')
        if data_type == 0:
            result = int(numeric_part)
        else:
            result = float(numeric_part)
        return result

    def plot_cofy_theta(self):
        plt.plot(self.x[1:], self.theta[1:], label='theta')
        plt.plot(self.x[1:], self.smooth_cog_y[1:], label='Cog Y')
        plt.legend()
        plt.grid(True)
        plt.xlabel('Point Number (n)')
        plt.ylabel('theta (d) Cog (cm)')
        plt.show()

    def moving_ave(self, curve, window_size):
        npts = len(curve)
        m_ave = np.zeros(npts)
        if window_size % 2 == 0:
            window_size += 1
        start_pt = int(window_size / 2)
        for i in range(int(window_size/2), npts - int(window_size/2)):
            sum = 0.0
            cntr = 0
            for p in range(i-start_pt, i+start_pt+1):
                sum += curve[p]
                cntr += 1
            m_ave[i] = sum / cntr

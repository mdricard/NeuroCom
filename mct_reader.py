import numpy as np
import matplotlib.pyplot as plt
from BiomechTools import zero_crossing, low_pass, critically_damped, residual_analysis
from math import asin, degrees

x = np.zeros(1250)
lf = np.zeros(1250)
rr = np.zeros(1250)
sh = np.zeros(1250)
lr = np.zeros(1250)
rf = np.zeros(1250)
fp_cofx = np.zeros(1250)
fp_cofy = np.zeros(1250)
fp_cogx = np.zeros(1250)
fp_cogy = np.zeros(1250)
theta = np.zeros(1250)          # used to compute sway angle
omega = np.zeros(1250)          # used to compute sway angular velocity
def fix_string(messy_string, data_type):
    """
    Remove non-numeric characters from string
    data_type 0 is an integer, 1 is a float
    """
    numeric_part = ''.join(char for char in messy_string if char.isdigit() or char == '.')
    if data_type == 0:
        result = int(numeric_part)
    else:
        result = float(numeric_part)
    return result

def read_neurocom_file_header(filename):
    """
    :param filename:
    :returns:
        subject as string
        date_of_birth as string
        ht as float
        test_type as string "MCT", "ADT", "SOT"
        cond as integer
        trial as integer
        sampling_rate as integer
    """
    with open(filename) as f:
        for i in range(7):
            f.readline()
        subj_line = f.readline().rstrip()                 # remove newline character
        # ------   get subject id as string   -------------------------------
        subject = subj_line.split(',')[1]                 #int(subj_line.split()[0])
        # ------   get subject date of birth as string   --------------------
        dob_line = f.readline().rstrip()
        date_of_birth = dob_line.split(',')[1]
        # ------   get subject height as float   -----------------------------
        ht_line = f.readline().rstrip()
        ht_str = ht_line.split(',')[1]
        ht = fix_string(ht_str, data_type=1)
        cog_ht = 0.5527 * ht        # cog ht is 55.27 % of ht, see NeuroCom Appendix
        for i in range(4):
            f.readline()
        # ------   get test type as string   ---------------------------------
        test_line = f.readline().rstrip()
        test_type = test_line.split(',')[1]
        for i in range(4):
            f.readline()
        # ------   get cond id as integer   -----------------------------------
        cond_line = f.readline().rstrip()
        cond_str = cond_line.split(',')[1]
        cond = fix_string(cond_str, data_type=0)
        # ------   get trial as integer   -------------------------------------
        trial_line = f.readline().rstrip()
        trial_str = trial_line.split(',')[1]
        trial = fix_string(trial_str, data_type=0)
        # ------   get sampling rate as integer   -----------------------------
        rate_line = f.readline().rstrip()
        rate_str = rate_line.split(',')[1]
        sampling_rate = fix_string(rate_str, data_type=0)
        f.readline()
        # ------   get sample duration   -----------------------------
        duration_line = f.readline().rstrip()
        duration_str = duration_line.split(',')[1]
        duration = fix_string(duration_str, data_type=1)
        # ------   get number of points   -----------------------------
        n_line = f.readline().rstrip()
        n_str = n_line.split(',')[1]
        n = fix_string(n_str, data_type=0)
        for i in range(4):
            f.readline()
        for row in range(n):
            nmbr_line = f.readline().rstrip()
            nmbr_str = nmbr_line.split(',')
            x[row] = fix_string(nmbr_str[0], data_type=1)
            lf[row] = fix_string(nmbr_str[1], data_type=1)
            rr[row] = fix_string(nmbr_str[2], data_type=1)
            sh[row] = fix_string(nmbr_str[3], data_type=1)
            lr[row] = fix_string(nmbr_str[4], data_type=1)
            rf[row] = fix_string(nmbr_str[5], data_type=1)
            fp_cofx[row] = fix_string(nmbr_str[6], data_type=1)
            fp_cofy[row] = fix_string(nmbr_str[7], data_type=1)
            fp_cogx[row] = fix_string(nmbr_str[8], data_type=1)
            fp_cogy[row] = fix_string(nmbr_str[9], data_type=1)

    return subject, date_of_birth, ht, cog_ht, test_type, cond, sampling_rate, duration, n

def plot_cop():
    plt.plot(x[1:], fp_cofx[1:], label='fpcofx')
    plt.plot(x[1:], fp_cofy[1:], label='fpcofy')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Point Number (n)')
    plt.ylabel('Force (N)')
    plt.show()

def plot_cofy_theta():
    plt.plot(x[1:], theta[1:], label='theta')
    plt.plot(x[1:], smooth_cog_y[1:], label='Cog Y')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Point Number (n)')
    plt.ylabel('theta (d) Cog (cm)')
    plt.show()

def plot_shear():
    plt.plot(x[1:], sh[1:], label='Shear')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Point Number (n)')
    plt.ylabel('Shear Force (N)')
    plt.show()

def plot_cog_and_shear():
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    #ax1.plot(x, smooth_cog_x, 'b-', label='Cog X')
    ax1.plot(x, smooth_cog_y, 'r-', label='Cog Y')
    ax2.plot(x, smooth_shear, 'k-', label='Shear')
    ax1.set_ylabel('COG (cm)')
    ax2.set_ylabel('Shear Force (N)')
    #fig.tight_layout()
    plt.grid(True)
    #plt.legend(['Cog X', 'Cog Y', 'Shear'])
    ax1.legend([smooth_cog_y, smooth_shear], ['Cog Y', 'Shear'])
    plt.show()

def plot_theta_and_shear():
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, theta, 'r-', label='Theta')
    ax2.plot(x, smooth_shear, 'k-', label='Shear')
    ax1.set_ylabel('Theta COG (d)')
    ax2.set_ylabel('Shear Force (N)')
    #fig.tight_layout()
    plt.grid(True)
    #plt.legend(['Cog X', 'Cog Y', 'Shear'])
    ax1.legend([smooth_cog_y, smooth_shear], ['Cog Y', 'Shear'])
    plt.show()

def plot_cof_cog_shear():
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(x, smooth_cof_y, color='blue')        # Left Y Axis Center of Pressure
    ax1_twin = ax1.twinx()      # Create a twin axes sharing the x-axis
    ax1_twin.plot(x, smooth_shear, color='red')   # Right Y Axis Shear Force
    ax1.set_ylabel('COP (cm)', color='blue')
    ax1_twin.set_ylabel('Shear Force (N)', color='red')
    ax1.set_title('COP Center of Pressure vs Shear Force')

    ax2.plot(x, smooth_cog_y, color='black')    # Left Y Axis Cog Y
    ax2_twin = ax2.twinx()   # Create a twin axes sharing the x-axis
    ax2_twin.plot(x, smooth_shear, color='red')  # Right Y Axis Shear Force
    # Add labels and titles
    ax2.set_ylabel('COG Y (cm)', color='black')
    ax2_twin.set_ylabel('Shear Force (N)', color='red')
    ax2.set_title('COG Y vs Shear Force')
    plt.tight_layout()  # Adjust layout and display the plot
    plt.show()

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C1_T2_10162008_004621.txt'
#file_name = 'D:/Crystal_MCT/FD1528_PC-022_SOT_C1_T1_10162008_003707.txt'
subject, date_of_birth, ht, cog_ht, test_type, cond_str, sampling_rate, duration, n = read_neurocom_file_header(filename=file_name)
#resid = residual_analysis(raw=sh, sampling_rate=sampling_rate, first_cutoff=2, last_cutoff=20, use_critical=False)
smooth_shear = critically_damped(raw=sh, sampling_rate=sampling_rate, filter_cutoff=20)
smooth_cog_x = low_pass(raw=fp_cogx, sampling_rate=sampling_rate, filter_cutoff=6)
smooth_cog_y = low_pass(raw=fp_cogy, sampling_rate=sampling_rate, filter_cutoff=6)
smooth_cof_x = low_pass(raw=fp_cofx, sampling_rate=sampling_rate, filter_cutoff=6)
smooth_cof_y = low_pass(raw=fp_cofy, sampling_rate=sampling_rate, filter_cutoff=6)
for i in range(len(smooth_cog_y)):
    theta[i] = degrees(asin(smooth_cog_y[i]/cog_ht)) - 2.3          # See NeuroCom appendix for formula
print('height: ', ht)
plot_cof_cog_shear()
plot_theta_and_shear()
plot_cofy_theta()

plot_cop()
plot_cog_and_shear()
#plt.plot(smooth_shear, 'r')
#plt.plot(sh, 'y')
#plt.grid()
#plt.xlabel('Point Number (n)')
#plt.ylabel('Shear Force (N)')
#plt.legend(['Smoothed Shear', 'Raw Shear'])
#plt.show()


#plot_shear()
#print("height is ", ht)
#print('dp[0] = ', x[0])

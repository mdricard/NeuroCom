import numpy as np
import matplotlib.pyplot as plt
from NeuroCom import NeuroCom

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C1_T1_10162008_004621.txt'
c1t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C1_T2_10162008_004621.txt'
c1t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C1_T3_10162008_004621.txt'
c1t3 = NeuroCom(file_name)
cond_1 = [c1t1, c1t2, c1t3]   # a list of NeuroCom objects

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C2_T1_10162008_004621.txt'
c2t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C2_T2_10162008_004621.txt'
c2t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C2_T3_10162008_004621.txt'
c2t3 = NeuroCom(file_name)
cond_2 = [c2t1, c2t2, c2t3]   # a list of NeuroCom objects

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C3_T1_10162008_004621.txt'
c3t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C3_T2_10162008_004621.txt'
c3t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C3_T3_10162008_004621.txt'
c3t3 = NeuroCom(file_name)
cond_3 = [c3t1, c3t2, c3t3]   # a list of NeuroCom objects

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C4_T1_10162008_004621.txt'
c4t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C4_T2_10162008_004621.txt'
c4t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C4_T3_10162008_004621.txt'
c4t3 = NeuroCom(file_name)
cond_4 = [c4t1, c4t2, c4t3]   # a list of NeuroCom objects

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C5_T1_10162008_004621.txt'
c5t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C5_T2_10162008_004621.txt'
c5t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C5_T3_10162008_004621.txt'
c5t3 = NeuroCom(file_name)
cond_5 = [c5t1, c5t2, c5t3]   # a list of NeuroCom objects

file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C6_T1_10162008_004621.txt'
c6t1 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C6_T2_10162008_004621.txt'
c6t2 = NeuroCom(file_name)
file_name = 'D:/Crystal_MCT/FD1528_PC-022_MCT_C6_T3_10162008_004621.txt'
c6t3 = NeuroCom(file_name)
cond_6 = [c6t1, c6t2, c6t3]   # a list of NeuroCom objects

plt.plot(c1t1.smooth_fz, label='trial 1')
plt.plot(c1t2.smooth_fz, label='trial 2')
plt.plot(c1t3.smooth_fz, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('Vertical Force (N)')
plt.title('MCT Condition 1')
plt.show()
#c1t1.moving_ave(c1t1.smooth_fz, 50)

plt.plot(c1t2.smooth_cof_y, label='cond 1')
plt.plot(c2t2.smooth_cof_y, label='cond 2')
plt.plot(c3t2.smooth_cof_y, label='cond 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 1 vs. Condition 3 vs. Condition 5')
plt.show()

plt.plot(c1t1.smooth_cof_y, label='trial 1')
plt.plot(c1t2.smooth_cof_y, label='trial 2')
plt.plot(c1t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 1')
plt.show()

plt.plot(c2t1.smooth_cof_y, label='trial 1')
plt.plot(c2t2.smooth_cof_y, label='trial 2')
plt.plot(c2t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 2')
plt.show()

plt.plot(c3t1.smooth_cof_y, label='trial 1')
plt.plot(c3t2.smooth_cof_y, label='trial 2')
plt.plot(c3t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 3')
plt.show()

plt.plot(c4t1.smooth_cof_y, label='trial 1')
plt.plot(c4t2.smooth_cof_y, label='trial 2')
plt.plot(c4t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 4')
plt.show()

plt.plot(c5t1.smooth_cof_y, label='trial 1')
plt.plot(c5t2.smooth_cof_y, label='trial 2')
plt.plot(c5t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 5')
plt.show()

plt.plot(c6t1.smooth_cof_y, label='trial 1')
plt.plot(c6t2.smooth_cof_y, label='trial 2')
plt.plot(c6t3.smooth_cof_y, label='trial 3')
plt.grid(True)
plt.legend()
plt.xlabel('Point Number (n)')
plt.ylabel('COP (cm)')
plt.title('MCT Condition 6')
plt.show()
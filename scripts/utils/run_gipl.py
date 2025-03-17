import subprocess
import os
import numpy as np



def run_gipl(index, x, y, tas_all,pr_all,SOIL, Tsoil):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Write tas data
    f = open(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}/in/bound.txt'.format(index+101)), 'w')
    f.write('36\n')
    for i in range(36):
        f.write(str(i + 1) + '\t' + str(tas_all[i, y, x].round(2)) + '\n')
    f.close()

    # Write initial data
    dep_lst = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80,
               90, 100, 110, 120]
    f = open(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\in\initial.txt'.format(index + 101)), 'w')
    f.write('1\t31\n')
    f.write('DEPTH\tTEMP\n')
    for d in range(31):
        f.write(str(dep_lst[d]) + '\t' + str(Tsoil[d, y, x])+ '\n')
    f.close()


    # Write soil data
    f = open(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\in\mineral.txt'.format(index + 101)), 'w')
    f.write('1\n')
    f.write('1\t3\n')
    if SOIL [y,x] == 1:
        f.write('0.20	0.07    -0.17	3100000.0	1500000.0	1.5	0.9	1\n')
        f.write('0.18	0.12	-0.15	2500000.0	1900000.0	1.7	2.2	9\n')
        f.write('0.04	0.01	-0.10	3250000.0	2480000.0	2.7	3.1	110\n')
    if SOIL [y,x] == 2:
        f.write('0.18	0.07	-0.17	3100000.0	1500000.0	1.6	2.4	2\n')
        f.write('0.17	0.12	-0.15	2500000.0	1900000.0	0.7	1.4	8\n')
        f.write('0.04	0.01	-0.10	3250000.0	2480000.0	2.7	3.1	110\n')
    if SOIL [y,x] == 3:
        f.write('0.06	0.037	-0.14	2800000.0	2200000.0	1.3	1.6	2\n')
        f.write('0.12	0.12	-0.15	2500000.0	1900000.0	1.3	1.6	8\n')
        f.write('0.04	0.01	-0.10	3250000.0	2480000.0	2.7	3.1	110\n')
    if SOIL [y,x] == 4:
        f.write('0.12	0.037	-0.14	2800000.0	2200000.0	1.3	1.6	3\n')
        f.write('0.12	0.12	-0.15	2500000.0	1900000.0	0.6	1.0	7\n')
        f.write('0.04	0.01	-0.10	3250000.0	2480000.0	2.7	3.1	110\n')
    f.close()


    # Write snow depth data
    snow = np.full(36, 0.0)
    for year in range(2010, 2013):
        for mon in range(12):
            # Divide rain and snow based on temperature, with -2 ℃ and 2 ℃ as two boundaries
            if tas_all[12 * (year - 2010) + mon, y, x] > 2:
                snow[12 * (year - 2010) + mon] = 0
            else:
                if tas_all[12 * (year - 2010) + mon, y, x] > -2:
                    pr_all[12 * (year - 2010) + mon, y, x] = pr_all[12 * (year - 2010) + mon, y, x] * (0.5 - 0.25 * tas_all[12 * (year - 2010) + mon, y, x])
                if 12 * (year - 2010) + mon == 0:
                    snow[12 * (year - 2010) + mon] = pr_all[12 * (year - 2010) + mon, y, x]
                else:
                    if snow[12 * (year - 2010) + mon - 1] == 0:
                        snow[12 * (year - 2010) + mon] = pr_all[12 * (year - 2010) + mon, y, x]
                    else:
                        snow[12 * (year - 2010) + mon] = pr_all[12 * (year - 2010) + mon, y, x] + snow[12 * (year - 2010) + mon - 1]
    snow = snow / 0.138 / 1000
    f = open(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\in\snow.txt'.format(index + 101)), 'w')
    f.write('36\n')
    for i in range(36):
        f.write(str(i + 1) + '\t' + str(snow[i].round(2)) + '\n')
    f.close()

    if (os.path.exists(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\out\result.txt' .format(index+101)))):
        os.remove(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\out\result.txt'.format(index + 101)))
    # Call GIPL2
    os.chdir(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}'.format(index+101)))
    subprocess.check_call(os.path.join(BASE_DIR, '../../temp/GIPL-master-{}\gipl.exe'.format(index+101)))



import csv
import glob
import os
import re
import pandas as pd


def csv_read(read_files):

    rs = []
    seq = []
    GSA = []
    other = []


    # opening the CSV file
    with open(read_files[0], mode='r')as file:
        csvFile = csv.reader(file)

        # patient_id is the first row that contain patient name
        for lines in csvFile:
            patient_id = lines
            break

        for lines in csvFile:
            search = re.search("rs", lines[0])
            if search:
                if lines[0][:2] == "rs":
                    rs.append(lines)
                elif lines[0][:3] == "GSA":
                    GSA.append(lines)
                elif lines[0][:3] == "seq":
                    seq.append(lines)
                else:
                    other.append(lines)

        return rs, GSA, seq, other, patient_id




def txt_read(read_files):
    rs = []
    seq = []
    GSA = []
    other = []

    input_file_list = []

    input_file = open(read_files[0], "r")
    # converted input file into list
    for line in input_file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        input_file_list.append(line_list)

    # split into 4 diff. list
    for lines in input_file_list:
        search = re.search("rs", lines[0])
        if search:
            if lines[0][:2] == "rs":
                rs.append(lines)
            elif lines[0][:3] == "GSA":
                GSA.append(lines)
            elif lines[0][:3] == "seq":
                seq.append(lines)
            else:
                other.append(lines)

    patient_id = input_file_list[0]

    return rs, GSA, seq, other, patient_id






def unique_id_list_extracted(ext):
    import time
    start_time = time.time()

    # step1
    file_path = "input_rs_ids/"
    read_files = glob.glob(os.path.join(file_path, "*.*"))

    unique_rs_id = []




    # common list of all the rs_id
    for j in read_files:
        z = 0
        with open(j, mode='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                if z == 0:
                    z = z + 1
                    name = lines
                else:
                    unique_rs_id.append(lines)


    # step2
    # reading from 7 lakh data file
    file_path1 = "input_genome_file/"
    read_files1 = glob.glob(os.path.join(file_path1, "*.*"))



    # start_time1 = time.time()
    if ext == 'txt':
        rs, GSA, seq, other, patient_id = txt_read(read_files1)
    else:
        rs, GSA, seq, other, patient_id = csv_read(read_files1)

    print('time taken to divide in to 4 different list =>', time.time() - start_time)

    info = [name[0], name[1]]
    column = info + patient_id
    print(len(column), end="")
    print(column)

    # step3
    _final_list_ = []

    rs_id_type = [rs, seq, GSA, other]

    for i in unique_rs_id:
        s = 0
        if i[2] == 'rs602662' :
            i[2] = 'exm-rs492602'
        for z in rs_id_type:
            for j in z:
                # print(i[2]+'dataTest',end="")
                x = re.search(str(i[2]), j[0])
                if x:
                    index = j[0].index(i[2])
                    m = j[0][index:]
                    if i[2] == m:
                        if i[2] == 'exm-rs492602' :
                            i[2] = 'rs602662'
                        j[0] = i[2]
                        info = [i[0], i[1]]
                        info1 = info + j
                        print(len(info1), end="")
                        print(info1)
                        _final_list_.append(info1)

                        s = s + 1
                        break
            if s != 0:
                break

        if s == 0:
            info = [i[0], i[1], i[2]]
            for j in range(0, len(rs[0]) - 1):
                info.append("N/A")
            print(len(info), end="")
            print(info)
            _final_list_.append(info)




    info = [name[0], name[1]]
    column = info + patient_id
    df = pd.DataFrame(columns=column)
    for i in _final_list_:
        df.loc[len(df.index)] = i
    df.to_csv('generated_rs_id_for_batch/{}_output.csv'.format(read_files[0][13:-4]), index = False)

    print("total time taken =>", time.time() - start_time, "  seconds")

    return 'DONE'





# extracting input file extension so that specific function can be called

file_path = "input_genome_file/"
read_files = glob.glob(os.path.join(file_path, "*.*"))
ext = str(read_files[0][-3:])

# extension = input("enter the file extension  => ")
unique_id_list_extracted(ext)
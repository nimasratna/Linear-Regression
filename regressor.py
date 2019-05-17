import sys
import random
import os
import math


def main():
    datasetfile = sys.argv[2]
    dataset=[]
    inpt= []
    outdir = "set"

    #os.system("python scaler.py -a "+str(datasetfile)+" > scaledata.txt") #stored max and min for scalling
    #os.system("python scaler.py -s scaledata.txt < "+str(datasetfile)+" > out.txt") #scaled dataset store in out.txt
    os.system("python validator.py -g "+str(datasetfile)+" -d "+outdir+" > split") #split scaled dataset and store it in out directory

    #find correct K(degree)
    for line in sys.stdin:
        if line != '\n' and line != '\n\r':
            l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
            inpt.append(l)

    dimension = len(inpt[0])
    f = open("split", "r")
    number_of_split = int(f.readline())
    k_max = 3
    #Qtable = [k_max][number_of_split]

    fo = open("validationevaluation.txt", "w+")
    for i in range(1, k_max+1):
        if i == 1:
            q_for_k = 0

            os.system("python converter.py -n " + str(dimension) + " -k " + str(i) + " > description1.txt")
            for j in range(number_of_split):
                trainingset = outdir + "/training_set" + str(j + 1) + ".txt"
                if dimension > 1:
                    os.system(
                        "python scaler.py -a " + str(
                            datasetfile) + " > scaledata.txt")  # stored max and min for scalling

                os.system("python trainer.py -t " + trainingset + " < description1.txt > description1.txt")

            for j in range(number_of_split):
                trainingset = outdir + "/training_set" + str(j + 1) + ".txt"
                # calculate output after training trainee.py for training and validation
                os.system("python trainee.py -d description.txt < " + trainingset + " > out" + str(j + 1) + ".txt")
                # calculate Q trainee and validation
                os.system("python validator.py -e " + trainingset + " < out" + str(j + 1) + ".txt > evaluation")
                f = open("evaluation", "r")
                q = float(f.readline())
                q_for_k += q
            q_for_k = q_for_k / number_of_split
            qval_for_k = 0
            for j in range(number_of_split):
                trainingset = outdir + "/validation_set" + str(j + 1) + ".txt"
                # calculate output after training trainee.py for training and validation
                os.system("python trainee.py -d description.txt < " + trainingset + " > outval" + str(j + 1) + ".txt")
                # calculate Q trainee and validation
                os.system("python validator.py -e " + trainingset + " < outval" + str(j + 1) + ".txt > evaluation")
                f = open("evaluation", "r")
                q = float(f.readline())
                qval_for_k += q
            qval_for_k = qval_for_k / number_of_split
        else:

            q_for_k = 0

            os.system("python converter.py -n "+str(dimension)+" -k "+str(i)+" > description1.txt")
            for j in range(number_of_split):
                trainingset = outdir + "/training_set"+str(j+1)+".txt"
                if dimension > 1:
                    os.system(
                        "python scaler.py -a " + str(datasetfile) + " > scaledata.txt")  # stored max and min for scalling

                os.system("python trainer.py -t "+trainingset+" < description1.txt > description1.txt")

            for j in range(number_of_split):
                trainingset = outdir + "/training_set" + str(j + 1) + ".txt"
                # calculate output after training trainee.py for training and validation
                os.system("python trainee.py -d description.txt < "+trainingset+" > out"+str(j+1)+".txt")
                # calculate Q trainee and validation
                os.system("python validator.py -e "+trainingset+" < out"+str(j+1)+".txt > evaluation")
                f = open ("evaluation", "r")
                q = float(f.readline())
                q_for_k += q
            q_for_k = q_for_k/number_of_split
            qval_for_k=0
            for j in range(number_of_split):
                trainingset = outdir + "/validation_set" + str(j + 1) + ".txt"
                # calculate output after training trainee.py for training and validation
                os.system("python trainee.py -d description.txt < " + trainingset + " > outval" + str(j + 1) + ".txt")
                # calculate Q trainee and validation
                os.system("python validator.py -e " + trainingset + " < outval" + str(j + 1) + ".txt > evaluation")
                f = open("evaluation", "r")
                q = float(f.readline())
                qval_for_k += q
            qval_for_k = qval_for_k / number_of_split
        #create Q table
        fo.write(str(i)+" "+str(q_for_k)+" "+str(qval_for_k)+"\n")

    fo.close()

    # choose best K
    os.system("python validator.py -v validationevaluation.txt > hyperparameter")

    #train with best k
    f = open("hyperparameter", "r")
    degree = int (f.readline())
    os.system("python converter.py -n " + str(dimension) + " -k " + str(degree) + " > description.txt")
    os.system("python trainer.py -t out.txt < description.txt > polynom.txt")

    inp = sys.stdin
    outpset = []

    os.system("python trainee.py -d polynom.txt < "+str(inp)+" > output1")

    #os.system("python scaler.py -a "+inp+" > scaledata.txt") #stored max and min for scalling
    #os.system("python scaler.py -s scaledata.txt < "+inp+".txt > inpscaled.txt") #scaled dataset store in out.txt

    #os.system("python.py trainee.py -d polynom.txt < inpscaled > out.txt")
    #os.system("python.py scaler.py -u data.txt < in.txt > out.txt")


    with open("output1", "r") as set:
        for line in set:
            if line != '\n':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ') ]
                print(l)

    





main()
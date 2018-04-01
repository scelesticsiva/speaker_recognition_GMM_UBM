import python_speech_features
import scipy.io.wavfile as wav
from python_speech_features import mfcc
import os
import subprocess
import csv
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_folder",type = str,\
                        help = "folder where all the audio files are there",required = True)
    parser.add_argument("--csv_file_name",type = str,\
                        help = "name of the mfcc coeffcients file",required = True)
    parser.add_argument("--opt",type = str,\
                        help = "choose <seperate> for creating seperate csv files for each audio file\
                                or <combined> for creating a single csv file",default = "seperate")
    parser.add_argument("--audio_format",type = str,\
                        help = "format of the audio files",default = "wav")
    args = parser.parse_args()
    mfcc_coefficients = extract_mfcc(args)

def extract_mfcc(args):
    os.chdir(args.audio_folder)
    audio_files = os.listdir()
    mfcc_coefficients = []
    flag = 0
    for each_file in audio_files:
        file_name_list = each_file.split(".")
        if file_name_list[-1] == args.audio_format:
            subprocess.run("sox {0}.{1} -r 16000 {2}_16.wav".format(file_name_list[0],file_name_list[-1],file_name_list[0]).split())
            #subprocess.run("ffmpeg -i {0}.{1} {2}_16.wav -ar 16000".format(file_name_list[0],file_name_list[-1],file_name_list[0]).split())
            subprocess.run("rm {0}.{1}".format(file_name_list[0],file_name_list[-1]).split())
            (rate,sig) = wav.read(file_name_list[0]+"_16.wav")
            mfcc_feat = mfcc(sig,rate)
            #print(type(mfcc_feat))
            if args.opt == "seperate":
                save_mfcc(mfcc_feat,args.csv_file_name+file_name_list[0])
            else:
                if flag == 0:
                    mfcc_coefficients = mfcc_feat
                    flag = 1
                else:
                    mfcc_coefficients = np.append(mfcc_coefficients,mfcc_feat,axis = 0)
    if args.opt == "combined":
        save_mfcc(mfcc_coefficients,args.csv_file_name)
    
#def extract_mfcc():
#    os.chdir(ROOT)
#    all_folders = os.listdir()
#    print(all_folders[1:NUM_OF_SUBFOLDERS-1])
#    
#    all_folders = all_folders[1:NUM_OF_SUBFOLDERS]
#    mfcc_coefficients = []
#    for each_folder in all_folders:
#        if each_folder[0] != ".":
#            os.chdir(ROOT+"/"+each_folder)
#            print("--------folder:{0}--------".format(each_folder))
#            all_subfolders = os.listdir()
#            for each_subfolder in all_subfolders:
#                if each_subfolder[0] != ".":
#                    print("--------SUB folder:{0}--------".format(each_subfolder))
#                    os.chdir(ROOT+"/"+each_folder+"/"+each_subfolder)
#                    all_audio_files = os.listdir()
#                    #print(all_audio_files)
#                    for each_file in all_audio_files:
#                        #print(each_file)
#                        file_name = each_file.split(".")[0]
#                        if each_file.split(".")[-1] == "flac":
#                            subprocess.run("ffmpeg -i {0}.flac {0}.wav -ar 16000".format(file_name).split())
#                            (rate,sig) = wav.read(ROOT+"/"+each_folder+"/"+each_subfolder+"/"+file_name+".wav")
#                            mfcc_feat = mfcc(sig,rate)
#                            for feature in mfcc_feat:
#                                mfcc_coefficients.append(feature)  
#    return mfcc_coefficients
                   
def save_mfcc(mfcc_coefficients,file_name): 
    print("saving the mfcc coefficients...")        
    #os.chdir(ROOT_SPEAKER_RECOGNITION)
    with open(file_name+".csv","w") as f:
        writer = csv.writer(f)
        writer.writerows(mfcc_coefficients)
        
if __name__ == "__main__":
    #mfcc_features = extract_mfcc()
    main()
    print("*********extraction done************")
    #save_mfcc(mfcc_features)

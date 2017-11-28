import python_speech_features
import scipy.io.wavfile as wav
from python_speech_features import mfcc
import os
import subprocess
import csv

NUM_OF_SUBFOLDERS = 10
ROOT = "/Users/siva/Documents/verisk/sivark/Downloads/LibriSpeech/dev-clean"
ROOT_SPEAKER_RECOGNITION = "/Users/siva/Documents/speaker_recognition"
MFCC_FILE_NAME = "mfcc_coefficients.csv"

def extract_mfcc():
    os.chdir(ROOT)
    all_folders = os.listdir()
    print(all_folders[1:NUM_OF_SUBFOLDERS-1])
    
    all_folders = all_folders[1:NUM_OF_SUBFOLDERS]
    mfcc_coefficients = []
    for each_folder in all_folders:
        if each_folder[0] != ".":
            os.chdir(ROOT+"/"+each_folder)
            print("--------folder:{0}--------".format(each_folder))
            all_subfolders = os.listdir()
            for each_subfolder in all_subfolders:
                if each_subfolder[0] != ".":
                    print("--------SUB folder:{0}--------".format(each_subfolder))
                    os.chdir(ROOT+"/"+each_folder+"/"+each_subfolder)
                    all_audio_files = os.listdir()
                    #print(all_audio_files)
                    for each_file in all_audio_files:
                        #print(each_file)
                        file_name = each_file.split(".")[0]
                        if each_file.split(".")[-1] == "flac":
                            subprocess.run("ffmpeg -i {0}.flac {0}.wav -ar 16000".format(file_name).split())
                            (rate,sig) = wav.read(ROOT+"/"+each_folder+"/"+each_subfolder+"/"+file_name+".wav")
                            mfcc_feat = mfcc(sig,rate)
                            for feature in mfcc_feat:
                                mfcc_coefficients.append(feature)  
    return mfcc_coefficients
                   
def save_mfcc(mfcc_coefficients): 
    print("saving the mfcc coefficients...")        
    os.chdir(ROOT_SPEAKER_RECOGNITION)
    with open(MFCC_FILE_NAME,"w") as f:
        writer = csv.writer(f)
        writer.writerows(mfcc_coefficients)
        
if __name__ == "__main__":
    mfcc_features = extract_mfcc()
    print("*********extraction done************")
    save_mfcc(mfcc_features)

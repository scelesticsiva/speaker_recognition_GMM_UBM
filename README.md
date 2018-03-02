# speaker_recognition_GMM_UBM
A speaker recognition system which uses GMM-UBM for use in an Android application which helps in monitoring patients suffering from Schizophrenia.

### Extracing MFCC from audio
- - -
To extract MFCC coefficients from audio samples, put all the audio files in a seperate folder and run the following command,
```
python3 extract_mfcc_coefficients.py
--audio_folder <path to the folder which contains audio>
--csv_file_name <name of the csv file that will be created>
--opt combined
```
### Creating Universal Background Model
- - -
To run UBM training run the following code,
```
python3 speaker_recognition.py 
--csv_file <path to MFCC coefficients file> 
--operation ubm
```
### Map adaptation using the created GMM-UBM model
- - -
To run MAP adaptation,
```
python3 speaker_recognition.py 
--csv_file <path to MFCC coefficients file> 
--operation map 
--ubm_file <path to the ubm file created after GMM-UBM model creation>
```

# speaker_recognition_GMM_UBM
A speaker recognition system which uses GMM-UBM for use in an Android application which helps in monitoring patients suffering from Schizophrenia.

To run UBM training run the following code,
```
python3 speaker_recognition.py 
--csv_file <path to MFCC coefficients file> 
--operation ubm
```

To run MAP adaptation,
```
python3 speaker_recognition.py 
--csv_file <path to MFCC coefficients file> 
--operation map 
--ubm_file <path to the ubm file created after GMM-UBM model creation>
```

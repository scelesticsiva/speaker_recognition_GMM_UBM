/***
 * @author - Sivaramakrishnan
 */

import org.jtransforms.fft.DoubleFFT_1D;
import java.io.*;
import java.lang.Math;
import java.util.Arrays;

public class feature_extraction {
    public static void main(String[] args) throws IOException{
        int FFT_SIZE = 512;
        int SAMPLING_RATE = 16000;
        int WINDOW_LENGTH = 5;//seconds
        int FRAME_LENGTH = 25;//milliseconds
        int FRAME_STEP = 10;//milliseconds
        int size_of_window = (int)(WINDOW_LENGTH*SAMPLING_RATE);
        WavFile wav = new WavFile("/Users/siva/Documents/speaker_recognition/prof_voice_samples/audiotest1_16.wav");
        wav.open();
        int[] samples = wav.getSamples(); //The last few samples are zero in the code in github
        double[] samples_ = new double[samples.length];
        for(int j = 0;j < samples.length;j++){
            samples_[j] = (double)samples[j];
        }

        extract_windows ew = new extract_windows(Arrays.copyOfRange(samples_,0,0+size_of_window),FRAME_LENGTH,FRAME_STEP,SAMPLING_RATE);
        extract_spectral_features esf = new extract_spectral_features(ew.getFrame_list(),FFT_SIZE,SAMPLING_RATE);

//        double[] frame_abs = new double[FFT_SIZE];
//        double[] frame_normalized = new double[FFT_SIZE/2-1];
//        DoubleFFT_1D fft = new DoubleFFT_1D(FFT_SIZE);
//        fft.realForwardFull(frame);
//        for(int each_fft = 0,abs_i = 0;each_fft < FFT_SIZE*2-1;each_fft += 2,abs_i++){
//            frame_abs[abs_i] = Math.sqrt((frame[each_fft]*frame[each_fft])+(frame[each_fft+1]*frame[each_fft+1]));
//        }
//        double frame_sum = 0.0;
//        for(int j = 1;j<FFT_SIZE/2;j++){
//            frame_normalized[j-1] = frame_abs[j];
//            frame_sum += frame_abs[j];
//        }
//        for(int k = 0;k<FFT_SIZE/2-1;k++){
//            frame_normalized[k] /= frame_sum;
//        }
//        System.out.println(frame_normalized[0]);
//        System.out.println(frame_normalized[254]);
//        float[] test = new float[20];
//        for(int i = 0;i<10;i++){
//            test[i] = (float)i;
//        }
//        FloatFFT_1D fft = new FloatFFT_1D(10);
//        fft.realForwardFull(test);
//        for(int j = 0;j<20;j++){
//            System.out.println(test[j]);
//        }
    }
}

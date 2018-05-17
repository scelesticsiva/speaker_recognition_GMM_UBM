/***
 * @author - Sivaramakrishnan
 */

import org.jtransforms.fft.DoubleFFT_1D;

public class fft_normalization {

    /***
     * Assigns the FFT SIZE required
     * @param FFT_SIZE Size of FFT which is twice the size of output array "frame normalised"
     */
    public fft_normalization(int FFT_SIZE){
        this.FFT_SIZE = FFT_SIZE;
    }

    /***
     * First copy the array of samples to a larger array(twice the size of FFT), calculate the FFT,find the absolute value
     * and normalise
     * @param samples the actual samples for each frame from the audio
     */
    public void fft_normalize(double[] samples){
        double[] frame = new double[FFT_SIZE*2];
        double[] frame_abs = new double[FFT_SIZE];
        double[] phase_full = new double[FFT_SIZE];
        double fact = 180.0/Math.PI;

        for(int j = 0;j < samples.length;j++){
            frame[j] = samples[j];
        }
        DoubleFFT_1D fft = new DoubleFFT_1D(FFT_SIZE);
        fft.realForwardFull(frame);
        for(int each_fft = 0,abs_i = 0;each_fft < FFT_SIZE*2-1;each_fft += 2,abs_i++){
            frame_abs[abs_i] = Math.sqrt((frame[each_fft]*frame[each_fft])+(frame[each_fft+1]*frame[each_fft+1])); //finding the absolute value of FFT
            phase_full[abs_i] = Math.atan2(frame[each_fft+1],frame[each_fft]) * fact; //finding the phase angle in degrees from the complex number returned by DoubleFFT_1D
        }
        double frame_sum = 0.0;
        for(int j = 1;j<FFT_SIZE/2;j++){
            frame_normalized[j-1] = frame_abs[j]; //copying the values only belonging to positive frequencies
            phase_angle[j-1] = phase_full[j]; //copying the values only belonging to positive frequencies
            frame_sum += frame_abs[j];
        }
        for(int k = 0;k<FFT_SIZE/2-1;k++){
            frame_normalized[k] /= frame_sum; //normalizing
        }
    }

    /***
     * returns the private fft normalised array
     * @return
     */
    double[] getFFTNormalised(){
        return this.frame_normalized;
    }

    double[] getPhase_angle() { return this.phase_angle;}

    int FFT_SIZE = 512;
    double[] frame_normalized = new double[FFT_SIZE/2-1];
    double[] phase_angle = new double[FFT_SIZE/2-1];
}

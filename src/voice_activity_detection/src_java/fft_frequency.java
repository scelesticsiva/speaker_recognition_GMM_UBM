/***
 * @author - Sivaramakrishnan
 */

public class fft_frequency {
    /***
     * Calculates the frequency bins for the required FFT size
     * @param FFT_SIZE Size of the FFT used
     * @param SAMPLING_RATE Sampling rate of the audio
     */
    public fft_frequency(int FFT_SIZE,int SAMPLING_RATE){
        fft_freq = new double[FFT_SIZE/2-1];
        double d_n = (double)FFT_SIZE/SAMPLING_RATE;
        System.out.println(d_n);
        for(int i = 1;i <= fft_freq.length;i++){
            fft_freq[i-1] = (double)i/d_n;
        }
    }

    /***
     * Returns the private double array fft_freq(which is the same as the python code)
     * @return
     */
    public double[] getFFTFrequency(){return fft_freq;}

    private double[] fft_freq;
}

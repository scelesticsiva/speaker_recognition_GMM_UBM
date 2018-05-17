/***
 * @author - Sivaramakrishnan
 */

import java.lang.reflect.Array;
import java.util.ArrayList;

public class extract_spectral_features {

    /***
     * Constructor which finds the normalised fft for each frame in a window
     * @param frame_list Arraylist containing all the frames in a window
     * @param FFT_SIZE FFT size used for calculating the FFT
     */
    public extract_spectral_features(ArrayList<double[]> frame_list,int FFT_SIZE,int SAMPLING_RATE){
        fft_normalised = new ArrayList<>();
        phase_angle = new ArrayList<>();
        for(double[] frame: frame_list){
            fft_normalization fft_norm = new fft_normalization(FFT_SIZE);
            fft_norm.fft_normalize(frame);
            fft_normalised.add(fft_norm.getFFTNormalised());
            phase_angle.add(fft_norm.getPhase_angle());
        }

        fft_frequency fq = new fft_frequency(FFT_SIZE,SAMPLING_RATE);
        fft_freq = fq.getFFTFrequency();

        //Once fft normalization, phase calculation and fft frequency bins are done we can extract all the spectral features
        extractSpectralFlux();
        extractSpectralRolloff();
        extractSpectralCentroid();
        extractBandwidth();
        extractNWPD();
        extractRSE();
    }

    /***
     * Finds the Spectral flux using the normalised FFT values
     */
    public void extractSpectralFlux(){
        spectral_flux = new ArrayList<>();
        for(double[] frame:fft_normalised){
            double sum = 0;
            for(int i = 1;i < frame.length;i++){
                sum += Math.pow(frame[i-1] - frame[i],2);
            }
            spectral_flux.add(sum);
        }
    }

    /***
     * Finds the Spectral Rolloff using normalised FFT values and FFT freqeuncy bins
     */
    public void extractSpectralRolloff(){
        spectral_rolloff = new ArrayList<>();
        for(double[] frame:fft_normalised){
            double[] temp = new double[frame.length];
            temp[0] = frame[0];
            double sum = frame[0],roll_of_percentage;
            int lower_spectral_index = 0;
            for(int j = 1;j < frame.length;j++){
                sum += frame[j];
                temp[j] = temp[j-1] + frame[j];
            }
            roll_of_percentage = sum * SPECTRAL_ROLLOFF_PERCENTAGE;
            for(int i = frame.length-1;i >= 0;i--){
                if(temp[i] < roll_of_percentage) {
                    lower_spectral_index = i;
                    break;
                }
            }
            spectral_rolloff.add(fft_freq[lower_spectral_index]);
        }
    }

    /***
     * Finds the Spectral Centroid for each frame in framelist
     */
    public void extractSpectralCentroid(){
        spectral_centroid = new ArrayList<>();
        double num;
        double den;
        for(int frame = 0;frame < fft_normalised.size();frame++){
            num = 0.0;
            den = 1E-15;
            for(int i = 0;i<fft_normalised.get(frame).length;i++){
                num += fft_freq[i] * (Math.pow(fft_normalised.get(frame)[i],2));
                den += (Math.pow(fft_normalised.get(frame)[i],2));
            }
            spectral_centroid.add(num/den);
        }
    }

    /***
     * Finds the bandwidth for each frame in framelist
     */
    public void extractBandwidth(){
        bandwidth = new ArrayList<>();
        double num;
        double den;
        for(int frame = 0;frame < fft_normalised.size();frame++){
            num = 0.0;
            den = 1E-15;
            for(int i = 0;i<fft_normalised.get(frame).length;i++){
                num += Math.pow(fft_freq[i] - spectral_centroid.get(frame),2) * Math.pow(fft_normalised.get(frame)[i],2);
                den += (Math.pow(fft_normalised.get(frame)[i],2));
            }
            bandwidth.add(num/den);
        }
    }

    /***
     * Find the Normalised Weighted Phase Deviation
     */
    public void extractNWPD(){
        nwpd = new ArrayList<>();
        double nwpd_;
        for(int frame = 0;frame < phase_angle.size(); frame++){
            double[] first_derivative = util.find_derivative(phase_angle.get(frame));
            double[] second_derivative = util.find_derivative(first_derivative); //size of this array is 2 less than the phase angle array because we find the second derivative
            nwpd_ = 0.0;
            for(int i = 0;i<second_derivative.length;i++){
                nwpd_ += fft_normalised.get(frame)[i] * second_derivative[i];
            }
            nwpd.add(nwpd_);
        }
    }


    /***
     * Finds the Relative Spectral Entropy of framelist
     */
    public void extractRSE(){
        rse = new ArrayList<>();
        double rse_;

        int fft_normalised_len = fft_normalised.get(0).length;
        double[] m_prev = util.zeros1D(fft_normalised_len);
        double[] m_curr = new double[fft_normalised_len];
        for(int i = 0;i < fft_normalised_len;i++){
            m_curr[i] = (m_prev[i] * RSE_M_T_PREV) + (fft_normalised.get(0)[i] * RSE_P_T);
        }

        for(int frame = 1;frame < fft_normalised.size();frame++){
            fft_normalised_len = fft_normalised.get(frame).length;
            //m_prev = m_curr;
            for(int k = 0;k < m_prev.length;k++){
                m_prev[k] = m_curr[k];
            }
            for(int i = 0;i < fft_normalised_len;i++){
                m_curr[i] = (m_prev[i] * RSE_M_T_PREV) + (fft_normalised.get(frame)[i] * RSE_P_T);
            }
            rse_ = 0.0;
            for(int j = 0;j < fft_normalised_len; j++){
                rse_ += fft_normalised.get(frame)[j] * (Math.log(fft_normalised.get(frame)[j]) - Math.log(m_prev[j]));
            }
            rse.add(-rse_);
        }
    }

    /***
     * returns the private ArrayList for spectral flux
     * @return
     */
    public ArrayList<Double> getSpectral_flux(){ return spectral_flux;}

    ArrayList<double[]> fft_normalised;
    ArrayList<double[]> phase_angle;
    double[] fft_freq;
    ArrayList<Double> spectral_flux;
    ArrayList<Double> spectral_rolloff;
    ArrayList<Double> spectral_centroid;
    ArrayList<Double> bandwidth;
    ArrayList<Double> nwpd;
    ArrayList<Double> rse;

    private static final double SPECTRAL_ROLLOFF_PERCENTAGE = 0.93;
    private static final double RSE_M_T_PREV = 0.9;
    private static final double RSE_P_T = 0.1;
}

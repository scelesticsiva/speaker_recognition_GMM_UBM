/***
 * @author - Sivaramakrishnan;
 */


import java.util.ArrayList;
import java.util.Arrays;

public class extract_windows {

    /***
     * Extracts frames from each window
     * @param window Array contains the samples from each window
     * @param FRAME_LENGTH Frame length we want in milliseconds
     * @param FRAME_STEP Step size in milliseconds
     * @param SAMPLING_RATE Sampling rate of the audio signal
     */
    public extract_windows(double[] window,int FRAME_LENGTH,int FRAME_STEP,int SAMPLING_RATE){
        int samples_per_frame = (int)((FRAME_LENGTH*Math.pow(10,-3))*SAMPLING_RATE);
        int frame_increment = (int)((FRAME_STEP*Math.pow(10,-3))*SAMPLING_RATE);
        int index = 0;
        while(index <= (window.length - samples_per_frame)){
            frame_list.add(Arrays.copyOfRange(window,index,index+samples_per_frame));
            index += frame_increment;
        }
    }

    /***
     * returns the private variable frame list
     * @return
     */
    public ArrayList<double[]> getFrame_list() {
        return frame_list;
    }

    ArrayList<double[]> frame_list = new ArrayList<>();
    int FRAME_LENGTH;
    int SAMPLING_RATE;
}

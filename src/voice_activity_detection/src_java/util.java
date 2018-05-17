/***
 * @author - Sivaramakrishnan
 */


/***
 * Class for all the util functions
 */
public class util {
    /***
     * Calculated the first derivative of a discrete array by subtracting the current element from next element
     * @param input_array the array to be taken the first derivative
     * @return first derivative array
     */
    static double[] find_derivative(double[] input_array){
        double[] temp = new double[input_array.length-1];
        for(int i = 0;i < input_array.length-1;i++){
            temp[i] = input_array[i+1] - input_array[i];
        }
        return temp;
    }

    /***
     * Creates 1D array with zeroes of input length
     * @param length length of the array to be formed
     * @return array with all zeros of specified length
     */
    static double[] zeros1D(int length){
        double[] temp = new double[length];
        return temp;
    }
}

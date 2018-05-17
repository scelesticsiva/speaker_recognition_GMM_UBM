import java.io.IOException;
import java.io.RandomAccessFile;

public class WavFile  {
    private byte[] byte_samples;
    private int[] samples;
    private int fs;
    private String file_path;
    private int samples_num;
    private int channels_num;


    ///////////////// constructor /////////////////////////////////////////////
    WavFile(String x){
        this.file_path = x;
    }

    /////////////////////////////////////////////////////////////////////////////////////////

    int[] getSamples(){
        return this.samples;
    }

    int getFs(){
        return this.fs;
    }

    ///////////// read samples from mono vaw ///////////////////////////////////////////////////

    void open() throws IOException{

        RandomAccessFile in = null;
        try{
            in = new RandomAccessFile(file_path.toString(), "r");
        }
        catch(Exception myEx)
        {
            //System.out.println("An exception encourred: " + myEx.getMessage());
            myEx.printStackTrace();
            System.exit(1);
        }


        byte_samples = new byte[(int) in.length()];


        in.read(byte_samples, 0, (int) (in.length()));

        this.samples_num = getSamplesNum(byte_samples[40], byte_samples[41], byte_samples[42], byte_samples[43]);
        this.channels_num = getChannelsNum(byte_samples[22], byte_samples[23]);

        //samples = new int[(int) (in.length()-44)/2/this.channels_num];
        samples = new int[this.samples_num/2/this.channels_num];

        this.fs = getFs(byte_samples[24], byte_samples[25], byte_samples[26], byte_samples[27]);

        if(this.channels_num==1){
            for (int i=44;i<(samples_num+44)/2; i++){
                samples[i-44] = toInt(byte_samples[(i-44)*2+45], byte_samples[(i-44)*2+44]);
            }
        }
        else if(this.channels_num==2){
            int j=44;
            for (int i=44;i<(samples_num+44)/2; i+=2){
                samples[j-44] = (toInt(byte_samples[(i-44)*2+45], byte_samples[(i-44)*2+44])+toInt(byte_samples[(i-44)*2+47], byte_samples[(i-44)*2+46]))/2;
                j++;
            }
        }
        else{
            System.out.println("Too much channels, only 1 or 2 are supported");
        }

        in.close();

    }

    //////////////////////////////////////////////////////////////////////////////////////////




    ///////////// FFT //////////////////////////////////////////////////////////////////



    ////////////////////////////////////////////////////////////////////////////////////////////


    //////////// WAV parameters from header ////////////////////////

    private int toInt(byte hb, byte lb){
        return ((int)hb << 8) | ((int)lb & 0xFF);
    }

    private int getFs(byte x1, byte x2, byte x3, byte x4){
        return ((int)x1 & 0xFF | (int)x2 << 8 | (int)x3 << 16 | (int)x4 << 24 );
    }

    private int getSamplesNum(byte x1, byte x2, byte x3, byte x4){
        return ((int)x1 & 0xFF | ((int)x2 << 8) & 0xFF00 | ((int)x3 << 16) & 0xFF0000 | ((int)x4 << 24) & 0xFF000000);
    }

    private int getChannelsNum(byte x1, byte x2){
        return ((int)x2 << 8) | ((int)x1 & 0xFF);
    }

    ////////////////////////////////////////////////////////////////////////////////////////////




}

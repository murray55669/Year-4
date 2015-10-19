/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utility;

import java.awt.Color;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

/**
 *
 * @author s1232200
 */
public class Utilities {
    public ArrayList<LiveData> arrayFromCSV (String filename) throws FileNotFoundException{
        ArrayList<LiveData> liveData = new ArrayList<LiveData>();
        
        Scanner scanner = new Scanner(new File("data/"+filename));
        scanner.useDelimiter("[,\n]");
        
        //Skip first line
        scanner.nextLine();
         
        //Get all tokens and store them in some data structure
        //I am just printing them
        while (scanner.hasNext())
        {
            int ts = Integer.parseInt(scanner.next());
            int rr = Integer.parseInt(scanner.next());
            int os = Integer.parseInt(scanner.next());
            float t = Float.parseFloat(scanner.next());
            int sbp = Integer.parseInt(scanner.next());
            int hr = Integer.parseInt(scanner.next());
            
            liveData.add(new LiveData(ts, rr, os, t, sbp, hr));
        }
         
        //Do not forget to close the scanner 
        scanner.close();
        
        return liveData;
    }
    
    public int genpSEWSScore (int rr, int os, float t, int sbp, int hr) {
        int rrScore = getRRScore(rr);
        int osScore = getOSScore(os);
        int tScore = getTScore(t);
        int sbpScore = getSBPScore(sbp);
        int hrScore = getHRScore(hr);
        
        int total = rrScore + osScore + tScore + sbpScore + hrScore;
        
        return total;
    }
    
    Color pSEWSGreen = new Color(0,255,0);
    Color pSEWSAmber = new Color(255,191,0);
    Color pSEWSRed = new Color(255,0,0);
    Color nan = new Color(255,0,255);
    
    public Color genSEWSColour (int total) {
        if (total >= 0 && total < 2) {
            return pSEWSGreen;
        } else if (total >= 2 && total < 4) {
            return pSEWSAmber;
        } else if (total >= 4) {
            return pSEWSRed;            
        }
        
        return nan;
    }

    public int getRRScore (int value) {
        if (value >= 9 && value <= 20) {
            return 0;
        } else if (value >= 21 && value <= 30) {
            return 1;
        } else if (value >= 31 && value <= 35) {
            return 2;
        } else if (value >= 36 || value <= 8) {
            return 3;
        }
        return -1;
    }
    public int getOSScore (int value) {
        if (value < 85) {
            return 3;
        } else if (value >= 85 && value <= 89) {
            return 2;
        } else if (value >= 90 && value <= 92) {
            return 1;
        } else if (value >= 93) {
            return 0;
        }
        return -1;
    }
    public int getTScore (float value) {
        if (value >= 36 && value < 38) {
            return 0;
        } else if ((value >= 38 && value < 38.5) || (value >= 35 && value < 36)) {
            return 1;
        } else if ((value >= 38.5) || (value >= 34 && value < 35)) {
            return 2;
        } else if (value < 34) {
            return 3;
        }
        return -1;
    }
    public int getSBPScore (int value) {
        if (value <= 69) {
            return 3;
        } else if ((value >= 70 && value <= 79) || value >= 200) {
            return 2;
        } else if (value >= 80 && value <= 99) {
            return 1;
        } else if (value >= 100 && value <= 199) {
            return 0;
        }
        return -1;
    }
    public int getHRScore (int value) {
        if (value >= 50 && value <= 99) {
            return 0;
        } else if ((value >= 100 && value <= 109) || (value >= 40 && value <= 49)) {
            return 1;
        } else if ((value >= 110 && value <= 129) || (value >= 30 && value <= 39)) {
            return 2;
        } else if (value >= 130 || value <= 29) {
            return 3;
        }
        return -1;
    }
}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utility;

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
}

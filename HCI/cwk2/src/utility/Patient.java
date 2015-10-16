/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package utility;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 *
 * @author Qi Zhou
 */
public class Patient {
    private int bedNum;
    private String fname;
    private String lname;
    private String gender;
    private String dob;
    private int lastBR;
    private int lastHR;
    private int lastBPUpper;
    private int lastBPLower;
    
    public ArrayList<LiveData> liveData;
    
    public Patient(int bn, String fnm, String lnm, String g, String d, String fileName/*, int lbr, int lhr, int lbpu, 
            int lbpl*/) {
        this.bedNum = bn;
        this.fname = fnm;
        this.lname = lnm;
        this.gender = g;
        this.dob = d;
        /*
        this.lastBR = lbr;
        this.lastHR = lhr;
        this.lastBPUpper = lbpu;
        this.lastBPLower = lbpl;
        */
        Utilities utils = new Utilities();
        try {
            this.liveData = utils.arrayFromCSV(fileName);
        } catch (FileNotFoundException ex) {
            System.out.println(ex.toString());
        }
    }

    public int getBedNumber() {
        return bedNum;
    }
    
    public String getFistName() {
        return fname;
    }

    public String getLastName() {
        return lname;
    }
    
    public String getGender() {
        return gender;
    }

    public String getDOB() {
        return dob;
    }

    
    
    public int getLastBR() {
        return lastBR;
    }
    
    public int getLastHR() {
        return lastHR;
    }

    public int getLastBPUpper() {
        return lastBPUpper;
    }
    
    public int getLastBPLower() {
        return lastBPLower;
    }
}

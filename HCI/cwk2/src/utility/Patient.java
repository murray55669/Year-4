/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package utility;

import java.awt.Color;
import java.io.FileNotFoundException;
import java.util.ArrayList;

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
    
    private int state = 0;
    
    private ArrayList<LiveData> liveData;
    
    private Utilities utils;
    
    public Patient(int bn, String fnm, String lnm, String g, String d, String fileName) {
        this.bedNum = bn;
        this.fname = fnm;
        this.lname = lnm;
        this.gender = g;
        this.dob = d;
        
        utils = new Utilities();
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
    
    public void setState (int state) {
        this.state = state;
    }
    public int getState () {
        return this.state;
    }
    
    public LiveData getLiveData (int time) {
        return liveData.get(time/5);
    }
    public Color getColour (int time) {
        LiveData data = this.getLiveData(time);
        int pSEWS = utils.genpSEWSScore(data.rr, data.os, data.t, data.sbp, data.hr);
        int SEWS = pSEWS + this.state;
        return utils.genSEWSColour(SEWS);
    }
}

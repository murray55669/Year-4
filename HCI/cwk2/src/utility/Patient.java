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
    
    private int state = -1;
    private boolean flagged = false;
    private boolean checked = false;
    
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
    
    public String getFullName () {
        return fname + " " + lname;
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
    
    public boolean getChecked () {
        return this.checked;
    }
    public void setChecked () {
        this.checked = true;
    }
    public void clearChecked () {
        this.checked = false;
    }
    
    public LiveData getLiveData (int time) {
        return liveData.get(time/500);
    }
    public ArrayList<LiveData> getAllLiveData () {
        return this.liveData;
    }
    public ArrayList<LiveData> getLiveDatahistory (int time) {
        //limit to an hour
        ArrayList<LiveData> choppedData = new ArrayList<LiveData>();
        
        int minStep = (time/100) - 3600;
        if (minStep < 0) {
            minStep = 0;
        }
        int maxStep = time/500;
        for (int i = minStep; i < maxStep; i++) {
            choppedData.add(liveData.get(i));
        }
        
        return choppedData;
    }
    public Color getColour (int time) {
        return utils.genSEWSColour(getSEWS(time));
    }
    public int getSEWS (int time) {
        LiveData data = this.getLiveData(time);
        int pSEWS = utils.genpSEWSScore(data.rr, data.os, data.t, data.sbp, data.hr);
        int SEWS = pSEWS;
        if (this.state >= 0) {
            SEWS = pSEWS + this.state;
        }
        return SEWS;
    }
    
    public boolean testAndFlag (int time) {
        LiveData data = this.getLiveData(time);
        int pSEWS = utils.genpSEWSScore(data.rr, data.os, data.t, data.sbp, data.hr);
        if (pSEWS >= 2) {
            this.flagged = true;
        }
        return this.flagged;
    }
    public void clearFlagged () {
        this.flagged = false;
    }
}

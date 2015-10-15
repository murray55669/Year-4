/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package patientview;

/**
 *
 * @author s1232200
 */
public class LiveData {
    
    public int ts;
    public int rr;
    public int os;
    public float t;
    public int sbp;
    public int hr;

    LiveData(int ts, int rr, int os, float t, int sbp, int hr) {
        this.ts = ts;
        this.rr = rr;
        this.os = os;
        this.t = t;
        this.sbp = sbp;
        this.hr = hr;        
    }
}

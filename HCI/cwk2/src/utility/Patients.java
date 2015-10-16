/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utility;

import java.util.ArrayList;

/**
 *
 * @author s1232200
 */
public class Patients {
    
    public ArrayList<Patient> patientList = new ArrayList<Patient>();
    
    public Patients () {
        patientList.add(new Patient(1001, "Alice", "Bailey", "F", "1958-10-12", "Alice_Bailey_20141011091022.csv"));
        patientList.add(new Patient(1002, "Charlie", "Dean", "M", "1962-03-02", "Charlie_Dean_20141013103445.csv"));
        patientList.add(new Patient(1003, "Elise", "Foster", "F", "1971-01-02", "Elise_Foster_20141013122956.csv"));
        patientList.add(new Patient(1004, "Grace", "Hughes", "F", "1975-05-14", "Grace_Hughes_20141013161902.csv"));
        patientList.add(new Patient(1005, "Ian", "Jones", "M", "1966-12-03", "Ian_Jones_20141013142915.csv"));
        patientList.add(new Patient(1006, "Kelly", "Lawrence", "F", "1969-03-16", "Kelly_Lawrence_201410141532.csv"));        
    }
    
    public Patient getPatient(int bedNum) {
        for (int i = 0; i < patientList.size(); i++) {
            if (patientList.get(i).getBedNumber() == bedNum) {
                return patientList.get(i);
            }
        }
        System.out.println("Patient "+String.valueOf(bedNum)+" not found!");
        return null;
    }
}

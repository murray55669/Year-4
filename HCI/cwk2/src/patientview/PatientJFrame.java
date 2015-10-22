/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package patientview;

import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Random;
import javax.swing.Timer;

import java.awt.Color;
import java.io.File;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.swing.ImageIcon;

import utility.LiveData;
import utility.Patient;
import utility.Patients;
import utility.Utilities;

/**
 *
 * @author Qi Zhou
 */
public class PatientJFrame extends javax.swing.JFrame {

    private Timer timer;
    private int timerCSeconds;
    
    private Patients patients;
    private int bedNum;
    private Patient thisPatient;
    
    private Utilities utils = new Utilities();
    
    Clip click;

    /**
     * Creates new form PatientJFrame
     */
    public PatientJFrame(int bedNum, int time, Patients patients) {
        initComponents();
        
        //set window in the center of the screen
        //Get the size of the screen
        Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
        //Determine the new location of the window
        int w = this.getSize().width;
        int h = this.getSize().height;
        int x = (dim.width - w) / 2;
        int y = (dim.height - h) / 2;
        //Move the window
        this.setLocation(x, y);
        
        //Load click sound
        try {
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("sounds/click.wav").getAbsoluteFile());
            click = AudioSystem.getClip();
            click.open(audioInputStream);
        } catch (Exception ex) {
            System.out.println(ex.toString());
        } 
        
        //Get patient
        this.patients = patients;
        this.bedNum = bedNum;
        thisPatient = patients.getPatient(bedNum);
        
        //fill titles
        patientNameField.setText(thisPatient.getFullName());
        wardNumField.setText("W001");
        bedNumField.setText(String.valueOf(bedNum));
        dobField.setText(thisPatient.getDOB());
        
        ImageIcon maleIcon = new ImageIcon("images/male.png");
        ImageIcon femaleIcon = new ImageIcon("images/female.png");
        if ("F".equals(thisPatient.getGender())) {
            genderIcon.setIcon(femaleIcon);
        } else {
            genderIcon.setIcon(maleIcon);
        }
        
        //Set background colour
        this.getContentPane().setBackground(new Color(240,240,240));
        
        rrIndicator.setOpaque(true);
        osIndicator.setOpaque(true);
        tIndicator.setOpaque(true);
        sbpIndicator.setOpaque(true);
        hrIndicator.setOpaque(true);
        pSEWSIndicator.setOpaque(true);
                
        //set focus on back button
        jButton_changeView.requestFocus();
           
        //set timer
        timerCSeconds = time;
        
        LiveData initialData = thisPatient.getLiveData(timerCSeconds);
        displayData(initialData.rr,initialData.os,initialData.t,initialData.sbp,initialData.hr);
        if (timer == null) {
            timer = new Timer(10, new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    // do it every 10 msecond
                    Calendar cal = Calendar.getInstance();
                    cal.getTime();
                    SimpleDateFormat sdf = new SimpleDateFormat("YYYY-MM-dd HH:mm:ss");
                    jLabel_systemTime.setText(sdf.format(cal.getTime()));
                    // do it every 5 seconds
                    if (timerCSeconds % 500 == 0) {                        
                        LiveData timedData = thisPatient.getLiveData(timerCSeconds);
                        
                        int br = timedData.rr;
                        int spo2 = timedData.os;
                        float temp = timedData.t;
                        int systolic = timedData.sbp;
                        int hr = timedData.hr;
                        
                        displayData(br,spo2,temp,systolic,hr);
                    }
                    timerCSeconds++;
                }
            });
        }

        if (timer.isRunning() == false) {
            timer.start();
        }
    }
    
    private void displayData(int rr, int os, float t, int sbp, int hr) {
        rrLabel.setText(Integer.toString(rr)+" breaths/min");
        rrIndicator.setBackground(genRedColour(rr, 0));
        
        osLabel.setText(Integer.toString(os)+"%");
        osIndicator.setBackground(genRedColour(os, 1));
        
        tLabel.setText(Float.toString(t)+" °C");
        tIndicator.setBackground(genRedColour(t, 2));
        
        sbpLabel.setText(Integer.toString(sbp)+" mmHg");
        sbpIndicator.setBackground(genRedColour(sbp, 3));
        
        hrLabel.setText(Integer.toString(hr)+" beats/min");
        hrIndicator.setBackground(genRedColour(hr, 4));
        
        int score = utils.genpSEWSScore(rr, os, t, sbp, hr);
        pSEWSLabel.setText(String.valueOf(score));
        
        Color pSEWSColour = utils.genSEWSColour(score);
        pSEWSIndicator.setBackground(pSEWSColour);
    }
    
    Color zeroRed = new Color(230,255,255);
    Color oneRed = new Color(255,170,170);
    Color twoRed = new Color(255,85,85);
    Color threeRed = new Color(255,0,0);
    Color nan = new Color(255,0,255);
    private Color genRedColour(int value, int mode) {
        /*
        Enumerating things is hard:
        0:breathing rate
        1:oxygen saturation
        2:temperature (FLOAT)
        3:systolic blood pressure
        4:heart rate
        */
        int result;
        switch(mode) {
            case 0:
                result = utils.getRRScore(value);
                break;
            case 1:
                result = utils.getOSScore(value);
                break;
            case 3:
                result = utils.getSBPScore(value);
                break;
            case 4:
                result = utils.getHRScore(value);
                break;
            default:
                return nan;
        }
        return getRedColour(result);
    }
    private Color genRedColour(float value, int mode) {
        //Java, yo
        int result = utils.getTScore(value);
        return getRedColour(result);
    }
    private Color getRedColour(int result) {
        switch(result) {
            case 0:
                return zeroRed;
            case 1:
                return oneRed;
            case 2:
                return twoRed;
            case 3:
                return threeRed;
            default:
                return nan;
        }
    }
    

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jLabel9 = new javax.swing.JLabel();
        jButton_changeView = new javax.swing.JButton();
        jLabel_systemTime = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        bedNumField = new javax.swing.JLabel();
        jPanel_readings = new javax.swing.JPanel();
        jLabel6 = new javax.swing.JLabel();
        rrIndicator = new javax.swing.JLabel();
        rrLabel = new javax.swing.JLabel();
        jLabel7 = new javax.swing.JLabel();
        osIndicator = new javax.swing.JLabel();
        osLabel = new javax.swing.JLabel();
        jLabel8 = new javax.swing.JLabel();
        tIndicator = new javax.swing.JLabel();
        tLabel = new javax.swing.JLabel();
        jLabel10 = new javax.swing.JLabel();
        sbpIndicator = new javax.swing.JLabel();
        sbpLabel = new javax.swing.JLabel();
        jLabel11 = new javax.swing.JLabel();
        hrIndicator = new javax.swing.JLabel();
        hrLabel = new javax.swing.JLabel();
        jSeparator1 = new javax.swing.JSeparator();
        jSeparator2 = new javax.swing.JSeparator();
        jSeparator3 = new javax.swing.JSeparator();
        jSeparator4 = new javax.swing.JSeparator();
        graphButton = new javax.swing.JButton();
        jPanel_title = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        patientNameField = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        dobField = new javax.swing.JLabel();
        genderIcon = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        wardNumField = new javax.swing.JLabel();
        jPanel1 = new javax.swing.JPanel();
        pSEWSIndicator = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        pSEWSLabel = new javax.swing.JLabel();

        jLabel9.setText("jLabel9");

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setBackground(new java.awt.Color(254, 254, 254));

        jButton_changeView.setText("Back");
        jButton_changeView.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton_changeViewActionPerformed(evt);
            }
        });

        jLabel_systemTime.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel_systemTime.setText("TIME");

        jLabel3.setText("- Bed");

        bedNumField.setText("jLabel");

        jPanel_readings.setBackground(new java.awt.Color(254, 254, 254));

        jLabel6.setText("Respiratory rate");

        rrIndicator.setBackground(new java.awt.Color(254, 254, 254));
        rrIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        rrIndicator.setMaximumSize(new java.awt.Dimension(16, 16));
        rrIndicator.setMinimumSize(new java.awt.Dimension(16, 16));
        rrIndicator.setPreferredSize(new java.awt.Dimension(16, 16));

        rrLabel.setBackground(new java.awt.Color(224, 224, 224));
        rrLabel.setText("Loading...");

        jLabel7.setText("Oxygen saturation");

        osIndicator.setBackground(new java.awt.Color(254, 254, 254));
        osIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        osIndicator.setMaximumSize(new java.awt.Dimension(16, 16));
        osIndicator.setMinimumSize(new java.awt.Dimension(16, 16));
        osIndicator.setPreferredSize(new java.awt.Dimension(24, 24));

        osLabel.setText("Loading...");

        jLabel8.setText("Temperature");
        jLabel8.setPreferredSize(new java.awt.Dimension(159, 16));

        tIndicator.setBackground(new java.awt.Color(254, 254, 254));
        tIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        tIndicator.setMaximumSize(new java.awt.Dimension(16, 16));
        tIndicator.setMinimumSize(new java.awt.Dimension(16, 16));
        tIndicator.setPreferredSize(new java.awt.Dimension(24, 24));

        tLabel.setBackground(new java.awt.Color(224, 224, 224));
        tLabel.setText("Loading...");

        jLabel10.setText("Systolic blood pressure");

        sbpIndicator.setBackground(new java.awt.Color(254, 254, 254));
        sbpIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        sbpIndicator.setMaximumSize(new java.awt.Dimension(16, 16));
        sbpIndicator.setMinimumSize(new java.awt.Dimension(16, 16));
        sbpIndicator.setPreferredSize(new java.awt.Dimension(24, 24));

        sbpLabel.setText("Loading...");

        jLabel11.setText("Heart rate");
        jLabel11.setPreferredSize(new java.awt.Dimension(159, 16));

        hrIndicator.setBackground(new java.awt.Color(254, 254, 254));
        hrIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        hrIndicator.setMaximumSize(new java.awt.Dimension(16, 16));
        hrIndicator.setMinimumSize(new java.awt.Dimension(16, 16));
        hrIndicator.setPreferredSize(new java.awt.Dimension(24, 24));

        hrLabel.setText("Loading...");

        graphButton.setText("View History (Last Hour)");
        graphButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                graphButtonActionPerformed(evt);
            }
        });

        org.jdesktop.layout.GroupLayout jPanel_readingsLayout = new org.jdesktop.layout.GroupLayout(jPanel_readings);
        jPanel_readings.setLayout(jPanel_readingsLayout);
        jPanel_readingsLayout.setHorizontalGroup(
            jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel_readingsLayout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(graphButton, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(jSeparator4)
                    .add(jSeparator3)
                    .add(jSeparator2)
                    .add(jSeparator1)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, jPanel_readingsLayout.createSequentialGroup()
                        .add(jLabel6, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 159, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(rrIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(rrLabel, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .add(jPanel_readingsLayout.createSequentialGroup()
                        .add(jLabel7, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 159, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(osIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(osLabel, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .add(jPanel_readingsLayout.createSequentialGroup()
                        .add(jLabel8, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 159, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(tIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(26, 26, 26)
                        .add(tLabel, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .add(jPanel_readingsLayout.createSequentialGroup()
                        .add(jLabel10, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 159, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(sbpIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(sbpLabel, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, jPanel_readingsLayout.createSequentialGroup()
                        .add(jLabel11, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 159, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(hrIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(27, 27, 27)
                        .add(hrLabel, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel_readingsLayout.setVerticalGroup(
            jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel_readingsLayout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING, false)
                    .add(rrLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, rrIndicator, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(jLabel6, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jSeparator1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 5, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(osLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel7, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(osIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jSeparator2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 5, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(tLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel8, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(tIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jSeparator3, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 4, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                        .add(jLabel10, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .add(sbpIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, sbpLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jSeparator4, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 4, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jPanel_readingsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(jLabel11, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(hrIndicator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, hrLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 24, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(graphButton, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .add(8, 8, 8))
        );

        jPanel_title.setBackground(new java.awt.Color(254, 254, 254));

        jLabel1.setText("Patient");

        patientNameField.setText("jLabel");

        jLabel4.setText("DoB:");

        dobField.setText("jLabel");

        org.jdesktop.layout.GroupLayout jPanel_titleLayout = new org.jdesktop.layout.GroupLayout(jPanel_title);
        jPanel_title.setLayout(jPanel_titleLayout);
        jPanel_titleLayout.setHorizontalGroup(
            jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel_titleLayout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(jLabel4)
                    .add(jLabel1))
                .add(18, 18, 18)
                .add(jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(patientNameField, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 100, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(dobField, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 100, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 24, Short.MAX_VALUE)
                .add(genderIcon, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 40, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        jPanel_titleLayout.setVerticalGroup(
            jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel_titleLayout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(genderIcon, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(jPanel_titleLayout.createSequentialGroup()
                        .add(jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                            .add(jLabel1)
                            .add(patientNameField))
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(jPanel_titleLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                            .add(jLabel4)
                            .add(dobField, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 16, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                        .add(0, 0, Short.MAX_VALUE)))
                .add(7, 7, 7))
        );

        jLabel2.setText("Ward");

        wardNumField.setText("jLabel");

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));

        pSEWSIndicator.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        jLabel5.setText("pSEWS:");

        pSEWSLabel.setText("0");
        pSEWSLabel.setHorizontalTextPosition(javax.swing.SwingConstants.RIGHT);

        org.jdesktop.layout.GroupLayout jPanel1Layout = new org.jdesktop.layout.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel1Layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(pSEWSLabel, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 19, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel5))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(pSEWSIndicator, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .add(jPanel1Layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING, false)
                    .add(pSEWSIndicator, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(jPanel1Layout.createSequentialGroup()
                        .add(jLabel5)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(pSEWSLabel)))
                .add(0, 9, Short.MAX_VALUE))
        );

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(jPanel_readings, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                        .add(jButton_changeView)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(jLabel2)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(wardNumField)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(jLabel3)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(bedNumField)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 84, Short.MAX_VALUE)
                        .add(jLabel_systemTime, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 143, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                    .add(layout.createSequentialGroup()
                        .add(jPanel_title, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(jPanel1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(jLabel3)
                    .add(bedNumField, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 28, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jLabel2)
                    .add(jButton_changeView)
                    .add(wardNumField)
                    .add(jLabel_systemTime, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(jPanel_title, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jPanel1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .add(7, 7, 7)
                .add(jPanel_readings, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void jButton_changeViewActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton_changeViewActionPerformed
        // TODO add your handling code here:
        click.start();
        //dispose current window
        this.dispose();
        //open the Ward-View
        WardJFrame wardframe = new WardJFrame(timerCSeconds, this.patients);
        wardframe.setVisible(true);
    }//GEN-LAST:event_jButton_changeViewActionPerformed

    private void graphButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_graphButtonActionPerformed
        // TODO add your handling code here:
        click.start();
        this.dispose();
        HistoryJFrame historyFrame = new HistoryJFrame(this.bedNum, timerCSeconds, this.patients);
        historyFrame.setVisible(true);
    }//GEN-LAST:event_graphButtonActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;


                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(PatientJFrame.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(PatientJFrame.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(PatientJFrame.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(PatientJFrame.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new PatientJFrame(0, 0, null).setVisible(true);
            }
        });
    }

    /**
     * Create a random int number
     */
    public int generateReading(int kind) {
        Random random = new Random();
        int returnReading = 0;
        switch (kind) {
            case 0: //Breathing Rate
                returnReading = random.nextInt(35) + 5 + 1;
                break;
            case 1: //SPO2
                returnReading = random.nextInt(20) + 80 + 1;
                break;
            case 2: //Blood Pressure - SYSTOLIC
                returnReading = random.nextInt(150) + 60 + 1;
                break;
            case 3: //Heart Rate
                returnReading = random.nextInt(20) + 140 + 1;
                break;
            default:
                break;
        }
        return returnReading;
    }

    /**
     * Create a random float number - body temp
     */
    public float generateReading(float kind) {
        Random random = new Random();
        return random.nextFloat() * 6 + 33;
    }
    
    /**
     * Create a random int number in a range - you might want to use this for testing
     */
    public int generateReadingInRange(int lower, int upper) {
        Random random = new Random();
        return random.nextInt(upper - lower) + lower + 1;
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel bedNumField;
    private javax.swing.JLabel dobField;
    private javax.swing.JLabel genderIcon;
    private javax.swing.JButton graphButton;
    private javax.swing.JLabel hrIndicator;
    private javax.swing.JLabel hrLabel;
    private javax.swing.JButton jButton_changeView;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JLabel jLabel_systemTime;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel_readings;
    private javax.swing.JPanel jPanel_title;
    private javax.swing.JSeparator jSeparator1;
    private javax.swing.JSeparator jSeparator2;
    private javax.swing.JSeparator jSeparator3;
    private javax.swing.JSeparator jSeparator4;
    private javax.swing.JLabel osIndicator;
    private javax.swing.JLabel osLabel;
    private javax.swing.JLabel pSEWSIndicator;
    private javax.swing.JLabel pSEWSLabel;
    private javax.swing.JLabel patientNameField;
    private javax.swing.JLabel rrIndicator;
    private javax.swing.JLabel rrLabel;
    private javax.swing.JLabel sbpIndicator;
    private javax.swing.JLabel sbpLabel;
    private javax.swing.JLabel tIndicator;
    private javax.swing.JLabel tLabel;
    private javax.swing.JLabel wardNumField;
    // End of variables declaration//GEN-END:variables
}

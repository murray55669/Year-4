/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package patientview;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import javax.swing.ImageIcon;
import javax.swing.Timer;
import utility.Patient;
import utility.Patients;
import java.util.ArrayList;

import javax.swing.JLabel;
import javax.swing.JComboBox;
import javax.swing.JButton;

/**
 *
 * @author s1232200
 */
public class WardJFrame extends javax.swing.JFrame {
    
    private Timer timer;
    private int timerCSeconds;
    
    private Patients patients = new Patients();
    
    ArrayList<JLabel> SEWSIndicators;
    ArrayList<JLabel> actionLabels;
    ArrayList<JLabel> bedNames;
    ArrayList<JButton> okButtons;
    ArrayList<JButton> bedButtons;
    ArrayList<JComboBox> bedStates;

    /**
     * Creates new form WardJFrame
     */
    public WardJFrame(int time) {
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
        
        //Set background colour
        this.getContentPane().setBackground(new Color(240,240,240));
        ImageIcon lBed = new ImageIcon("images/bedl.png");
        ImageIcon rBed = new ImageIcon("images/bedr.png");
        
        SEWSIndicators = new ArrayList<JLabel>() {
            {
                add(SEWSIndicator1);
                add(SEWSIndicator2);
                add(SEWSIndicator3);
                add(SEWSIndicator4);
                add(SEWSIndicator5);
                add(SEWSIndicator6);
            }
        };
        actionLabels = new ArrayList<JLabel>() {
            {
               add(actionLabel1);
               add(actionLabel2);
               add(actionLabel3);
               add(actionLabel4);
               add(actionLabel5);
               add(actionLabel6);
            }  
        };
        bedNames = new ArrayList<JLabel>() {
            {
               add(bed1Name);               
               add(bed2Name);
               add(bed3Name);
               add(bed4Name);
               add(bed5Name);
               add(bed6Name);
            }  
        };
        okButtons = new ArrayList<JButton>() {
            {
                add(okButton1);
                add(okButton2);
                add(okButton3);
                add(okButton4);
                add(okButton5);
                add(okButton6);
            }
        };
        bedButtons = new ArrayList<JButton>() {
            {
                add(bed1);
                add(bed2);
                add(bed3);
                add(bed4);
                add(bed5);
                add(bed6);
            }
        };
        bedStates = new ArrayList<JComboBox>() {
            {
                add(bed1State);
                add(bed2State);
                add(bed3State);
                add(bed4State);
                add(bed5State);
                add(bed6State);
            }
        };
        
        //Set bed icons
        for (int i = 0; i < bedButtons.size(); i++) {
            if (i % 2 == 0) {
                bedButtons.get(i).setIcon(lBed);
            } else {
                bedButtons.get(i).setIcon(rBed);
            }
        }
        //Set names
        for (int i = 0; i < bedNames.size(); i++) {
            bedNames.get(i).setText(patients.getPatient(i+1001).getFullName());
        }
        
        for (JLabel label : SEWSIndicators) {
            label.setOpaque(true);
        }
        
        //Hide stuff
        for (JLabel label : actionLabels) {
            label.setVisible(false);
        }
        for (JComboBox box : bedStates) {
            box.setVisible(false);
        }
        for (JButton button : okButtons) {
            button.setVisible(false);
        }
        
        //set focus on exit button
        jButton_changeView.requestFocus();
        
        wardNumField.setText(patients.getWardNum());
        
        timerCSeconds = time;
        
        displayData();
        if (timer == null) {
            timer = new Timer(10, new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    // do it every 10 msecond
                    Calendar cal = Calendar.getInstance();
                    cal.getTime();
                    SimpleDateFormat sdf = new SimpleDateFormat("YYYY-MM-dd HH:mm:ss");
                    jLabel_systemTime.setText(sdf.format(cal.getTime()));
                    
                    displayData();
                    
                    timerCSeconds++; 
                }
            });
        }

        if (timer.isRunning() == false) {
            timer.start();
        }
    }
    
    private void displayData () {    
        //Set names
        for (int i = 0; i < SEWSIndicators.size(); i++) {
            SEWSIndicators.get(i).setBackground(patients.getPatient(i+1001).getColour(timerCSeconds));
        }      
        
        for (int i = 1; i < patients.getPatientCount()+1; i++) {
            int bedNum = i + 1000;
            boolean isFlagged = patients.getPatient(bedNum).checkAndFlag(timerCSeconds);
            if (isFlagged && i == 1) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            } else if (isFlagged && i == 2) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            } else if (isFlagged && i == 3) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            } else if (isFlagged && i == 4) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            } else if (isFlagged && i == 5) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            } else if (isFlagged && i == 6) {
                actionLabel1.setVisible(false);
                bed1State.setVisible(false);
            }
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

        wardNumField = new javax.swing.JLabel();
        jButton_changeView = new javax.swing.JButton();
        jLabel_systemTime = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        bed1 = new javax.swing.JButton();
        bed2 = new javax.swing.JButton();
        bed3 = new javax.swing.JButton();
        bed4 = new javax.swing.JButton();
        bed5 = new javax.swing.JButton();
        bed6 = new javax.swing.JButton();
        bed1State = new javax.swing.JComboBox();
        bed2State = new javax.swing.JComboBox();
        bed3State = new javax.swing.JComboBox();
        bed4State = new javax.swing.JComboBox();
        bed5State = new javax.swing.JComboBox();
        bed6State = new javax.swing.JComboBox();
        SEWSIndicator1 = new javax.swing.JLabel();
        SEWSIndicator5 = new javax.swing.JLabel();
        SEWSIndicator3 = new javax.swing.JLabel();
        SEWSIndicator2 = new javax.swing.JLabel();
        SEWSIndicator6 = new javax.swing.JLabel();
        SEWSIndicator4 = new javax.swing.JLabel();
        actionLabel1 = new javax.swing.JLabel();
        okButton1 = new javax.swing.JButton();
        bed1Name = new javax.swing.JLabel();
        bed2Name = new javax.swing.JLabel();
        bed3Name = new javax.swing.JLabel();
        actionLabel3 = new javax.swing.JLabel();
        okButton3 = new javax.swing.JButton();
        bed4Name = new javax.swing.JLabel();
        actionLabel4 = new javax.swing.JLabel();
        okButton4 = new javax.swing.JButton();
        actionLabel2 = new javax.swing.JLabel();
        okButton2 = new javax.swing.JButton();
        bed5Name = new javax.swing.JLabel();
        actionLabel5 = new javax.swing.JLabel();
        okButton5 = new javax.swing.JButton();
        bed6Name = new javax.swing.JLabel();
        actionLabel6 = new javax.swing.JLabel();
        okButton6 = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        wardNumField.setText("jLabel");

        jButton_changeView.setText("Exit");
        jButton_changeView.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton_exitActionPerformed(evt);
            }
        });

        jLabel_systemTime.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel_systemTime.setText("TIME");

        jLabel2.setText("Ward");

        bed1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bedClicked(evt);
            }
        });

        bed1State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        bed2State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        bed3State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        bed4State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        bed5State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        bed6State.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Alert", "Verbal", "Pain", "Unresponsive" }));

        SEWSIndicator1.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        SEWSIndicator5.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        SEWSIndicator3.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        SEWSIndicator2.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        SEWSIndicator6.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        SEWSIndicator4.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        actionLabel1.setText("No action needed.");

        okButton1.setText("OK");
        okButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                okButton1ActionPerformed(evt);
            }
        });

        bed1Name.setText("jLabel1");

        bed2Name.setText("jLabel1");

        bed3Name.setText("jLabel3");

        actionLabel3.setText("No action needed.");

        okButton3.setText("OK");
        okButton3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                okButton3ActionPerformed(evt);
            }
        });

        bed4Name.setText("jLabel4");

        actionLabel4.setText("No action needed,");

        okButton4.setText("OK");

        actionLabel2.setText("No action needed,");

        okButton2.setText("OK");

        bed5Name.setText("jLabel7");

        actionLabel5.setText("No action needed,");

        okButton5.setText("OK");
        okButton5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                okButton5ActionPerformed(evt);
            }
        });

        bed6Name.setText("jLabel9");

        actionLabel6.setText("No action needed,");

        okButton6.setText("OK");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(bed5Name, javax.swing.GroupLayout.DEFAULT_SIZE, 164, Short.MAX_VALUE)
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                .addComponent(okButton3, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(bed3State, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(actionLabel3, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                    .addComponent(bed3, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(SEWSIndicator3, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                .addComponent(okButton5, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(bed5State, javax.swing.GroupLayout.Alignment.LEADING, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                    .addComponent(bed5, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(SEWSIndicator5, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addComponent(actionLabel5, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 132, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                    .addComponent(bed1, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(SEWSIndicator1, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addComponent(actionLabel1, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(bed1State, javax.swing.GroupLayout.Alignment.LEADING, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(bed1Name, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(okButton1, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                            .addComponent(bed3Name, javax.swing.GroupLayout.PREFERRED_SIZE, 132, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(139, 139, 139)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(bed2Name, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                    .addComponent(okButton6, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(bed6State, javax.swing.GroupLayout.Alignment.LEADING, 0, 132, Short.MAX_VALUE)
                                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                            .addComponent(bed6Name, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                                .addComponent(SEWSIndicator6, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(bed6, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                            .addComponent(actionLabel2, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                                .addComponent(SEWSIndicator2, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(bed2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                            .addComponent(bed4Name, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                                .addComponent(SEWSIndicator4, javax.swing.GroupLayout.PREFERRED_SIZE, 20, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(bed4, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                            .addComponent(actionLabel4, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addComponent(bed4State, javax.swing.GroupLayout.Alignment.LEADING, 0, 132, Short.MAX_VALUE)
                                            .addComponent(okButton4, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addComponent(bed2State, javax.swing.GroupLayout.Alignment.LEADING, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                            .addComponent(okButton2, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                        .addComponent(actionLabel6, javax.swing.GroupLayout.PREFERRED_SIZE, 124, javax.swing.GroupLayout.PREFERRED_SIZE)))
                                .addGap(0, 31, Short.MAX_VALUE)))
                        .addGap(12, 12, 12))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jButton_changeView)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(wardNumField)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(jLabel_systemTime, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap())))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel_systemTime, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jLabel2)
                    .addComponent(jButton_changeView)
                    .addComponent(wardNumField))
                .addGap(9, 9, 9)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(bed1Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(bed1, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(SEWSIndicator1, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed1State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton1)
                        .addGap(34, 34, 34)
                        .addComponent(bed3Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(SEWSIndicator3, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(bed3, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel3)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed3State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton3))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(bed2Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(bed2, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(SEWSIndicator2, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed2State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton2)
                        .addGap(34, 34, 34)
                        .addComponent(bed4Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(SEWSIndicator4, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(bed4, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel4)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed4State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton4)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 37, Short.MAX_VALUE)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(bed5Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(bed5, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(SEWSIndicator5, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel5)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed5State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton5))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(bed6Name)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(SEWSIndicator6, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(bed6, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(actionLabel6)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bed6State, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(okButton6)))
                .addGap(30, 30, 30))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void jButton_exitActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton_exitActionPerformed

         // TODO add your handling code here:
        System.exit(0);
    }//GEN-LAST:event_jButton_exitActionPerformed

    private void bedClicked(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_bedClicked
        // TODO add your handling code here:
        int bedNum = 0;
        if (evt.getSource() == bed1){
            bedNum = 1001;
        } else if (evt.getSource() == bed2){
            bedNum = 1002;
        } else if (evt.getSource() == bed3){
            bedNum = 1003;
        } else if (evt.getSource() == bed4){
            bedNum = 1004;
        } else if (evt.getSource() == bed5){
            bedNum = 1005;
        } else if (evt.getSource() == bed6){
            bedNum = 1006;
        }
        this.dispose();
        PatientJFrame patientFrame = new PatientJFrame(bedNum, timerCSeconds);
        patientFrame.setVisible(true);
    }//GEN-LAST:event_bedClicked

    private void okButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_okButton1ActionPerformed
        // TODO add your handling code here:
        okButton1.setVisible(false);
    }//GEN-LAST:event_okButton1ActionPerformed

    private void okButton3ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_okButton3ActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_okButton3ActionPerformed

    private void okButton5ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_okButton5ActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_okButton5ActionPerformed

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
            java.util.logging.Logger.getLogger(WardJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(WardJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(WardJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(WardJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new WardJFrame(0).setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel SEWSIndicator1;
    private javax.swing.JLabel SEWSIndicator2;
    private javax.swing.JLabel SEWSIndicator3;
    private javax.swing.JLabel SEWSIndicator4;
    private javax.swing.JLabel SEWSIndicator5;
    private javax.swing.JLabel SEWSIndicator6;
    private javax.swing.JLabel actionLabel1;
    private javax.swing.JLabel actionLabel2;
    private javax.swing.JLabel actionLabel3;
    private javax.swing.JLabel actionLabel4;
    private javax.swing.JLabel actionLabel5;
    private javax.swing.JLabel actionLabel6;
    private javax.swing.JButton bed1;
    private javax.swing.JLabel bed1Name;
    private javax.swing.JComboBox bed1State;
    private javax.swing.JButton bed2;
    private javax.swing.JLabel bed2Name;
    private javax.swing.JComboBox bed2State;
    private javax.swing.JButton bed3;
    private javax.swing.JLabel bed3Name;
    private javax.swing.JComboBox bed3State;
    private javax.swing.JButton bed4;
    private javax.swing.JLabel bed4Name;
    private javax.swing.JComboBox bed4State;
    private javax.swing.JButton bed5;
    private javax.swing.JLabel bed5Name;
    private javax.swing.JComboBox bed5State;
    private javax.swing.JButton bed6;
    private javax.swing.JLabel bed6Name;
    private javax.swing.JComboBox bed6State;
    private javax.swing.JButton jButton_changeView;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel_systemTime;
    private javax.swing.JButton okButton1;
    private javax.swing.JButton okButton2;
    private javax.swing.JButton okButton3;
    private javax.swing.JButton okButton4;
    private javax.swing.JButton okButton5;
    private javax.swing.JButton okButton6;
    private javax.swing.JLabel wardNumField;
    // End of variables declaration//GEN-END:variables
}

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
import java.util.ArrayList;
import java.util.Calendar;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.Timer;
import utility.Patient;
import utility.Patients;
import utility.Utilities;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.IntervalMarker;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.StandardXYItemRenderer;
import org.jfree.data.xy.XYDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import utility.LiveData;

/**
 *
 * @author student
 */
public class HistoryJFrame extends javax.swing.JFrame {

    private Timer timer;
    private int timerCSeconds;
    
    private Patients patients;
    private int bedNum;
    private Patient thisPatient;
    
    private XYPlot plot;
    private ChartPanel cp;
    
    ArrayList<JCheckBox> checkBoxes;
    
    /**
     * Creates new form HistoryJFrame
     */
    public HistoryJFrame(int bedNum, int time, Patients patients) {
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
        
        //Get patient
        this.patients = patients;
        this.bedNum = bedNum;
        thisPatient = patients.getPatient(bedNum);
        
        //Set background colour
        this.getContentPane().setBackground(new Color(240,240,240));
        
        //fill titles
        wardNumField.setText("W001");
        bedNumField.setText(String.valueOf(bedNum));
        
        checkBoxes = new ArrayList<JCheckBox>() {
            {
               add(jCheckBox1);
               add(jCheckBox2);
               add(jCheckBox3);
               add(jCheckBox4);
               add(jCheckBox5);
               add(jCheckBox6);
            }  
        };
        
        genGraph(getGraphCode());
        
        //set timer
        timerCSeconds = time;
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
                        //genGraph(getGraphCode()); //only useful for dispalying data up until the current moment
                    }
                    
                    timerCSeconds++;
                }
            });
        }

        if (timer.isRunning() == false) {
            timer.start();
        }
    }
    
    public void genGraph(int code) {
        //ArrayList<LiveData> data = thisPatient.getLiveDatahistory(timerCSeconds); //Displays live data up untill the current moment
        ArrayList<LiveData> data = thisPatient.getAllLiveData();
        
        //create and populate graph
        XYSeries rr = new XYSeries("Respiratory rate (breaths/min)");
        XYSeries os = new XYSeries("Oxygen saturation (%)");
        XYSeries t = new XYSeries("Temperature (°C)");
        XYSeries sbp = new XYSeries("Systolic blood pressure (mmHg)");
        XYSeries hr = new XYSeries("Heart rate (beats/min)");
        
        for (int i = 0; i < data.size(); i++) {
            rr.add(i*5, data.get(i).rr);
            os.add(i*5, data.get(i).os);
            t.add(i*5, data.get(i).t);
            sbp.add(i*5, data.get(i).sbp);
            hr.add(i*5, data.get(i).hr);
        }
        
        XYDataset xyDataset1 = new XYSeriesCollection(rr);
        XYDataset xyDataset2 = new XYSeriesCollection(os);
        XYDataset xyDataset3 = new XYSeriesCollection(t);
        XYDataset xyDataset4 = new XYSeriesCollection(sbp);
        XYDataset xyDataset5 = new XYSeriesCollection(hr);
        
        JFreeChart chart = ChartFactory.createXYLineChart(
            thisPatient.getFullName(), "Time (s)", "",
            null, PlotOrientation.VERTICAL, true, true, false);
        
        this.plot = chart.getXYPlot();
        
        this.plot.setRenderer(0, new StandardXYItemRenderer());
        this.plot.setRenderer(1, new StandardXYItemRenderer());
        this.plot.setRenderer(2, new StandardXYItemRenderer());
        this.plot.setRenderer(3, new StandardXYItemRenderer());
        this.plot.setRenderer(4, new StandardXYItemRenderer());
        
        boolean markers = false;
        if ((code & 32) == 32) {
            markers = true;
        }
        //respiratory rate
        if ((code & 1) == 1) {
            this.plot.setDataset(0, xyDataset1);
            if (markers) {
                IntervalMarker zone = new IntervalMarker(9, 20);
                zone.setPaint(new Color(255,0,0,64));
                plot.addRangeMarker(zone);
            }
            this.plot.getRendererForDataset(plot.getDataset(0)).setSeriesPaint(0, Color.red);
        } 
        //oxygen saturation
        if ((code & 2) == 2) {
            this.plot.setDataset(1, xyDataset2);
            if (markers) {
                IntervalMarker zone = new IntervalMarker(93, 100);
                zone.setPaint(new Color(0,255,0,64));
                plot.addRangeMarker(zone);
            }
            this.plot.getRendererForDataset(plot.getDataset(1)).setSeriesPaint(0, Color.green);
        } 
        //temperature
        if ((code & 4) == 4) {
            this.plot.setDataset(2, xyDataset3);
            if (markers) {
                IntervalMarker zone = new IntervalMarker(36, 37.9);
                zone.setPaint(new Color(0,0,255,64));
                plot.addRangeMarker(zone);
            }
            this.plot.getRendererForDataset(plot.getDataset(2)).setSeriesPaint(0, Color.blue);
        } 
        //systolic blood pressure
        if ((code & 8) == 8) {
            this.plot.setDataset(3, xyDataset4);
            if (markers) {
                IntervalMarker zone = new IntervalMarker(100, 199);
                zone.setPaint(new Color(255,255,0,64));
                plot.addRangeMarker(zone);
            }
            this.plot.getRendererForDataset(plot.getDataset(3)).setSeriesPaint(0, Color.yellow);
        } 
        //heart rate
        if ((code & 16) == 16) {
            this.plot.setDataset(4, xyDataset5);
            if (markers) {
                IntervalMarker zone = new IntervalMarker(50, 99);
                zone.setPaint(new Color(255,0,255,64));
                plot.addRangeMarker(zone);
            }
            this.plot.getRendererForDataset(plot.getDataset(4)).setSeriesPaint(0, Color.magenta);
        } 
        
        
        graphPanel.removeAll();
        cp = new ChartPanel(chart);
        cp.setMouseWheelEnabled(true);
        cp.setPreferredSize(new Dimension(640, 480));
        graphPanel.setLayout(new java.awt.BorderLayout());
        graphPanel.add(cp, java.awt.BorderLayout.CENTER);
        graphPanel.validate();
        
        
    }
    
    private int getGraphCode () {
        int code = 0;
        for (int i = 0; i < checkBoxes.size(); i++) {
            if (checkBoxes.get(i).isSelected()) {
                code += Math.pow(2, i);
            } 
        }
        return code;
    }
        

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jLabel_systemTime = new javax.swing.JLabel();
        wardNumField = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        bedNumField = new javax.swing.JLabel();
        jButton_changeView = new javax.swing.JButton();
        jLabel2 = new javax.swing.JLabel();
        jLabel1 = new javax.swing.JLabel();
        graphPanel = new javax.swing.JPanel();
        jPanel1 = new javax.swing.JPanel();
        jCheckBox1 = new javax.swing.JCheckBox();
        jCheckBox2 = new javax.swing.JCheckBox();
        jCheckBox3 = new javax.swing.JCheckBox();
        jCheckBox4 = new javax.swing.JCheckBox();
        jCheckBox5 = new javax.swing.JCheckBox();
        jButton1 = new javax.swing.JButton();
        jCheckBox6 = new javax.swing.JCheckBox();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jLabel_systemTime.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel_systemTime.setText("TIME");

        wardNumField.setText("jLabel");

        jLabel3.setText("- Bed");

        bedNumField.setText("jLabel");

        jButton_changeView.setText("Back");
        jButton_changeView.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton_changeViewActionPerformed(evt);
            }
        });

        jLabel2.setText("Ward");

        jLabel1.setText("- History");

        graphPanel.setBackground(new java.awt.Color(255, 255, 255));

        javax.swing.GroupLayout graphPanelLayout = new javax.swing.GroupLayout(graphPanel);
        graphPanel.setLayout(graphPanelLayout);
        graphPanelLayout.setHorizontalGroup(
            graphPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        graphPanelLayout.setVerticalGroup(
            graphPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 480, Short.MAX_VALUE)
        );

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));

        jCheckBox1.setSelected(true);
        jCheckBox1.setText("Respiratory rate");

        jCheckBox2.setSelected(true);
        jCheckBox2.setText("Oxygen saturation");
        jCheckBox2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jCheckBox2ActionPerformed(evt);
            }
        });

        jCheckBox3.setSelected(true);
        jCheckBox3.setText("Temperature");

        jCheckBox4.setSelected(true);
        jCheckBox4.setText("Systolic blood pressure");

        jCheckBox5.setSelected(true);
        jCheckBox5.setText("Heart rate");

        jButton1.setText("Display");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        jCheckBox6.setText("Show ideal ranges");
        jCheckBox6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jCheckBox6ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(jCheckBox1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jCheckBox3)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jCheckBox5))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(jCheckBox2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jCheckBox4)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 25, Short.MAX_VALUE)
                        .addComponent(jCheckBox6)))
                .addGap(8, 8, 8)
                .addComponent(jButton1)
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jCheckBox1)
                            .addComponent(jCheckBox3)
                            .addComponent(jCheckBox5))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(jCheckBox2)
                            .addComponent(jCheckBox4)
                            .addComponent(jCheckBox6))
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addComponent(jButton1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jButton_changeView)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(wardNumField)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel3)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(bedNumField)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(jLabel_systemTime, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(graphPanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel3)
                    .addComponent(bedNumField, javax.swing.GroupLayout.PREFERRED_SIZE, 28, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel2)
                    .addComponent(jButton_changeView)
                    .addComponent(wardNumField)
                    .addComponent(jLabel_systemTime, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jLabel1))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(graphPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void jButton_changeViewActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton_changeViewActionPerformed
        // TODO add your handling code here:
        //dispose current window
        this.dispose();
        //open the Patient-View
        PatientJFrame patientFrame = new PatientJFrame(this.bedNum, timerCSeconds, this.patients);
        patientFrame.setVisible(true);
    }//GEN-LAST:event_jButton_changeViewActionPerformed

    private void jCheckBox2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jCheckBox2ActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_jCheckBox2ActionPerformed

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // TODO add your handling code here:
        //get checkbox value, update graph
        genGraph(getGraphCode());
    }//GEN-LAST:event_jButton1ActionPerformed

    private void jCheckBox6ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jCheckBox6ActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_jCheckBox6ActionPerformed

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
            java.util.logging.Logger.getLogger(HistoryJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(HistoryJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(HistoryJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(HistoryJFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new HistoryJFrame(0,0,null).setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel bedNumField;
    private javax.swing.JPanel graphPanel;
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton_changeView;
    private javax.swing.JCheckBox jCheckBox1;
    private javax.swing.JCheckBox jCheckBox2;
    private javax.swing.JCheckBox jCheckBox3;
    private javax.swing.JCheckBox jCheckBox4;
    private javax.swing.JCheckBox jCheckBox5;
    private javax.swing.JCheckBox jCheckBox6;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel_systemTime;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JLabel wardNumField;
    // End of variables declaration//GEN-END:variables
}

package com.sdp.eden;

public class BatteryStatus {
    private String Voltage;

    public BatteryStatus(){

    }

    public BatteryStatus(String voltage) {
        Voltage=voltage;
    }

    public String getVoltage() { return Voltage; }
    public void setVoltage(String voltage) { Voltage = voltage; }
}

package com.sdp.eden;

public class BatteryStatus {
    private Double Voltage;

    public BatteryStatus(){

    }

    public BatteryStatus(Double voltage) {
        Voltage=voltage;
    }

    public Double getVoltage() { return Voltage; }
    public void setVoltage(Double voltage) { Voltage = voltage; }
}

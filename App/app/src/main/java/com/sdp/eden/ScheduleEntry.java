package com.sdp.eden;

import java.util.ArrayList;

public class ScheduleEntry {
    private String PlantName;
    private String Day;
    private String Time;
    private int Quantity;

    public ScheduleEntry() {

    }

    public ScheduleEntry(String plantName, String day, String time, int quantity) {
        PlantName = plantName;
        Day = day;
        Time = time;
        Quantity = quantity;
    }

    public String getPlantName() {return PlantName; }
    public String getDay() {return Day; }
    public String getTime() {return Time; }
    public int getQuantity() {return Quantity; }
}

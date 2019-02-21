package com.sdp.eden;

public class ScheduleEntry {
    private String Day;
    private String PlantName;
    private Integer Quantity;
    private String Time;


    public ScheduleEntry() {

    }

    public ScheduleEntry(String day, String plantName, Integer quantity, String time) {
        Day = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
    }

    public String getPlantName() {return PlantName; }
    public String getDay() {return Day; }
    public String getTime() {return Time; }
    public Integer getQuantity() {return Quantity; }

    public void setPlantName(String plantName) {PlantName = plantName; }
    public void setDay(String day) {Day = day; }
    public void setTime(String time) {Time = time; }
    public void setQuantity(Integer quantity) {Quantity=quantity; }
}

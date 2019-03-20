package com.sdp.eden;

public class ScheduleEntry {
    private Integer DayOfWeek;
    private String PlantName;
    private Integer Quantity;
    private String Time;


    public ScheduleEntry() {

    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
    }

    public String getPlantName() {return PlantName; }
    public Integer getDay() {return DayOfWeek; }
    public String getTime() {return Time; }
    public Integer getQuantity() {return Quantity; }

    public void setPlantName(String plantName) {PlantName = plantName; }
    public void setDay(Integer day) {DayOfWeek = day; }
    public void setTime(String time) {Time = time; }
    public void setQuantity(Integer quantity) {Quantity=quantity; }
}

package com.sdp.eden;

public class ScheduleEntry {
    private Integer DayOfWeek;
    private String PlantName;
    private Integer Quantity;
    private String Time;
    private Float PlantXCoordinate;
    private Float PlantYCoordinate;


    public ScheduleEntry() {

    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time, Float plantXCoordinate, Float plantYCoordinate) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
        PlantXCoordinate=plantXCoordinate;
        PlantYCoordinate=plantYCoordinate;
    }

    public String getPlantName() {return PlantName; }
    public Integer getDay() {return DayOfWeek; }
    public String getTime() {return Time; }
    public Integer getQuantity() {return Quantity; }
    public Float getPlantXCoordinate() { return PlantXCoordinate; }
    public Float getPlantYCoordinate() { return PlantYCoordinate; }

    public void setPlantName(String plantName) {PlantName = plantName; }
    public void setDay(Integer day) {DayOfWeek = day; }
    public void setTime(String time) {Time = time; }
    public void setQuantity(Integer quantity) {Quantity=quantity; }
    public void setPlantXCoordinate(Float xCoordinate) {PlantXCoordinate=xCoordinate;}
    public void setPlantYCoordinate(Float yCoordinate) {PlantYCoordinate=yCoordinate;}
}

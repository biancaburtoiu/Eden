package com.sdp.eden;

public class ScheduleEntry {
    private Integer DayOfWeek;
    private String PlantName;
    private Integer Quantity;
    private String Time;
    private Float PlantXCoordinate;
    private Float PlantYCoordinate;

    private Integer PlantNoOfPetals;


    public ScheduleEntry() {

    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time, Integer plantNoOfPetals) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
        PlantNoOfPetals = plantNoOfPetals;
    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time, Integer plantNoOfPetals, Float plantXCoordinate, Float plantYCoordinate) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
        PlantNoOfPetals = plantNoOfPetals;
        PlantXCoordinate=plantXCoordinate;
        PlantYCoordinate=plantYCoordinate;
    }

    public String getPlantName() {return PlantName; }
    public Integer getDay() {return DayOfWeek; }
    public String getTime() {return Time; }
    public Integer getQuantity() {return Quantity; }
    public Integer getPlantNoOfPetals() {return PlantNoOfPetals; }
    public Float getPlantXCoordinate() { return PlantXCoordinate; }
    public Float getPlantYCoordinate() { return PlantYCoordinate; }

    public void setPlantName(String plantName) {PlantName = plantName; }
    public void setDay(Integer day) {DayOfWeek = day; }
    public void setTime(String time) {Time = time; }
    public void setQuantity(Integer quantity) {Quantity=quantity; }
    public void setPlantNoOfPetals(Integer plantNoOfPetals) {PlantNoOfPetals=plantNoOfPetals; }
    public void setPlantXCoordinate(Float xCoordinate) {PlantXCoordinate=xCoordinate;}
    public void setPlantYCoordinate(Float yCoordinate) {PlantYCoordinate=yCoordinate;}
}

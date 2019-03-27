package com.sdp.eden;

public class ScheduleEntry {
    private Integer DayOfWeek;
    private String PlantName;
    private Integer Quantity;
    private String Time;
    private Float PlantXCoordinate;
    private Float PlantYCoordinate;

    private Integer PlantNoOfPetals;
    private Boolean Valid;


    public ScheduleEntry() {

    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time, Integer plantNoOfPetals, Boolean valid) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
        PlantNoOfPetals = plantNoOfPetals;
        Valid = true;
    }

    public ScheduleEntry(Integer day, String plantName, Integer quantity, String time,
                         Integer plantNoOfPetals, Float plantXCoordinate, Float plantYCoordinate, Boolean valid) {
        DayOfWeek = day;
        PlantName = plantName;
        Quantity = quantity;
        Time = time;
        PlantNoOfPetals = plantNoOfPetals;
        PlantXCoordinate=plantXCoordinate;
        PlantYCoordinate=plantYCoordinate;
        Valid = true;
    }

    public String getPlantName() {return PlantName; }
    public Integer getDay() {return DayOfWeek; }
    public String getTime() {return Time; }
    public Integer getQuantity() {return Quantity; }
    public Integer getPlantNoOfPetals() {return PlantNoOfPetals; }
    public Float getPlantXCoordinate() { return PlantXCoordinate; }
    public Float getPlantYCoordinate() { return PlantYCoordinate; }
    public Boolean getValid() {return Valid; }

    public void setPlantName(String plantName) {PlantName = plantName; }
    public void setDay(Integer day) {DayOfWeek = day; }
    public void setTime(String time) {Time = time; }
    public void setQuantity(Integer quantity) {Quantity=quantity; }
    public void setPlantNoOfPetals(Integer plantNoOfPetals) {PlantNoOfPetals=plantNoOfPetals; }
    public void setPlantXCoordinate(Float xCoordinate) {PlantXCoordinate=xCoordinate;}
    public void setPlantYCoordinate(Float yCoordinate) {PlantYCoordinate=yCoordinate;}
    public void setValid(Boolean valid) {Valid = valid; }
}

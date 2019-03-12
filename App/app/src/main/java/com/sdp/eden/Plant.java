package com.sdp.eden;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;
    private List<Integer> Photo;
    private Float XCoordinate;
    private Float YCoordinate;


    public Plant(){

    }

    public Plant(String name, String species, List<Integer> photo){
        Name=name;
        Species=species;
        Photo=photo;
    }

    public Plant(String name, String species, List<Integer> photo, Float xcoordinate, Float ycoordinate){
        Name=name;
        Species=species;
        Photo=photo;
        XCoordinate=xcoordinate;
        YCoordinate=ycoordinate;
    }

    public String getName() {
        return Name;
    }
    public void setName(String name) { Name = name; }

    public String getSpecies() {
        return Species;
    }
    public void setSpecies(String species) { Species = species; }

    public List<Integer> getPhoto() { return Photo; }
    public void setPhoto(List<Integer> photo) { Photo = photo; }

    public Float getXCoordinate() { return XCoordinate; }
    public void setXCoordinate(float xCoordinate) { XCoordinate = xCoordinate; }

    public Float getYCoordinate() { return YCoordinate; }
    public void setYCoordinate(float yCoordinate) { YCoordinate = yCoordinate; }
}

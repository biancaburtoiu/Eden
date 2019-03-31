package com.sdp.eden;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;
    private List<Integer> Photo;

    private Float XCoordinate;
    private Float YCoordinate;

    private Integer NoOfPetals;



    public Plant(){

    }

    public Plant(String name, String species, List<Integer> photo, Integer noOfPetals){
        Name=name;
        Species=species;
        Photo=photo;
        NoOfPetals=noOfPetals;
    }

    public Plant(String name, String species, List<Integer> photo, Integer noOfPetals, Float xcoordinate, Float ycoordinate){
        Name=name;
        Species=species;
        Photo=photo;
        NoOfPetals=noOfPetals;
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

    public Integer getNoOfPetals() { return NoOfPetals; }
    public void setNoOfPetals(Integer noOfPetals) { NoOfPetals = noOfPetals; }

    //@Exclude
    public Float getXCoordinate() { return XCoordinate; }

    //@Exclude
    public void setXCoordinate(float xCoordinate) { XCoordinate = xCoordinate; }

    //@Exclude
    public Float getYCoordinate() { return YCoordinate; }

    //@Exclude
    public void setYCoordinate(float yCoordinate) { YCoordinate = yCoordinate; }

}

package com.sdp.eden;


import com.google.firebase.firestore.Exclude;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;
    private List<Integer> Photo;

    private Float XCoordinate;
    private Float YCoordinate;

    private String LastWatered;

    private Integer NoOfPetals;


    public Plant(){

    }

    public Plant(String lastWatered, String name, String species, List<Integer> photo, Integer noOfPetals){
        LastWatered = lastWatered;
        Name=name;
        Species=species;
        Photo=photo;
        NoOfPetals=noOfPetals;

    }

    public Plant(String lastWatered, String name, String species, List<Integer> photo, Integer noOfPetals, Float xcoordinate, Float ycoordinate){
        LastWatered = lastWatered;
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

    public String getLastWatered() {
        return LastWatered;
    }

    public void setLastWatered(String lastWatered) {
        LastWatered = lastWatered;
    }

    //@Exclude
    public Float getXCoordinate() { return XCoordinate; }

    //@Exclude
    public void setXCoordinate(float xCoordinate) { XCoordinate = xCoordinate; }

    //@Exclude
    public Float getYCoordinate() { return YCoordinate; }

    //@Exclude
    public void setYCoordinate(float yCoordinate) { YCoordinate = yCoordinate; }
}

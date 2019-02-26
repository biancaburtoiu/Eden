package com.sdp.eden;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;
    private List<Integer> Photo;


    public Plant(){

    }

    public Plant(String name, String species, List<Integer> photo){
        Name=name;
        Species=species;
        Photo=photo;
    }

    public String getName() {
        return Name;
    }

    public String getSpecies() {
        return Species;
    }

    public List<Integer> getPhoto() { return Photo; }

    public void setName(String name) { Name = name; }

    public void setSpecies(String species) { Species = species; }

    public void setPhoto(List<Integer> photo) { Photo = photo; }
}

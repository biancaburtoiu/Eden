package com.sdp.eden;

public class Plant {
    private String Name;
    private String Species;
    private int Photo;


    public Plant(){

    }

    public Plant(String name, String species, int photo){
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

    public int getPhoto() {
        return Photo;
    }

    public void setName(String name) { Name = name; }

    public void setSpecies(String species) { Species = species; }

    public void setPhoto(int photo) {
        Photo = photo;
    }
}

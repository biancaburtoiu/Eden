package com.sdp.eden;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;


    public Plant(){

    }

    public Plant(String name, String species){
        Name=name;
        Species=species;
    }

    public String getName() {
        return Name;
    }

    public String getSpecies() {
        return Species;
    }


    public void setName(String name) { Name = name; }

    public void setSpecies(String species) { Species = species; }

}

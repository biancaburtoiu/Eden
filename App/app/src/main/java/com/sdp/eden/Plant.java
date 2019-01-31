package com.sdp.eden;

public class Plant {
    private String Name;
    private int Photo;

    public Plant(){

    }

    public Plant(String name, int photo){
        Name=name;
        Photo=photo;
    }

    public String getName() {
        return Name;
    }

    public int getPhoto() {
        return Photo;
    }

    public void setName(String name) {
        Name = name;
    }

    public void setPhoto(int photo) {
        Photo = photo;
    }
}

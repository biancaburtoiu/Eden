package com.sdp.eden;


import android.graphics.Bitmap;
import java.util.List;

public class Plant {
    private String Name;
    private String Species;
    //private Bitmap PhotoBitmap;
    private List<Integer> Photo;


    public Plant(){

    }

    public Plant(String name, String species, List<Integer> photo){
        Name=name;
        Species=species;
        //PhotoBitmap=photoBitmap;
        Photo=photo;
    }

    public String getName() {
        return Name;
    }

    public String getSpecies() {
        return Species;
    }

//    public Bitmap getPhotoBitmap() {
//        return PhotoBitmap;
//    }

    public List<Integer> getPhoto() { return Photo; }

    public void setName(String name) { Name = name; }

    public void setSpecies(String species) { Species = species; }

//    public void setPhotoBitmap(Bitmap photoBitmap) {
//        PhotoBitmap = photoBitmap;
//    }

    public void setPhoto(List<Integer> photo) { Photo = photo; }
}

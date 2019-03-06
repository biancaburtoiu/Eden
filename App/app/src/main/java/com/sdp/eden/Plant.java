package com.sdp.eden;

import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;

import com.google.firebase.firestore.Exclude;

import java.util.List;

public class Plant {
    private String Name;
    private String Species;

    private Drawable Drawable;


    public Plant(){

    }

    public Plant(String name, String species, Drawable drawable){
        Name=name;
        Species=species;
        Drawable=drawable;
    }

    public String getName() {
        return Name;
    }

    public String getSpecies() {
        return Species;
    }

    @Exclude
    public Drawable getDrawable() { return Drawable; }

    public void setName(String name) { Name = name; }

    public void setSpecies(String species) { Species = species; }

    public void setDrawable(Drawable drawable) { Drawable = drawable; }
}

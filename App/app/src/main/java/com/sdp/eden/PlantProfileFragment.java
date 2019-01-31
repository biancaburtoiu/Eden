package com.sdp.eden;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

import java.util.function.ToDoubleBiFunction;


public class PlantProfileFragment extends DialogFragment {
    private static final String TAG = "PlantProfileFragment";

    public PlantProfileFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_plant_profile, container, false);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        Log.d(TAG, "Entered PlantProfileFragment");
        super.onViewCreated(view, savedInstanceState);

        // TODO: Query database and obtain information of that plant

        // This would be the Plant object returned by the database query
        Plant plant = new Plant("p1", "cacti", 15);
        Log.d(TAG, String.format("Plant name: %s, species: %s, photo: %s",plant.getName(),plant.getSpecies(),plant.getPhoto()));

        TextView name = view.findViewById(R.id.plantName);
        name.setText(plant.getName());

        TextView species = view.findViewById(R.id.plantSpecies);
        species.setText(plant.getSpecies());

        // TODO: Functionality to display photo?

        Button editNameButton = view.findViewById(R.id.editNameButton);
        editNameButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Create AlertDialog with EditText to write new name
                // TODO: Modify(?) name field of that plant
            }
        });

        Button editSpeciesButton = view.findViewById(R.id.editSpeciesButton);
        editSpeciesButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Create AlertDialog with EditText to write new species
                // TODO: Modify(?) species field of that plant
                // TODO: That would also modify the schedule! Handle that as well!
            }
        });

        Button viewScheduleButton = view.findViewById(R.id.viewScheduleButton);
        viewScheduleButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Open a window with the schedule information
            }
        });

        Button deletePlantButton = view.findViewById(R.id.deletePlantButton);
        deletePlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Create AlertDialog asking if user is completely sure
                // TODO: Delete plant document from database
            }
        });
    }
}

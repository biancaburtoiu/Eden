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

import java.util.function.ToDoubleBiFunction;


public class AddPlantFragment extends DialogFragment {
    private static final String TAG = "AddPlantFragment";

    public AddPlantFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_add_plant, container, false);
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        Log.d(TAG, "Entered AddPlantFragment");
        super.onViewCreated(view, savedInstanceState);

        final EditText plantName = (EditText) view.findViewById(R.id.plantName);

        final Spinner plantSpecies = view.findViewById(R.id.plantSpecies);
        String[] species = new String[]{"cacti","daisy","lily"};
        ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(getContext(), R.layout.species_option, species);
        plantSpecies.setAdapter(speciesAdapter);


        Button addPlantButton = (Button) view.findViewById(R.id.addPlantButton);
        addPlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(TAG, "New plant to add to database:");
                Log.d(TAG, "Plant name: " + plantName.getText());
                Log.d(TAG, "Plant species: " + plantSpecies.getSelectedItem());

                // Adds plant to database with info: name and species
            }
        });
    }
}

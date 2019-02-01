package com.sdp.eden;

import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class PlantListFragment extends Fragment {
    private static final String TAG = "PlantListFragment";
    View v;

    private RecyclerView myrecyclerview;
    private List<Plant> plants;

    // To keep track of the items checked (selected) in the RecyclerView
    private List<Integer> checkedItems;

    @Override
    public void onResume() {
        super.onResume();
        checkedItems = new ArrayList<>();
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.fragment_plants,container,false);

        //setting up Layout Manager and adapter for recyclerview
        myrecyclerview = v.findViewById(R.id.plant_recyclerview);
        RecyclerViewAdapter recyclerAdapter = new RecyclerViewAdapter(getContext(),plants);
        myrecyclerview.setLayoutManager(new LinearLayoutManager(getActivity()));
        myrecyclerview.setAdapter(recyclerAdapter);

        // TODO: Set recyclerview to grab plants list by querying the database
        return v;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        plants = new ArrayList<>();
        plants.add(new Plant("plant1","species1", R.drawable.plant1));
        plants.add(new Plant("plant2","species2", R.drawable.plant2));
        plants.add(new Plant("plant3","species3", R.drawable.plant3));

    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // TODO: Get number of selected items in RecyclerView
        // If only ONE item selected, enable the Edit, Delete and View Schedule buttons. Disable Add
        // If no item selected, disable the Edit, Delete and View Schedule buttons. Enable Add


        Button viewScheduleButton = view.findViewById(R.id.viewPlantScheduleButton);
        viewScheduleButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Open a window with the schedule information
            }
        });


        Button editPlantButton = view.findViewById(R.id.editPlantButton);
        editPlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Create AlertDialog with EditText to write new info
                // TODO: Modify(?) fields of that plant
            }
        });

        Button deletePlantButton = view.findViewById(R.id.deletePlantButton);
        deletePlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(TAG, "User input: click on Delete");

                AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                builder.setTitle("Delete plant");
                builder.setMessage("Are you sure you want to delete this plant from the database? All information will be lost.");

                builder.setPositiveButton("Delete", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // TODO: Delete plant document from database
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });



        Button addPlantButton = v.findViewById(R.id.addPlantButton);
        addPlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(TAG, "User input: click on Add");

                AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                builder.setTitle("Add a new plant!");

                View viewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.fragment_add_plant,
                        (ViewGroup) getView(), false);

                final EditText plantName = viewInflated.findViewById(R.id.plantName);
                final Spinner plantSpecies = viewInflated.findViewById(R.id.plantSpecies);
                builder.setView(viewInflated);

                String[] species = new String[]{"cacti","daisy","lily"};
                ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(getContext(), R.layout.species_option, species);
                plantSpecies.setAdapter(speciesAdapter);

                builder.setPositiveButton("Add", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Log.d(TAG, "New plant to add to database:");
                        Log.d(TAG, "Plant name: " + plantName.getText());
                        Log.d(TAG, "Plant species: " + plantSpecies.getSelectedItem());

                        // Checks for empty plant name
                        if (plantName.getText().toString().trim().length() == 0) {
                            Log.d(TAG, "Plant name format incorrect. Rejected further operations.");
                            Toast.makeText(getContext(), "Plant name cannot be empty.", Toast.LENGTH_LONG).show();
                        }
                        else {
                            Log.d(TAG, "Plant name format correct.");
                            // TODO: Add plant to database with info: name and species
                        }
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });
    }
}

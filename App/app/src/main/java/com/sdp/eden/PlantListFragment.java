package com.sdp.eden;

import android.content.DialogInterface;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.Fragment;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.util.SparseBooleanArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;

import java.util.ArrayList;
import java.util.List;

public class PlantListFragment extends Fragment {
    private static final String TAG = "PlantListFragment";
    View v;

    private RecyclerView recyclerView;
    private RecyclerView_Adapter adapter;
    private ArrayList<Plant> plants;
    private android.support.v7.view.ActionMode mActionMode;
    private Eden_main mainAct;


    @Override
    public void onResume() {
        super.onResume();
        getLatestPlantList();    // Query the database to get latest list
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.fragment_plants,container,false);

        // Moved the recyclerview initialization bit here
        recyclerView = v.findViewById(R.id.plant_recyclerview);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        getLatestPlantList();    // Query the database to get latest list

        implementRecyclerViewClickListeners();
        mainAct = (Eden_main) getActivity();

        return v;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d("realID", "value" + getId());
        ((Eden_main) getActivity()).fr= this;

        // Don't need these anymore:
//        plants = new ArrayList<>();
//        plants.add(new Plant("plant1","species1", R.drawable.plant1));
//        plants.add(new Plant("plant2","species2", R.drawable.plant2));
//        plants.add(new Plant("plant3","species3", R.drawable.plant3));
    }

    private void populateRecyclerView(ArrayList<Plant> plants){ // Bianca - changed this to accept a list parameter
//        recyclerView = v.findViewById(R.id.plant_recyclerview);
//        recyclerView.setHasFixedSize(true);
//        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
        adapter = new RecyclerView_Adapter(getActivity(),plants);
        recyclerView.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }

    private void implementRecyclerViewClickListeners() {
        recyclerView.addOnItemTouchListener(new RecyclerTouchListener(getActivity(), recyclerView, new RecyclerClick_Listener() {
            @Override
            public void onClick(View view, int position) {
                //If ActionMode not null select item
                if (mActionMode != null)
                    onListItemSelect(position);
            }

            @Override
            public void onLongClick(View view, int position) {
                //Select item on long click
                onListItemSelect(position);
            }
        }));
    }

    //List item select method
    private void onListItemSelect(int position) {
        adapter.toggleSelection(position);//Toggle the selection

        boolean hasCheckedItems = adapter.getSelectedCount() > 0;//Check if any items are already selected or not


        if (hasCheckedItems && mActionMode == null)
            // there are some selected items, start the actionMode
                mActionMode = ((AppCompatActivity) getActivity()).startSupportActionMode(new Toolbar_ActionMode_Callback(getActivity(),adapter,plants,this));
        else if (!hasCheckedItems && mActionMode != null)
            // there no selected items, finish the actionMode
            mActionMode.finish();

        if (mActionMode != null)
            //set action mode title on item selection
            mActionMode.setTitle(String.valueOf(adapter
                    .getSelectedCount()) + " selected");


    }

    //Delete selected rows
    public void deleteRows() {
        SparseBooleanArray selected = adapter
                .getSelectedIds();//Get selected ids

        //Loop all selected ids
        for (int i = (selected.size() - 1); i >= 0; i--) {
            if (selected.valueAt(i)) {
                //If current id is selected remove the item via key
                plants.remove(selected.keyAt(i));
                adapter.notifyDataSetChanged();//notify adapter

            }
        }
        Toast.makeText(getActivity(), selected.size() + " item deleted.", Toast.LENGTH_SHORT).show();//Show Toast
        mActionMode.finish();//Finish action mode after use

    }

    //Set action mode null after use
    public void setNullToActionMode() {
        if (mActionMode != null)
            mActionMode = null;
    }



    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        FloatingActionButton addPlantButton = v.findViewById(R.id.addPlantButton);
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

                // TODO: Kieran W - Maybe add more species here for the user interview?
                String[] species = new String[]{"cacti","daisy","lily","orchid"};
                ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(getContext(), R.layout.species_option, species);
                plantSpecies.setAdapter(speciesAdapter);

                builder.setPositiveButton("Add", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Log.d(TAG, "New plant to add to database:");
                        Log.d(TAG, "Plant name: " + plantName.getText().toString());
                        Log.d(TAG, "Plant species: " + plantSpecies.getSelectedItem().toString());

                        // Checks for empty plant name
                        if (plantName.getText().toString().trim().length() == 0) {
                            Log.d(TAG, "Plant name format incorrect. Rejected further operations.");
                            Toast.makeText(getContext(), "Plant name cannot be empty.", Toast.LENGTH_LONG).show();
                        }
                        else {
                            Log.d(TAG, "Plant name format correct.");

                            // For now any new plant would be added with this default drawable.
                            // To implement actual photo functionality later.
                            Plant plant = new Plant(plantName.getText().toString(),
                                                    plantSpecies.getSelectedItem().toString(),
                                                    R.drawable.plant1);
                            DbOps.instance.addPlant(plant, new DbOps.onAddPlantFinishedListener() {
                                @Override
                                public void onUpdateFinished(boolean success) {
                                    getLatestPlantList();
                                    Toast.makeText(getContext(),"You just added a new plant!", Toast.LENGTH_LONG).show();
                                }
                            });
                        }
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });
/*       addPlantButton.setOnClickListener(p->{


          ((Eden_main) getActivity()).changeFrag(new RobotFragment());

       });*/
    }

    // Queries the database to get the most recent list of plants
    public void getLatestPlantList() {
        DbOps.instance.getPlantList(FirebaseAuth.getInstance().getCurrentUser().getEmail(),
                new DbOps.OnGetPlantListFinishedListener() {
                    @Override
                    public void onGetPlantListFinished(List<Plant> plantsFromDB) {
                        if (plantsFromDB==null) return;

                        Log.d(TAG, "Obtained list of plants from DB of size: "+plantsFromDB.size());

                        // Refreshes the recyclerview:
                        populateRecyclerView(new ArrayList<Plant>(plantsFromDB));
                    }
                });
    }
}

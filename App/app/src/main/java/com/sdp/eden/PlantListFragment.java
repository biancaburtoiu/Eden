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
import android.view.ActionMode;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

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
        populateRecyclerView();
        implementRecyclerViewClickListeners();
        mainAct = (Eden_main) getActivity();

        // TODO: Set recyclerview to grab plants list by querying the database
        return v;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d("realID", "value" + getId());
        ((Eden_main) getActivity()).fr= this;

        plants = new ArrayList<>();
        plants.add(new Plant("plant1","species1", R.drawable.plant1));
        plants.add(new Plant("plant2","species2", R.drawable.plant2));
        plants.add(new Plant("plant3","species3", R.drawable.plant3));


    }

    private void populateRecyclerView(){
        recyclerView = v.findViewById(R.id.plant_recyclerview);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
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

        // TODO: Get number of selected items in RecyclerView
        // If only ONE item selected, enable the Edit, Delete and View Schedule buttons. Disable Add
        // If no item selected, disable the Edit, Delete and View Schedule buttons. Enable Add





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
/*       addPlantButton.setOnClickListener(p->{


          ((Eden_main) getActivity()).changeFrag(new RobotFragment());

       });*/
    }
}

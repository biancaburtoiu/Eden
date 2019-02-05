package com.sdp.eden;

import android.content.Context;
import android.content.DialogInterface;
import android.net.Uri;
import android.os.Bundle;
import android.provider.SyncStateContract;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.CardView;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.PopupMenu;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;

import java.util.ArrayList;
import java.util.List;

public class Plant_Cards_Fragment extends Fragment {

    private static final String TAG = "PlantListFragment";
    private Eden_main mainAct;
    private ArrayList<Plant> plants;
    private RecyclerView recyclerView;
    private RecyclerViewAdapter adapter;

   public View onCreateView (@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
       View view = inflater.inflate(R.layout.fragment_plants, container, false);
       getLatestPlantList();    // Query the database to get latest list
       //implementRecyclerViewClickListeners();
       mainAct = (Eden_main) getActivity();
       recyclerView = view.findViewById(R.id.Plants_Recycler_view);
       recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
       return view;
   }


    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        FloatingActionButton addPlantButton = view.findViewById(R.id.addPlantButton);
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
                            Snackbar.make(getView().findViewById(R.id.viewSnack), "Name your plant!", Snackbar.LENGTH_SHORT).show();
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

    @Override
    public void onResume() {
        super.onResume();
        getLatestPlantList();    // Query the database to get latest list
    }

    public static Fragment newInstance() {
       return new Plant_Cards_Fragment();
    }

    private void populateRecyclerView(ArrayList<Plant> plants){ // Bianca - changed this to accept a list parameter
       adapter = new RecyclerViewAdapter(plants);
       recyclerView.setAdapter(adapter);
       adapter.notifyDataSetChanged();
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
                        plants = new ArrayList<Plant>(plantsFromDB);
                        populateRecyclerView(new ArrayList<Plant>(plantsFromDB));
                    }
                });
    }


    private class RecyclerViewHolder extends RecyclerView.ViewHolder{

       private CardView mCardView;
       private TextView plantName;
       private TextView plantDetail;
       private ImageView plantImage;


        public RecyclerViewHolder(@NonNull View itemView) {
            super(itemView);
            mCardView = itemView.findViewById(R.id.card_view);
        }



        public RecyclerViewHolder(LayoutInflater inflater, ViewGroup container){
            super(inflater.inflate(R.layout.card_layout, container, false));
            mCardView = itemView.findViewById(R.id.card_view);
            plantName = itemView.findViewById(R.id.card_plant_name);
            plantDetail = itemView.findViewById(R.id.card_plant_detail);
            plantImage = itemView.findViewById(R.id.card_plant_image);

        }
    }

    private class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewHolder>{
       public ArrayList<Plant> plantsList;

       public RecyclerViewAdapter(ArrayList<Plant> list){
           this.plantsList = list;
       }

        @NonNull
        @Override
        public RecyclerViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
            LayoutInflater inflater = LayoutInflater.from(getActivity());
            return new RecyclerViewHolder(inflater, viewGroup);
        }

        @Override
        public void onBindViewHolder(@NonNull RecyclerViewHolder recyclerViewHolder, int i) {
            ImageButton mImageButton = recyclerViewHolder.mCardView.findViewById(R.id.popup_menu);

            recyclerViewHolder.plantName.setText(plantsList.get(i).getName());
            recyclerViewHolder.plantDetail.setText(plantsList.get(i).getSpecies());
            recyclerViewHolder.plantImage.setImageResource(plantsList.get(i).getPhoto());

            recyclerViewHolder.mCardView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Snackbar.make(getView().findViewById(R.id.viewSnack), "Name: " + plantsList.get(i).getName(), Snackbar.LENGTH_SHORT).show();
                }
            });

            mImageButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    showPopupMenu(mImageButton, i);
                }
            });

        }


        private void showPopupMenu(View view,int position) {
            // inflate menu
            PopupMenu popup = new PopupMenu(view.getContext(),view );
            MenuInflater inflater = popup.getMenuInflater();
            inflater.inflate(R.menu.card_menu, popup.getMenu());
            popup.setOnMenuItemClickListener(new MyMenuItemClickListener(position));
            popup.show();
        }


        @Override
        public int getItemCount() {
            return plantsList.size();
        }
    }


    class MyMenuItemClickListener implements PopupMenu.OnMenuItemClickListener {

        private int position;
        public MyMenuItemClickListener(int positon) {
            this.position=positon;
        }

        @Override
        public boolean onMenuItemClick(MenuItem menuItem) {
            switch (menuItem.getItemId()) {

                case R.id.card_delete:
                    Snackbar.make(getView().findViewById(R.id.viewSnack), "selected delete on plant: " + plants.get(position).getName(), Snackbar.LENGTH_SHORT).show();
                    return true;
                case R.id.card_edit:
                    Snackbar.make(getView().findViewById(R.id.viewSnack), "selected edit on plant: " + plants.get(position).getName(), Snackbar.LENGTH_SHORT).show();
                    return true;
            }
            return false;
        }
    }

}

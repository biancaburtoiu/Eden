package com.sdp.eden;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
//import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.CardView;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Base64;
import android.util.Log;
import android.view.ContextThemeWrapper;
import android.view.LayoutInflater;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.PopupMenu;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.common.primitives.Bytes;
import com.google.common.primitives.Ints;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import com.github.clans.fab.FloatingActionButton;
import com.github.clans.fab.FloatingActionMenu;

import static android.app.Activity.RESULT_OK;

public class Plant_Cards_Fragment extends Fragment {

    private static final String TAG = "Plant_Cards_Fragment";
    private ArrayList<Plant> plants; // list of plants pulled from firebase
    private RecyclerView recyclerView;
    private ImageView plantPic;
    private StorageReference mStorage = FirebaseStorage.getInstance().getReference();
    private String enteredPlantName; // this will hopefully be temp
    private Uri takenImage; // once again hopeful;ly this will be temp!

    // FAM Chunk
    FloatingActionMenu materialDesignFAM;
    FloatingActionButton fab_addPlant, fab_addSchedule;
    // FAM Chunk End


    public View onCreateView (@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
        View view = inflater.inflate(R.layout.fragment_plants, container, false);
        getLatestPlantList();    // Query the database to get latest list
        recyclerView = view.findViewById(R.id.Plants_Recycler_view);
        
        // FAM Chunk: https://www.viralandroid.com/2016/02/android-floating-action-menu-example.html
        materialDesignFAM = (FloatingActionMenu) view.findViewById(R.id.material_design_android_floating_action_menu);
        fab_addPlant = (FloatingActionButton) view.findViewById(R.id.material_design_floating_action_menu_item1);
        fab_addSchedule = (FloatingActionButton) view.findViewById(R.id.material_design_floating_action_menu_item2);

        fab_addPlant.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Log.d(TAG, "User input: click on Add");

                AlertDialog.Builder builder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                //builder.setTitle("Add a new plant!");

                View viewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.fragment_add_plant, (ViewGroup) getView(), false);

                final EditText plantName = viewInflated.findViewById(R.id.plantName);
                final Spinner plantSpecies = viewInflated.findViewById(R.id.plantSpecies);
                plantPic = viewInflated.findViewById(R.id.plantPic);
                builder.setView(viewInflated);

                // TODO: perhaps changing species to a short description of the plant (E.G. location or characteristic)
                String[] species = new String[]{"Select Species","cacti","daisy","lily","orchid"};
                ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(Objects.requireNonNull(getContext()), R.layout.species_option, species);
                plantSpecies.setAdapter(speciesAdapter); // creates the drop down selection

                plantPic.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        if (plantName.getText().toString().trim().length() == 0){
                            plantName.setError("Enter a plant name");
                        }else{
                            enteredPlantName = plantName.getText().toString().trim();
                            Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE); // kieran - opens camera
                            // TODO: Kieran - upload to firebase storage and pull for each card (having trouble with this)
                            if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
                                startActivityForResult(takePictureIntent, 111); // set the request code for the photo to 111
                            }
                        }
                    }
                });

                builder.setPositiveButton("Add", (dialog, which) -> {
                    Log.d(TAG, "New plant to add to database:");
                    Log.d(TAG, "Plant name: " + plantName.getText().toString());
                    Log.d(TAG, "Plant species: " + plantSpecies.getSelectedItem().toString()); // extracts the plant data from user input

                    if(plantSpecies.getSelectedItem().toString().equals("Select Species")){
                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "Select a Species", Snackbar.LENGTH_SHORT).show();
                    }
                    // Checks for empty plant name
                    if (plantName.getText().toString().trim().length() == 0) {
                        Log.d(TAG, "Plant name format incorrect. Rejected further operations.");
                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "Name your plant!", Snackbar.LENGTH_SHORT).show();
                    }
                    else {
                        Log.d(TAG, "Plant name format correct.");

                        ProgressDialog mProgress;
                        mProgress = new ProgressDialog(getContext());
                        mProgress.setMessage("Creating the plant ...");
                        mProgress.show();

                        // List<Integer> defaultPlant = bitmapToIntegerList(BitmapFactory.decodeResource(getResources(),R.drawable.default_plant));

                        // TODO: Need to adapt this if we save pictures to bucket!
                        Plant plant;
                        if (imageBitmap == null) {
                            plant = new Plant(plantName.getText().toString(),
                                    plantSpecies.getSelectedItem().toString(),
                                    new ArrayList<>());
                        }
                        else {
                            plant = new Plant(plantName.getText().toString(),
                                    plantSpecies.getSelectedItem().toString(),
                                    bitmapToIntegerList(imageBitmap));
                        }

                        DbOps.instance.addPlant(plant, new DbOps.onAddPlantFinishedListener() {
                            @Override
                            public void onUpdateFinished(boolean success) {
                                //uploadImageToFirebase(); // completes the new plant
                                getLatestPlantList();

                                mProgress.dismiss();
                            }
                        });
                        // uploadImageToFirebase(); // completes the new plant --- moved from here
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.show();

            }
        });

        fab_addSchedule.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                //builder.setTitle("Add schedule for plant");

                View viewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.fragment_add_plant_schedule,
                        (ViewGroup) getView(), false);

                final TimePicker timePicker = viewInflated.findViewById(R.id.timePicker);
                timePicker.setIs24HourView(true);

                final Spinner plantSelect = viewInflated.findViewById(R.id.plantSelect);
                List<String> plantArray = (plants.stream().map(plant -> plant.getName()).collect(Collectors.toList()));
                plantArray.add(0, "Select Plant");

                ArrayAdapter<String> plantsAdapter = new ArrayAdapter<>(Objects.requireNonNull(getContext()), R.layout.spinner_style, plantArray.toArray(new String[]{}));
                plantSelect.setAdapter(plantsAdapter);

                final Spinner dayOfWeekPicker = viewInflated.findViewById(R.id.dayOfWeek);
                String[] days = new String[]{"Select Day","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
                ArrayAdapter<String> daysAdapter = new ArrayAdapter<>(Objects.requireNonNull(getContext()), R.layout.spinner_style, days);
                dayOfWeekPicker.setAdapter(daysAdapter); // creates the drop down selection

                EditText quantityInput = viewInflated.findViewById(R.id.quantityInput);

                builder.setView(viewInflated);

                builder.setPositiveButton("Set", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                        // TODO: modify this to grab plant somehow!!!
                        String currentPlant = plantSelect.getSelectedItem().toString();

                        // getMinute is in 0-59 interval. The code below adds a 0 ahead of the minutes 0-9
                        // Result: 20:01 instead of 20:1
                        // However, hours between 12am and 12pm will have a single digit: e.g. 2:45

                        String time;
                        if (timePicker.getMinute()<10)
                            time = timePicker.getHour()+":0"+timePicker.getMinute();
                        else
                            time = timePicker.getHour()+":"+timePicker.getMinute();

                        int quantity = Integer.parseInt(quantityInput.getText().toString());

                        String selectedDay = dayOfWeekPicker.getSelectedItem().toString();

                        ScheduleEntry scheduleEntry = new ScheduleEntry(selectedDay,currentPlant, quantity, time);
                        DbOps.instance.addScheduleEntry(scheduleEntry, new DbOps.onAddScheduleEntryFinishedListener() {
                            @Override
                            public void onAddScheduleEntryFinished(boolean success) {
                                Toast.makeText(getContext(), "Added watering schedule entry for "+ currentPlant +
                                        " on "+scheduleEntry.getDay()+ "s at "+ scheduleEntry.getTime()+ "!", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });
        // FAM Chunk End

        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity())); // sets layout for recycler view, linear list in this case
        return view;
    }


    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
    }


    // https://stackoverflow.com/a/40886397
    public String bitmapToString(Bitmap bmp) {

        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.PNG, 100, bao);
        bmp.recycle();
        byte[] byteArray = bao.toByteArray();
        String result = Base64.encodeToString(byteArray, Base64.DEFAULT);

        Log.d(TAG, "Result of bitmapToString is: "+result);
        return result;
    }

    // https://stackoverflow.com/a/40886397
    public List<Integer> bitmapToIntegerList(Bitmap bmp) {

        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.PNG, 100, bao); // bmp is bitmap from user image file
        bmp.recycle();
        byte[] byteArray = bao.toByteArray();

        List<Byte> byteList = Bytes.asList(byteArray);
        List<Integer> integerList = Ints.asList(Ints.toArray(byteList));

        Log.d(TAG, "Result of bitmapToIntegerList is: "+integerList);
        return integerList;
    }


    // http://ramsandroid4all.blogspot.com/2014/09/converting-byte-array-to-bitmap-in.html
    public Bitmap byteArrayToBitmap(byte[] byteArray)
    {
        ByteArrayInputStream arrayInputStream = new ByteArrayInputStream(byteArray);
        Bitmap bitmap = BitmapFactory.decodeStream(arrayInputStream);

        Log.d(TAG, "Result of byteArrayToBitmap is: "+bitmap);
        return bitmap;
    }


    Bitmap imageBitmap;
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data){ // retrieves the camera image
        super.onActivityResult(requestCode,resultCode,data);

        if (requestCode == 111 && resultCode == RESULT_OK){
            Bundle extras = data.getExtras();

            //Changed here!
            //Bitmap imageBitmap = (Bitmap) extras.get("data");
            imageBitmap = (Bitmap) extras.get("data");

            plantPic.setImageBitmap(imageBitmap);
            takenImage = getImageUri(getContext(), imageBitmap);
            System.out.println("taken image is " + takenImage);
            System.out.println("Plant name is " + enteredPlantName);
        }
    }

    // converts the BitMap to Uri
    public Uri getImageUri(Context inContext, Bitmap inImage) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(inContext.getContentResolver(), inImage, "Title", null);
        return Uri.parse(path);
    }

    public void uploadImageToFirebase(){ // uploads the image to firebase
        ProgressDialog mProgress;
        mProgress = new ProgressDialog(getContext());
        mProgress.setMessage("Creating Plant ...");
        mProgress.show();
        StorageReference filepath = mStorage.child("PlantPhotos").child(FirebaseAuth.getInstance().getCurrentUser().getEmail().toString()).child(enteredPlantName);
        filepath.putFile(takenImage).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) { mProgress.dismiss(); }
        });

    }


    @Override
    public void onResume() {
        super.onResume();
        getLatestPlantList();    // Query the database to get latest list
    }

    public static Fragment newInstance() {
        return new Plant_Cards_Fragment(); // new instance of the fragment
    }

    private void populateRecyclerView(ArrayList<Plant> plants){ // Bianca - changed this to accept a list parameter
        RecyclerViewAdapter adapter = new RecyclerViewAdapter(plants);
        recyclerView.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }


    // Queries the database to get the most recent list of plants
    public void getLatestPlantList() {
        ProgressDialog mProgress;
        mProgress = new ProgressDialog(getContext(), R.style.spinner);
        mProgress.setMessage("Getting your plants ...");
        mProgress.show();
        DbOps.instance.getPlantList(Objects.requireNonNull(FirebaseAuth.getInstance().getCurrentUser()).getEmail(),
                plantsFromDB -> {
                    if (plantsFromDB==null) return;

                    Log.d(TAG, "Obtained list of plants from DB of size: "+plantsFromDB.size());

                    // Refreshes the recyclerview:
                    plants = new ArrayList<>(plantsFromDB);
                    populateRecyclerView(new ArrayList<>(plantsFromDB)); // calling method to display the list
                    mProgress.dismiss();
                });
    }


    private class RecyclerViewHolder extends RecyclerView.ViewHolder{

        private CardView mCardView; // card for data display
        private TextView plantName; // plants name from firebase
        private TextView plantDetail; // plants detail (currently species)
        private ImageView plantImage; // plants picture


        RecyclerViewHolder(LayoutInflater inflater, ViewGroup container){
            super(inflater.inflate(R.layout.card_layout, container, false));
            //finding the location for each container in the display card
            mCardView = itemView.findViewById(R.id.card_view);
            plantName = itemView.findViewById(R.id.card_plant_name);
            plantDetail = itemView.findViewById(R.id.card_plant_detail);
            plantImage = itemView.findViewById(R.id.card_plant_image);

        }
    }

    private class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewHolder>{

        ArrayList<Plant> plantsList; // plants list

        RecyclerViewAdapter(ArrayList<Plant> list){
            this.plantsList = list;
        } // Adapter for the recycler view

        @NonNull
        @Override
        public RecyclerViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
            LayoutInflater inflater = LayoutInflater.from(getActivity()); // inflates the view to the fragment
            return new RecyclerViewHolder(inflater, viewGroup);
        }

        @Override
        public void onBindViewHolder(@NonNull RecyclerViewHolder recyclerViewHolder, int i) {
            ImageButton mImageButton = recyclerViewHolder.mCardView.findViewById(R.id.popup_menu); // creates the drop down menu in each card

            recyclerViewHolder.plantName.setText(plantsList.get(i).getName()); // populating the cards with the object details
            recyclerViewHolder.plantDetail.setText(plantsList.get(i).getSpecies());
            recyclerViewHolder.plantImage.setImageBitmap(byteArrayToBitmap(Bytes.toArray(plantsList.get(i).getPhoto())));

            //snackbar location
            //recyclerViewHolder.mCardView.setOnClickListener(v -> Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "Name: " + plantsList.get(i).getName(), Snackbar.LENGTH_SHORT).show());
            recyclerViewHolder.mCardView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Plant curPlant = plantsList.get(i);
                    AlertDialog.Builder viewbuilder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                    View scheduleViewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.individual_schedule_view, (ViewGroup) getView(), false);

                    ListView scheduleList = scheduleViewInflated.findViewById(R.id.individualScheduleList);
                    TextView name = scheduleViewInflated.findViewById(R.id.plantName);
                    TextView spec = scheduleViewInflated.findViewById(R.id.species);
                    ImageView plantpic = scheduleViewInflated.findViewById(R.id.plantPic);
                    name.setText(curPlant.getName());
                    spec.setText(curPlant.getSpecies());
                    plantpic.setImageBitmap(byteArrayToBitmap(Bytes.toArray(plantsList.get(i).getPhoto())));
                    plantpic.bringToFront();


                    DbOps.instance.getScheduleEntriesForPlant(curPlant, new DbOps.OnGetSchedulesForPlantFinishedListener() {
                        @Override
                        public void onGetSchedulesForPlantFinished(List<ScheduleEntry> scheduleEntries) {
                            if (scheduleEntries==null) {
                                String[] values = new String[] {"No schedule entries to display."};
                                ArrayAdapter<String> adapter = new ArrayAdapter<String>(Objects.requireNonNull(getContext()),
                                        R.layout.individual_schedule_view_item, R.id.schedule, values);
                                scheduleList.setAdapter(adapter);
                            }
                            else {
                                List<String> values = new ArrayList<String>();

                                for (ScheduleEntry entry : scheduleEntries) {
                                    // Simple approach - could be done differently
                                    String entryText = entry.getDay()+"s at "+entry.getTime()+" with quantity: "+entry.getQuantity()+"ml";
                                    values.add(entryText);
                                }

                                ArrayAdapter<String> adapter = new ArrayAdapter<String>(Objects.requireNonNull(getContext()),
                                        R.layout.individual_schedule_view_item, R.id.schedule, values);
                                scheduleList.setAdapter(adapter);
                            }
                        }
                    });
                    viewbuilder.setView(scheduleViewInflated);

                    // Sets document value to true in Users(col)/user(doc)/Triggers(col)/Trigger(doc)
                    // - has boolean field: Value
                    viewbuilder.setPositiveButton("Water now!", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                            builder.setTitle("Water "+curPlant.getName()+" now!");
                            builder.setMessage("This will trigger Eden to water "+curPlant.getName()+" now. Continue?");
                            builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    DbOps.instance.setWaterNowTrigger(new DbOps.onSetWaterNowFinishedListener() {
                                        @Override
                                        public void onSetWaterFinished(boolean success) {
                                            if (success) Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "Eden will water "+curPlant.getName()+" now!", Snackbar.LENGTH_SHORT).show();
                                            else Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "Database error. Try again!", Snackbar.LENGTH_SHORT).show();
                                        }
                                    });
                                }
                            });
                            AlertDialog viewdialog = builder.create();
                            viewdialog.show();
                        }
                    });

                    AlertDialog viewdialog = viewbuilder.create();
                    viewdialog.show();
                }
            });

            //calls method to display menu
            mImageButton.setOnClickListener(v -> showPopupMenu(mImageButton, i));
        }

        private void showPopupMenu(View view,int position) {
            // inflate menu
            Context wrapper = new ContextThemeWrapper(getContext(), R.style.popupMenu);
            PopupMenu popup = new PopupMenu(wrapper,view );
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


    class MyMenuItemClickListener implements PopupMenu.OnMenuItemClickListener { // class for when an item is clicked withing the popup menu

        private int position;
        MyMenuItemClickListener(int positon) {
            this.position=positon;
        }

        @Override
        public boolean onMenuItemClick(MenuItem menuItem) {
            switch (menuItem.getItemId()) {

                case R.id.card_delete: // delete is selected
                    DbOps.instance.deletePlant(plants.get(position), success -> getLatestPlantList());
                    return true;

                case R.id.card_edit: // edit is selected

                    Plant currentPlant = plants.get(position);

                    AlertDialog.Builder editbuilder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                    //editbuilder.setTitle("Edit plant name");

                    View editviewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.fragment_edit_plant,
                            (ViewGroup) getView(), false);

                    final EditText newPlantName = editviewInflated.findViewById(R.id.plantName);
                    newPlantName.setHint(currentPlant.getName());

                    final Spinner newPlantSpecies = editviewInflated.findViewById(R.id.plantSpecies);
                    newPlantSpecies.setPrompt(currentPlant.getSpecies());
                    // TODO: perhaps changing specicies to a short description of the plant (E.G. location or characteristic)
                    String[] species = new String[]{"Select Species","cacti","daisy","lily","orchid"};
                    ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(Objects.requireNonNull(getContext()), R.layout.species_option, species);
                    newPlantSpecies.setAdapter(speciesAdapter);

                    editbuilder.setView(editviewInflated);

                    editbuilder.setPositiveButton("Change name", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            if (newPlantName.getText().toString().trim().length() != 0) {
                                DbOps.instance.editPlantName(currentPlant, newPlantName.getText().toString(), new DbOps.onEditPlantFinishedListener() {
                                    @Override
                                    public void onEditPlantFinished(boolean success) {
                                        getLatestPlantList();
                                        Toast.makeText(getContext(), "Successfully changed name!", Toast.LENGTH_SHORT).show();
                                    }
                                });
                            }
                            else Toast.makeText(getContext(), "Invalid new plant name. Please use a valid name.", Toast.LENGTH_SHORT).show();
                        }
                    });
                    editbuilder.setNeutralButton("Change species", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            if (!newPlantSpecies.getSelectedItem().toString().equals("Select Species")) {
                                DbOps.instance.editPlantSpecies(currentPlant, newPlantSpecies.getSelectedItem().toString(), new DbOps.onEditPlantFinishedListener() {
                                    @Override
                                    public void onEditPlantFinished(boolean success) {
                                        getLatestPlantList();
                                        Toast.makeText(getContext(), "Successfully changed species!", Toast.LENGTH_SHORT).show();
                                    }
                                });
                            }
                            else Toast.makeText(getContext(), "No species selected. Please select species.", Toast.LENGTH_SHORT).show();
                        }
                    });
                    AlertDialog editdialog = editbuilder.create();
                    editdialog.show();
                    return true;
            }
            return false;
        }
    }
}

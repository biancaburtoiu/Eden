package com.sdp.eden;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.VectorDrawable;
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
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.NumberPicker;
import android.widget.PopupMenu;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;

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
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import com.github.clans.fab.FloatingActionButton;
import com.github.clans.fab.FloatingActionMenu;

import static android.app.Activity.RESULT_OK;

public class Plant_Cards_Fragment extends Fragment {

    private static final String TAG = "Plant_Cards_Fragment";
    private ArrayList<Plant> plants; // list of plants pulled from firebase
    private ArrayList<ScheduleEntry> schedules;

    private RecyclerView plantsRV;
    private RecyclerView schedulesRV;

    private ImageView plantPic;
    private StorageReference mStorage = FirebaseStorage.getInstance().getReference();
    private String enteredPlantName; // this will hopefully be temp
    private Uri takenImage; // once again hopeful;ly this will be temp!
    private int width, height;


    FloatingActionMenu materialDesignFAM;
    FloatingActionButton fab_addPlant, fab_addSchedule;

    @Override
    public void onResume() {
        super.onResume();
        getLatestPlantList();    // Query the database to get latest list
    }

    public static Fragment newInstance() {
        return new Plant_Cards_Fragment(); // new instance of the fragment
    }


    public View onCreateView (@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
        View view = inflater.inflate(R.layout.fragment_plants, container, false);
        getLatestPlantList();    // Query the database to get latest list
        plantsRV = view.findViewById(R.id.Plants_Recycler_view);
        
        // https://www.viralandroid.com/2016/02/android-floating-action-menu-example.html
        materialDesignFAM = (FloatingActionMenu) view.findViewById(R.id.material_design_android_floating_action_menu);
        fab_addPlant = (FloatingActionButton) view.findViewById(R.id.material_design_floating_action_menu_item1);
        fab_addSchedule = (FloatingActionButton) view.findViewById(R.id.material_design_floating_action_menu_item2);

        width = (int)(getResources().getDisplayMetrics().widthPixels*0.90);
        height = (int)(getResources().getDisplayMetrics().heightPixels*0.70);

        materialDesignFAM.setClosedOnTouchOutside(true);


        fab_addPlant.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Log.d(TAG, "User input: click on Add");

                AlertDialog.Builder builder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                View viewInflated = LayoutInflater.from(getActivity()).inflate(R.layout.fragment_add_plant, (ViewGroup) getView(), false);

                final EditText plantName = viewInflated.findViewById(R.id.plantName);
                final Spinner plantSpecies = viewInflated.findViewById(R.id.plantSpecies);
                final NumberPicker petalPicker = viewInflated.findViewById(R.id.petalPicker);

                plantPic = viewInflated.findViewById(R.id.plantPic);
                builder.setView(viewInflated);

                String[] species = new String[]{"Select Species","cacti","daisy","lily","orchid"};
                ArrayAdapter<String> speciesAdapter = new ArrayAdapter<>(Objects.requireNonNull(getContext()), R.layout.species_option, species);
                plantSpecies.setAdapter(speciesAdapter); // creates the drop down selection

                //Petal picker setup
                petalPicker.setMinValue(1);
                petalPicker.setMaxValue(7);
                petalPicker.setWrapSelectorWheel(false);

                // Disables keyboard on clicks outside the EditText
                // https://stackoverflow.com/a/19828165/7038747
                plantName.setOnFocusChangeListener(new View.OnFocusChangeListener() {
                    @Override
                    public void onFocusChange(View v, boolean hasFocus) {
                        if (!hasFocus) {
                            hideKeyboard(v);
                        }
                    }
                });
                plantSpecies.setOnTouchListener(new View.OnTouchListener() {
                    @Override
                    public boolean onTouch(View v, MotionEvent event) {
                        hideKeyboard(v);
                        return false;
                    }
                });


                plantPic.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        enteredPlantName = plantName.getText().toString().trim(); // this is currently not used.
                        // When this starts and the plant has no name yet, it would be saved as blank name
                        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE); // kieran - opens camera

                        if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
                            startActivityForResult(takePictureIntent, 111); // set the request code for the photo to 111
                        }
                    }
                });

                builder.setPositiveButton("Next", (dialog, which) -> {
                    Log.d(TAG, "New plant to add to database:");
                    Log.d(TAG, "Plant name: " + plantName.getText().toString());
                    Log.d(TAG, "Plant species: " + plantSpecies.getSelectedItem().toString()); // extracts the plant data from user input
                    Log.d(TAG, "Number of petals: "+petalPicker.getValue());

                    // Sanity checks before continuing
                    if (plantName.getText().toString().trim().length() == 0) {
                        Log.d(TAG, "Plant name format incorrect. Rejected further operations.");
                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "You must enter a plant name!", Snackbar.LENGTH_SHORT).show();
                    }
                    else if (plantSpecies.getSelectedItem().toString().equals("Select Species")){
                        Log.d(TAG, "Empty plant species selection. Rejected further operations.");
                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "You must select a species!", Snackbar.LENGTH_SHORT).show();
                    }
                    else {
                        Log.d(TAG, "Plant name format correct.");
                        Log.d(TAG, "Going to pick coordinates...");

                        // TODO: Go to the fragment
                        AlertDialog.Builder builder1 = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
                        View viewInflated1 = LayoutInflater.from(getActivity()).inflate(R.layout.picturetag_main, (ViewGroup) getView(), false);
                        View img = viewInflated1.findViewById(R.id.overhead_image);
                        Bitmap bmp = BitmapFactory.decodeResource(getResources(), R.drawable.overhead_image);
                        Drawable d = new BitmapDrawable(getResources(), bmp);
                        img.setBackground(d);
                        builder1.setView(viewInflated1);

                        builder1.setPositiveButton("Create plant", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                ProgressDialog mProgress;
                                mProgress = new ProgressDialog(getContext(), R.style.spinner);
                                mProgress.setMessage("Creating the plant ...");
                                mProgress.setCanceledOnTouchOutside(false);
                                mProgress.show();

                                List<Float> coordinates = PictureTagMain.getPointCoordinatesFromRoom(getActivity());
                                Log.d("Coords", coordinates.toString());

                                if (coordinates.get(0) < 0f) coordinates.set(0, 0f);
                                if (coordinates.get(0) > 1f) coordinates.set(0, 1f);
                                if (coordinates.get(1) < 0f) coordinates.set(1, 0f);
                                if (coordinates.get(1) > 1f) coordinates.set(1, 1f);

                                float x = PictureTagLayout.returnX();
                                float y = PictureTagLayout.returnY();

                                Log.d("CoordsRaw", x + ", " + y);

                                // TODO: Reject continuing if coords are incorrect!!!

                                // Generating plant icon
                                Bitmap defaultPlant = BitmapFactory.decodeResource(getContext().getResources(), R.drawable.def_plant_icon);
                                ByteArrayOutputStream out = new ByteArrayOutputStream();
                                defaultPlant.compress(Bitmap.CompressFormat.PNG, 0, out);
                                Bitmap decoded = BitmapFactory.decodeStream(new ByteArrayInputStream(out.toByteArray()));

                                List<Integer> image;

                                if (imageBitmap == null) {
                                    image = bitmapToIntegerList(defaultPlant);
                                } else {
                                    image = bitmapToIntegerList(imageBitmap);
                                }

                                //TODO: Adapt coordinates to what robot uses.
                                Plant plant = new Plant(
                                        plantName.getText().toString(),
                                        plantSpecies.getSelectedItem().toString(),
                                        image,
                                        petalPicker.getValue(),
                                        coordinates.get(0),
                                        coordinates.get(1)
                                );

                                DbOps.instance.addPlant(plant, new DbOps.onAddPlantFinishedListener() {
                                    @Override
                                    public void onUpdateFinished(boolean success) {
                                        //uploadImageToFirebase(); // completes the new plant
                                        getLatestPlantList();

                                        mProgress.dismiss();
                                        materialDesignFAM.close(false);
                                    }
                                });
                            }
                        });

                        // Adds cancel in overhead image plant creation step
                        builder1.setNeutralButton("Cancel", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                // nothing happens
                            }
                        });

                        AlertDialog dialog1 = builder1.create();
                        dialog1.setCanceledOnTouchOutside(false);
                        dialog1.show();
                        //dialog1.getWindow().setLayout(width, height);
                    }
                });

                // Adds cancel in plant data plant creation step
                builder.setNeutralButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // nothing happens
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.setCanceledOnTouchOutside(false);
                dialog.show();
                //dialog.getWindow().setLayout(width, height);

            }
        });

        fab_addSchedule.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()), R.style.Dialog);
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

                final NumberPicker quantityPicker = viewInflated.findViewById(R.id.quantityPicker);
                quantityPicker.setWrapSelectorWheel(false);
                quantityPicker.setMinValue(0);
                quantityPicker.setMaxValue(6);
                quantityPicker.setDisplayedValues(new String[] {"10","25","50","75","100","125","150"});

                builder.setView(viewInflated);

                builder.setPositiveButton("Set", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                        ProgressDialog mProgress;
                        mProgress = new ProgressDialog(getContext(), R.style.spinner);
                        mProgress.setMessage("Planning a watering...");
                        mProgress.setCanceledOnTouchOutside(false);
                        mProgress.show();

                        String currentPlantName = plantSelect.getSelectedItem().toString();
                        Plant currentPlant = plants.stream().filter(p -> p.getName() == currentPlantName)
                                .findFirst().orElse(null);

                        String time;
                        if (timePicker.getMinute()<10)
                            time = timePicker.getHour()+":0"+timePicker.getMinute();
                        else
                            time = timePicker.getHour()+":"+timePicker.getMinute();

                        if (timePicker.getHour()<10) time = "0"+time;

                        String selectedDay = dayOfWeekPicker.getSelectedItem().toString();
                        int dayToNumber;
                        switch (selectedDay) {
                            case "Monday": dayToNumber=0; break;
                            case "Tuesday": dayToNumber=1; break;
                            case "Wednesday": dayToNumber=2; break;
                            case "Thursday": dayToNumber=3; break;
                            case "Friday": dayToNumber=4; break;
                            case "Saturday": dayToNumber=5; break;
                            default: dayToNumber=6; break;
                        }

                        // Sanity checks before continuing
                        if(currentPlantName.equals("Select Plant")){
                            Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "You must select a plant!", Snackbar.LENGTH_SHORT).show();
                        }
                        else if (selectedDay.equals("Select Day")) {
                            Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack), "You must select the day of week!", Snackbar.LENGTH_SHORT).show();
                        }
                        else {
                            Log.d(TAG, "Quantity picker result: "+quantityPicker.getValue());
                            int quantity = Integer.parseInt(quantityPicker.getDisplayedValues()[quantityPicker.getValue()]);

                            ScheduleEntry scheduleEntry = new ScheduleEntry(dayToNumber, currentPlantName, quantity, time,
                                    currentPlant.getNoOfPetals(),
                                    currentPlant.getXCoordinate(), currentPlant.getYCoordinate(),
                                    true);

                            DbOps.instance.addScheduleEntry(scheduleEntry, new DbOps.onAddScheduleEntryFinishedListener() {
                                @Override
                                public void onAddScheduleEntryFinished(boolean success) {
                                    if (success)
                                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                "Added watering schedule entry for "+ currentPlantName + " on "+selectedDay+ "s at "
                                                        + scheduleEntry.getTime()+ "!", Snackbar.LENGTH_SHORT).show();
                                    else
                                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                "Could not add watering schedule entry for "+ currentPlantName +".", Snackbar.LENGTH_SHORT).show();
                                    mProgress.dismiss();
                                }
                            });
                        }
                    }
                });
                builder.setNeutralButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // nothing happens
                    }
                });
                AlertDialog dialog = builder.create();
                dialog.setCanceledOnTouchOutside(false);
                dialog.show();
            }
        });

        plantsRV.setLayoutManager(new LinearLayoutManager(getActivity())); // sets layout for recycler view, linear list in this case
        return view;
    }


    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
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
        mProgress.setCanceledOnTouchOutside(false);
        mProgress.show();
        StorageReference filepath = mStorage.child("PlantPhotos").child(FirebaseAuth.getInstance().getCurrentUser().getEmail().toString()).child(enteredPlantName);
        filepath.putFile(takenImage).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) { mProgress.dismiss(); }
        });

    }

    private void populatePlantsRecyclerView(ArrayList<Plant> plants){ // Bianca - changed this to accept a list parameter
        RecyclerViewAdapter adapter = new RecyclerViewAdapter(plants);
        plantsRV.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }

    private void populateSchedulesRecyclerView(ArrayList<ScheduleEntry> schedules) {
        ScheduleRVAdapter adapter = new ScheduleRVAdapter(schedules);
        schedulesRV.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }

    public void getLatestSchedulesList(Plant plant) {
        DbOps.instance.getScheduleEntriesForPlant(plant, new DbOps.OnGetSchedulesForPlantFinishedListener() {
            @Override
            public void onGetSchedulesForPlantFinished(List<ScheduleEntry> scheduleEntries) {
                if (scheduleEntries==null) populateSchedulesRecyclerView(new ArrayList<>());
                else {
                    Log.d(TAG, "Obtained schedules list of size: "+scheduleEntries.size());

                    //Refreshes the recyclerview:
                    schedules = new ArrayList<>(scheduleEntries);
                    populateSchedulesRecyclerView(new ArrayList<>(scheduleEntries));
                }
            }
        });
    }

    // Queries the database to get the most recent list of plants
    public void getLatestPlantList() {
        ProgressDialog mProgress;
        mProgress = new ProgressDialog(getContext(), R.style.spinner);
        mProgress.setMessage("Getting your plants ...");
        mProgress.setCanceledOnTouchOutside(false);
        mProgress.show();
        DbOps.instance.getPlantList(Objects.requireNonNull(FirebaseAuth.getInstance().getCurrentUser()).getEmail(),
                plantsFromDB -> {
                    if (plantsFromDB==null) {
                        populatePlantsRecyclerView(new ArrayList<>());
                    }
                    else {
                        Log.d(TAG, "Obtained list of plants from DB of size: "+plantsFromDB.size());

                        // Refreshes the recyclerview:
                        plants = new ArrayList<>(plantsFromDB);
                        populatePlantsRecyclerView(new ArrayList<>(plantsFromDB)); // calling method to display the list
                    }
                    mProgress.dismiss();
                });
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
                    AlertDialog.Builder deleteBuilder = new AlertDialog.Builder(Objects.requireNonNull(getActivity()));
                    deleteBuilder.setTitle("Delete "+plants.get(position).getName());
                    deleteBuilder.setMessage("Are you sure you want to delete "+plants.get(position).getName()+"? " +
                            "This action cannot be undone.");
                    deleteBuilder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            ProgressDialog mProgress;
                            mProgress = new ProgressDialog(getContext(), R.style.spinner);
                            mProgress.setMessage("Deleting the plant...");
                            mProgress.setCanceledOnTouchOutside(false);
                            mProgress.show();

                            DbOps.instance.deletePlant(plants.get(position), success -> {
                                if (success) {
                                    Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                            "Successfully deleted plant!", Snackbar.LENGTH_SHORT).show();
                                    getLatestPlantList();
                                }
                                else {
                                    Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                            "Could not delete plant. Please try again!", Snackbar.LENGTH_SHORT).show();
                                    getLatestPlantList();
                                }
                                mProgress.dismiss();
                            });
                        }
                    });
                    deleteBuilder.setNeutralButton("Cancel", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // nothing happens
                        }
                    });
                    AlertDialog deleteDialog = deleteBuilder.create();
                    deleteDialog.setCanceledOnTouchOutside(false);
                    deleteDialog.show();
                    return true;
            }
            return false;
        }
    }


    // Recyclerview Holders & Adapters:

    private class ScheduleRVHolder extends RecyclerView.ViewHolder{
        private TextView day;
        private TextView time;
        private TextView quantity;
        private Button deleteWateringButton;

        ScheduleRVHolder(@NonNull View itemView){
            super(itemView);
            day = itemView.findViewById(R.id.day);
            time = itemView.findViewById(R.id.time);
            quantity = itemView.findViewById(R.id.quantity);
            deleteWateringButton = itemView.findViewById(R.id.deleteWateringButton);
        }
    }

    private class ScheduleRVAdapter extends RecyclerView.Adapter<ScheduleRVHolder> {
        ArrayList<ScheduleEntry> scheduleEntriesList;

        ScheduleRVAdapter(ArrayList<ScheduleEntry> list) {
            this.scheduleEntriesList = list;
        }

        @Override
        public int getItemCount() {
            return scheduleEntriesList.size();
        }

        @NonNull
        @Override
        public ScheduleRVHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
            View v = LayoutInflater.from(viewGroup.getContext())
                    .inflate(R.layout.individual_schedule_view_item, viewGroup, false);
            return new ScheduleRVHolder(v);
        }

        @Override
        public void onBindViewHolder(@NonNull ScheduleRVHolder scheduleRVHolder, int i) {
            String dayAsText;
            switch (scheduleEntriesList.get(i).getDay()) {
                case 0: dayAsText="Monday"; break;
                case 1: dayAsText="Tuesday"; break;
                case 2: dayAsText="Wednesday"; break;
                case 3: dayAsText="Thursday"; break;
                case 4: dayAsText="Friday"; break;
                case 5: dayAsText="Saturday"; break;
                default: dayAsText="Sunday"; break;
            }
            scheduleRVHolder.day.setText(dayAsText);
            scheduleRVHolder.time.setText(scheduleEntriesList.get(i).getTime());
            scheduleRVHolder.quantity.setText(scheduleEntriesList.get(i).getQuantity()+"ml");
            scheduleRVHolder.deleteWateringButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
                    builder.setTitle("Delete schedule entry");
                    builder.setMessage("Are you sure you want to delete this entry? This action cannot be undone.");

                    builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            DbOps.instance.deleteScheduleEntryOfPlant(scheduleEntriesList.get(i), new DbOps.onDeletePlantScheduleFinishedListener() {
                                @Override
                                public void onDeleteScheduleFinished(boolean success) {
                                    if (success) {
                                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                "Successfully deleted schedule entry!", Snackbar.LENGTH_SHORT).show();
                                        Plant curPlant = plants.stream()
                                                .findFirst()
                                                .filter(plant -> plant.getName().equals(scheduleEntriesList.get(i).getPlantName()))
                                                .orElse(null);
                                        getLatestSchedulesList(curPlant);

                                    }
                                    else
                                        Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                "Could not delete schedule entry. Please retry!", Snackbar.LENGTH_SHORT).show();
                                }
                            });
                        }
                    });
                    builder.setNeutralButton("Cancel", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // do nothing
                        }
                    });
                    AlertDialog dialog = builder.create();
                    dialog.setCanceledOnTouchOutside(false);
                    dialog.show();
                }
            });
        }
    }

    private class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewHolder>{

        ArrayList<Plant> plantsList;

        RecyclerViewAdapter(ArrayList<Plant> list) {
            this.plantsList = list;
        }

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

                    schedulesRV = scheduleViewInflated.findViewById(R.id.individualScheduleRecyclerView);
                    schedulesRV.setLayoutManager(new LinearLayoutManager(getActivity()));

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
                                ScheduleRVAdapter scheduleRVAdapter = new ScheduleRVAdapter(new ArrayList<>());
                                schedulesRV.setAdapter(scheduleRVAdapter);
                            }
                            else {
                                // for safety. not necessary
                                List<ScheduleEntry> correctEntries = scheduleEntries.stream()
                                                    .filter(entry -> entry.getValid()).collect(Collectors.toList());
                                ScheduleRVAdapter scheduleRVAdapter = new ScheduleRVAdapter(new ArrayList<>(correctEntries));
                                schedulesRV.setAdapter(scheduleRVAdapter);
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
                                    DbOps.instance.setWaterNowTrigger(curPlant,new DbOps.onSetWaterNowFinishedListener() {
                                        @Override
                                        public void onSetWaterFinished(boolean success) {
                                            if (success)
                                                Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                        "Eden will water "+curPlant.getName()+" now!", Snackbar.LENGTH_SHORT).show();
                                            else
                                                Snackbar.make(Objects.requireNonNull(getView()).findViewById(R.id.viewSnack),
                                                        "Database error. Try again!", Snackbar.LENGTH_SHORT).show();
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


    // Bitmap image helper methods:
    private static Bitmap getBitmap(VectorDrawable vectorDrawable) {
        Bitmap bitmap = Bitmap.createBitmap(vectorDrawable.getIntrinsicWidth(),
                vectorDrawable.getIntrinsicHeight(), Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        vectorDrawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight());
        vectorDrawable.draw(canvas);
        return bitmap;
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

    // https://stackoverflow.com/a/19828165/7038747
    public void hideKeyboard(View view) {
        InputMethodManager inputMethodManager =(InputMethodManager) getActivity()
                .getSystemService(Objects.requireNonNull(getActivity()).INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(view.getWindowToken(), 0);
    }
}

package com.sdp.eden;

import android.support.annotation.NonNull;
import android.util.Log;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.firebase.firestore.WriteBatch;

import java.util.ArrayList;
import java.util.List;

public class DbOps {
    private static final String TAG = "DbOps";


    FirebaseFirestore db = FirebaseFirestore.getInstance();

    public static final DbOps instance = new DbOps();

    //Puts plant into Users/CurrentUserEmail/Plants
    void addPlant(Plant plant, onAddPlantFinishedListener listener) {

        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(plant.getName()).set(plant) // Kieran - changed so the id is now the plant name
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()) {
                            listener.onUpdateFinished(true);
                            Log.d(TAG, "Plant: "+plant.getName()+" successfully added to database!");
                        }
                        else {
                            listener.onUpdateFinished(false);
                            Log.d(TAG, "Could not add plant: "+plant.getName()+" to database.");
                        }
                    }
                });
    }


    //Gets all available plants from Users/CurrentUserEmail/Plants
    void getPlantList(String user_email, OnGetPlantListFinishedListener listener) {

        db.collection("Users")
                .document(user_email)
                .collection("Plants")
                .get()
                .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                    @Override
                    public void onComplete(@NonNull Task<QuerySnapshot> task) {
                        if (task.getResult().isEmpty()) {
                            Log.d(TAG, "Get PlantList unsuccessful.");
                            listener.onGetPlantListFinished(new ArrayList<Plant>());
                        }
                        else {
                            Log.d(TAG, "Get PlantList successful!");
                            List<Plant> plants = task.getResult().toObjects(Plant.class);
                            listener.onGetPlantListFinished(plants);
                        }
                    }
                });
    }

    void addScheduleEntry(ScheduleEntry scheduleEntry, onAddScheduleEntryFinishedListener listener){
        // Sets the name of the database document to something user-friendly
        String scheduleString = scheduleEntry.getDay()+"-"+
                                scheduleEntry.getTime()+"-"+scheduleEntry.getQuantity()+"ml";

        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Schedules")
                .document(scheduleString).set(scheduleEntry)
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()) {
                            listener.onAddScheduleEntryFinished(true);
                            Log.d(TAG, "Schedule for plant: "+scheduleEntry.getPlantName()+" successfully added to database!");
                        }
                        else {
                            listener.onAddScheduleEntryFinished(false);
                            Log.d(TAG, "Could not add schedule entry for plant: "+scheduleEntry.getPlantName()+" to database.");
                        }
                    }
                });
    }

    void getScheduleEntriesForPlant(Plant plant, OnGetSchedulesForPlantFinishedListener listener) {
        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Schedules")
                .whereEqualTo("plantName", plant.getName())
                .get().addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
            @Override
            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                if (!task.getResult().isEmpty()) {
                    List<ScheduleEntry> scheduleEntries = task.getResult().toObjects(ScheduleEntry.class);
                    Log.d(TAG, "Retrieved scheduleEntries for plant " + plant.getName() + " size: " + scheduleEntries.size());
                    listener.onGetSchedulesForPlantFinished(scheduleEntries);
                } else listener.onGetSchedulesForPlantFinished(null);
            }
        });
    }

    void getAllScheduleEntries(OnGetAllSchedulesFinishedListener listener) {
        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Schedules")
                .get().addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
            @Override
            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                if (!task.getResult().isEmpty()) {
                    List<ScheduleEntry> scheduleEntries = task.getResult().toObjects(ScheduleEntry.class);
                    Log.d(TAG, "Retrieved scheduleEntries size: "+scheduleEntries.size());
                    listener.onGetAllSchedulesFinished(scheduleEntries);
                }
                else listener.onGetAllSchedulesFinished(null);
            }
        });
    }


    // deletes plant from firebase
    void deletePlant(Plant plant, onDeletePlantFinishedListener listener){
        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(plant.getName()).delete().addOnCompleteListener(new OnCompleteListener<Void>() {
            @Override
            public void onComplete(@NonNull Task<Void> task) {
                if (task.isSuccessful()) {
                    Log.d(TAG, "Task was successful, entering deleteSchedulesOfPlant");
                    deleteSchedulesOfPlant(plant, listener);
                } else {
                    listener.onDeletePlantFinished(false);
                    Log.d(TAG, "Could not delete plant");
                }
            }
        });
    }

    void deleteSchedulesOfPlant(Plant plant, onDeletePlantFinishedListener listener) {
        // Gets the schedule entries of that specific plant and then removes them in a batch operation.

        WriteBatch batch1 = db.batch();

        DbOps.instance.getScheduleEntriesForPlant(plant, new DbOps.OnGetSchedulesForPlantFinishedListener() {
            @Override
            public void onGetSchedulesForPlantFinished(List<ScheduleEntry> scheduleEntries) {
                if (scheduleEntries==null) {
                    Log.d(TAG, "No schedules to delete.");
                    return;
                }

                for (ScheduleEntry scheduleEntry : scheduleEntries) {
                    String scheduleString = scheduleEntry.getDay() + "-" +
                            scheduleEntry.getTime() + "-" + scheduleEntry.getQuantity() + "ml";
                    Log.d(TAG, "(Deleting: ) Schedule string: " + scheduleString);

                    DocumentReference scheduleToRemove =
                            db.collection("Users")
                                    .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                                    .collection("Schedules")
                                    .document(scheduleString);
                    batch1.delete(scheduleToRemove);
                }

                batch1.commit().addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()){
                            Log.d(TAG, "Successfully removed schedule entries for plant");
                            Log.d(TAG, "AND Successfully removed plant");
                            listener.onDeletePlantFinished(true);
                        }
                        else {
                            Log.d(TAG, "Could not remove schedule entries for plant");
                            Log.d(TAG, "And could not remove plant");
                            listener.onDeletePlantFinished(false);
                        }
                    }
                });
            }
        });
    }

    void editPlantName(Plant oldPlant, String newName, onEditPlantFinishedListener listener) {
        WriteBatch batch = db.batch();

        // Create new plant with same properties but new name
        DocumentReference creator = db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(newName);
        batch.set(creator, new Plant(newName, oldPlant.getSpecies(), oldPlant.getPhoto()));

        // Remove current plant document
        DocumentReference remover = db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(oldPlant.getName());
        batch.delete(remover);

        // Update schedule entries for old plant name with new plant name
        DbOps.instance.getScheduleEntriesForPlant(oldPlant, new OnGetSchedulesForPlantFinishedListener() {
            @Override
            public void onGetSchedulesForPlantFinished(List<ScheduleEntry> scheduleEntries) {
                if (scheduleEntries==null) {
                    Log.d(TAG, "No schedules to delete.");
                }
                else {
                    for (ScheduleEntry scheduleEntry : scheduleEntries) {
                        String scheduleString = scheduleEntry.getDay() + "-" +
                                scheduleEntry.getTime() + "-" + scheduleEntry.getQuantity() + "ml";
                        Log.d(TAG, "(Editing: ) Schedule string: " + scheduleString);

                        DocumentReference scheduleToUpdate =
                                db.collection("Users")
                                        .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                                        .collection("Schedules")
                                        .document(scheduleString);
                        batch.set(scheduleToUpdate, new ScheduleEntry(scheduleEntry.getDay(), newName,
                                scheduleEntry.getQuantity(), scheduleEntry.getTime()));
                    }
                }

                batch.commit().addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()) {
                            listener.onEditPlantFinished(true);
                            Log.d(TAG, "Edit plant name finished!");
                        }
                        else {
                            listener.onEditPlantFinished(false);
                            Log.d(TAG, "Could not edit plant name.");
                        }
                    }
                });
            }
        });
    }

    void editPlantSpecies(Plant oldPlant, String newSpecies, onEditPlantFinishedListener listener) {
        WriteBatch batch = db.batch();

        // Create new plant with same properties but new species (this will just update the document)
        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(oldPlant.getName())
                .update("species", newSpecies)
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()) {
                            Log.d(TAG, "Successfully modified plant species.");
                            listener.onEditPlantFinished(true);
                        }
                        else {
                            Log.d(TAG, "Could not modify plant species.");
                            listener.onEditPlantFinished(false);
                        }
                    }
                });
    }

    interface onAddPlantFinishedListener {
        void onUpdateFinished(boolean success);
    }

    interface onAddScheduleEntryFinishedListener {
        void onAddScheduleEntryFinished(boolean success);
    }

    interface OnGetPlantListFinishedListener {
        void onGetPlantListFinished(List<Plant> plants);
    }

    interface OnGetSchedulesForPlantFinishedListener {
        void onGetSchedulesForPlantFinished(List<ScheduleEntry> scheduleEntries);
    }

    interface OnGetAllSchedulesFinishedListener {
        void onGetAllSchedulesFinished(List<ScheduleEntry> scheduleEntries);
    }

    interface onDeletePlantFinishedListener {
        void onDeletePlantFinished(boolean success);
    }

    interface onEditPlantFinishedListener {
        void onEditPlantFinished(boolean success);
    }


}

package com.sdp.eden;

import android.support.annotation.NonNull;
import android.util.Log;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;

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

    // deletes plant from firebase
    void deletePlant(Plant plant, onDeletePlantFinishedListener listener){
        db.collection("Users")
                .document(FirebaseAuth.getInstance().getCurrentUser().getEmail())
                .collection("Plants")
                .document(plant.getName()).delete().addOnCompleteListener(new OnCompleteListener<Void>() {
            @Override
            public void onComplete(@NonNull Task<Void> task) {
                if (task.isSuccessful()) {
                    listener.onDeletePlantFinished(true);
                    Log.d(TAG, "Plant Deleted");
                } else {
                    listener.onDeletePlantFinished(false);
                    Log.d(TAG, "Could not delete plant");
                }
            }
        });
    }

    interface onAddPlantFinishedListener {
        void onUpdateFinished(boolean success);
    }

    interface OnGetPlantListFinishedListener {
        void onGetPlantListFinished(List<Plant> plants);
    }

    interface onDeletePlantFinishedListener {
        void onDeletePlantFinished(boolean success);
    }
}

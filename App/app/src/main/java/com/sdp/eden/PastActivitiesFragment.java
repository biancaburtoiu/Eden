package com.sdp.eden;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class PastActivitiesFragment extends Fragment {

    private static final String TAG = "PastActivitiesFragment";
    private RecyclerView pastActivitiesRV;
    private TextView noEntriesText;

//    public static Fragment newInstance() {
//        return new PastActivitiesFragment();
//    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v =  inflater.inflate(R.layout.fragment_past_activities,container,false);

        pastActivitiesRV = v.findViewById(R.id.pastActivities);
        noEntriesText = v.findViewById(R.id.emptyPV);

        pastActivitiesRV.setLayoutManager(new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false));
        pastActivitiesRV.setAdapter(new PastActivitiesAdapter(new ArrayList<>()));

        return v;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        refreshPastActivities();
    }

    public void refreshPastActivities() {
        DbOps.instance.getPlantList(Objects.requireNonNull(FirebaseAuth.getInstance().getCurrentUser()).getEmail(), new DbOps.OnGetPlantListFinishedListener() {
            @Override
            public void onGetPlantListFinished(List<Plant> plants) {

                if (plants.size()==0) {
                    pastActivitiesRV.setVisibility(View.GONE);
                    noEntriesText.setVisibility(View.VISIBLE);
                }
                else {
                    pastActivitiesRV.setVisibility(View.VISIBLE);
                    noEntriesText.setVisibility(View.GONE);

                    PastActivitiesAdapter adapter = new PastActivitiesAdapter(new ArrayList<>(plants));
                    pastActivitiesRV.setAdapter(adapter);
                    //adapter.notifyDataSetChanged();
                }
            }
        });
    }


    private class PastActivitiesRVHolder extends RecyclerView.ViewHolder{
        private TextView plant;
        private TextView lastWatered;

        PastActivitiesRVHolder(@NonNull View itemView){
            super(itemView);
            plant = itemView.findViewById(R.id.plant);
            lastWatered = itemView.findViewById(R.id.lastWatered);
        }
    }

    private class PastActivitiesAdapter extends RecyclerView.Adapter<PastActivitiesRVHolder>{

        ArrayList<Plant> plantsList;

        PastActivitiesAdapter(ArrayList<Plant> list) {
            this.plantsList = list;
        }

        @NonNull
        @Override
        public PastActivitiesRVHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
            return new PastActivitiesRVHolder(LayoutInflater.from(viewGroup.getContext())
                    .inflate(R.layout.individual_past_activity_item, viewGroup, false));
        }

        @Override
        public void onBindViewHolder(@NonNull PastActivitiesRVHolder recyclerViewHolder, int i) {
            recyclerViewHolder.plant.setText(plantsList.get(i).getName());
            recyclerViewHolder.lastWatered.setText("petals: " + plantsList.get(i).getNoOfPetals());
        }


        @Override
        public int getItemCount() {
            return plantsList.size();
        }
    }

}

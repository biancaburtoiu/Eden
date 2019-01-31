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
import android.widget.Button;

import java.util.ArrayList;
import java.util.List;

public class PlantListFragment extends Fragment {
    View v;

    private RecyclerView myrecyclerview;
    private List<Plant> plants;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.fragment_placeholder1,container,false);

        //setting up Layout Manager and adapter for recyclerview
        myrecyclerview = v.findViewById(R.id.plant_recyclerview);
        RecyclerViewAdapter recyclerAdapter = new RecyclerViewAdapter(getContext(),plants);
        myrecyclerview.setLayoutManager(new LinearLayoutManager(getActivity()));
        myrecyclerview.setAdapter(recyclerAdapter);

        // TODO: Set recyclerview to grab plants list by querying the database
        Button addPlantButton = v.findViewById(R.id.addPlantButton);
        addPlantButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getFragmentManager().beginTransaction().replace(R.id.fragment_placeholder1,
                        new AddPlantFragment()).commit();
            }
        });

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

    }
}

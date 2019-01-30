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

import java.util.ArrayList;
import java.util.List;

public class placeholderfragment1 extends Fragment {
    View v;

    private RecyclerView myrecyclerview;
    private List<Plant> plants;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.fragment_placeholder1,container,false);
        myrecyclerview = v.findViewById(R.id.plant_recyclerview);
        RecyclerViewAdapter recyclerAdapter = new RecyclerViewAdapter(getContext(),plants);
        myrecyclerview.setLayoutManager(new LinearLayoutManager(getActivity()));
        myrecyclerview.setAdapter(recyclerAdapter);
        return v;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        plants = new ArrayList<>();
        plants.add(new Plant("plant1",R.drawable.plant1));
        plants.add(new Plant("plant2",R.drawable.plant2));
        plants.add(new Plant("plant3",R.drawable.plant3));

    }
}

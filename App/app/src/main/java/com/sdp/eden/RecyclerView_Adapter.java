package com.sdp.eden;


import android.content.Context;
import android.graphics.Color;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.util.SparseBooleanArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

//Generic RecyclerView adapter format

public class RecyclerView_Adapter extends RecyclerView.Adapter<RecyclerView_Adapter.MyViewHolder> {

    Context mContext;
    ArrayList<Plant> mData;
    private SparseBooleanArray mSelectedItemsIds;


    public RecyclerView_Adapter(Context mContext, ArrayList<Plant> mData){
        this.mContext=mContext;
        this.mData=mData;
        mSelectedItemsIds = new SparseBooleanArray();
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v;
        v=LayoutInflater.from(mContext).inflate(R.layout.card_layout,viewGroup,false);
        MyViewHolder vHolder = new MyViewHolder(v);

        return vHolder;
    }


    @Override
    public void onBindViewHolder(@NonNull MyViewHolder myViewHolder, int position) {
        //display image and species and text
        myViewHolder.tv_name.setText(mData.get(position).getName());
        myViewHolder.tv_species.setText(mData.get(position).getSpecies());
        myViewHolder.img.setImageResource(mData.get(position).getPhoto());

        myViewHolder.itemView
                .setBackgroundColor(mSelectedItemsIds.get(position) ? 0x9934B5E4
                        : Color.TRANSPARENT);

    }

    public void toggleSelection(int position){
        selectView(position, !mSelectedItemsIds.get(position));
    }

    //Remove selected selections
    public void removeSelection() {
        mSelectedItemsIds = new SparseBooleanArray();
        notifyDataSetChanged();
    }

    //Put or delete selected position into SparseBooleanArray
    public void selectView(int position, boolean value) {
        if (value)
            mSelectedItemsIds.put(position, value);
        else
            mSelectedItemsIds.delete(position);

        notifyDataSetChanged();
    }

    //Get total selected count
    public int getSelectedCount() {
        return mSelectedItemsIds.size();
    }

    //Return all selected ids
    public SparseBooleanArray getSelectedIds() {
        return mSelectedItemsIds;
    }

    @Override
    public int getItemCount() {
        return mData.size();
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder{

        private TextView tv_name;
        private TextView tv_species;
        private ImageView img;

        public MyViewHolder(View v) {
            super(v);

            tv_name = (TextView) v.findViewById(R.id.card_plant_name);
            tv_species = (TextView) v.findViewById(R.id.card_plant_detail);
            img = (ImageView) v.findViewById(R.id.card_plant_image);
        }
    }
}

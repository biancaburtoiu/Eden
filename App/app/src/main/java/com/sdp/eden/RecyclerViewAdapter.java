package com.sdp.eden;


import android.content.Context;
import android.media.Image;
import android.provider.ContactsContract;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.List;

//Generic RecyclerView adapter format

public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewAdapter.MyViewHolder> {

    Context mContext;
    List<Plant> mData;


    public RecyclerViewAdapter(Context mContext, List<Plant> mData){
        this.mContext=mContext;
        this.mData=mData;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v;
        v=LayoutInflater.from(mContext).inflate(R.layout.item_plant,viewGroup,false);
        MyViewHolder vHolder = new MyViewHolder(v);

        return vHolder;
    }

    
    


    @Override
    public void onBindViewHolder(@NonNull MyViewHolder myViewHolder, int position) {
        //display image and text
        myViewHolder.tv_name.setText(mData.get(position).getName());
        myViewHolder.img.setImageResource(mData.get(position).getPhoto());

    }

    @Override
    public int getItemCount() {
        return mData.size();
    }

    public static class MyViewHolder extends RecyclerView.ViewHolder{

        private TextView tv_name;
        private ImageView img;

        public MyViewHolder(View v) {
            super(v);

            tv_name =  (TextView)  v.findViewById(R.id.name_plant);
            img = (ImageView) v.findViewById(R.id.img_plant);
        }
    }
    
    
}

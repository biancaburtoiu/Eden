package com.sdp.eden;


import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

//The adapter class associated with the image split class
public class ImageAdapter extends BaseAdapter {

    private Context mContext;
    private int selectedPosition =-1;
    private ArrayList<Bitmap> imageChunks;
    private int imageWidth, imageHeight;
    private boolean longClick=true;
    private Bitmap selectedImage;
    FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReference();

    //constructor
    public ImageAdapter(Context c, ArrayList<Bitmap> images){
        mContext = c;
        imageChunks = images;
        imageWidth = images.get(0).getWidth();
        imageHeight = images.get(0).getHeight();
    }

    @Override
    public int getCount() {
        return imageChunks.size();
    }

    public void setSelectedPosition(int position, boolean isLongClick){
        selectedPosition = position;
        longClick=isLongClick;
    }

    public void send_to_robot(){
        if(selectedImage!=null){
            StorageReference imageRef = storageRef.child("selected_image.jpg");
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            selectedImage.compress(Bitmap.CompressFormat.PNG, 100, baos);
            byte[] data = baos.toByteArray();

            UploadTask uploadTask = imageRef.putBytes(data);
            uploadTask.addOnFailureListener(new OnFailureListener() {
                @Override
                public void onFailure(@NonNull Exception exception) {
                    // Handle unsuccessful uploads
                }
            }).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {

                }
            });

        }
    }


    @Override
    public Object getItem(int position) {
        return imageChunks.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView image;
        if(convertView == null){
            image = new ImageView(mContext);
            image.setLayoutParams(new GridView.LayoutParams(imageWidth - 10 , imageHeight));
            image.setPadding(0, 0, 0, 0);
        }else{
            image = (ImageView) convertView;
        }

        if(longClick){
            if (position == selectedPosition) {
                image.setBackgroundColor(Color.BLACK);
                selectedImage=imageChunks.get(position);
            } else {
                image.setBackgroundColor(Color.TRANSPARENT);
                selectedImage=null;
            }
        }else{
            image.setBackgroundColor(Color.TRANSPARENT);
            selectedImage=null;
        }
        image.setImageBitmap(imageChunks.get(position));
        return image;
    }
}


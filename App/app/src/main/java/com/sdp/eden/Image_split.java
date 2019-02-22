package com.sdp.eden;


import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.GridView;


import java.util.ArrayList;

public class Image_split extends AppCompatActivity {

    private Bitmap bmp;
    private ArrayList<Bitmap> chunkedImages = new ArrayList<>(40);
    private ImageAdapter adapter;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.image_split);

        bmp = BitmapFactory.decodeResource(getResources(), R.drawable.overhead_image);
        splitImage(bmp);
        adapter = new ImageAdapter(this,chunkedImages);
        displaySplit(chunkedImages);

    }


    private void splitImage(Bitmap bitmap) {

        //For the number of rows and columns of the grid to be displayed
        int rows,cols;

        //For height and width of the small image chunks
        int chunkHeight,chunkWidth;


        //Getting the scaled bitmap of the source image
        Bitmap scaledBitmap = Bitmap.createScaledBitmap(bitmap, bitmap.getWidth(), bitmap.getHeight(), true);

        rows = cols = (int) Math.sqrt(36);
        chunkHeight = bitmap.getHeight()/rows;
        chunkWidth = bitmap.getWidth()/cols;

        //xCoord and yCoord are the pixel positions of the image chunks
        int yCoord = 0;
        for(int x=0; x<rows; x++){
            int xCoord = 0;
            for(int y=0; y<cols; y++){
                chunkedImages.add(Bitmap.createBitmap(scaledBitmap, xCoord, yCoord, chunkWidth, chunkHeight));
                xCoord += chunkWidth;
            }
            yCoord += chunkHeight;
        }
    }

    private void displaySplit(ArrayList<Bitmap> images){
        GridView grid = (GridView) findViewById(R.id.gridview);
        grid.setAdapter(adapter);
        grid.setNumColumns((int) Math.sqrt(chunkedImages.size()));
        grid.setOnItemClickListener((parent, v, position, id) -> {
            adapter.setSelectedPosition(position,false);
            adapter.notifyDataSetChanged();
        });

        grid.setOnItemLongClickListener((parent, v, position, id) -> {
            adapter.setSelectedPosition(position,true);
            adapter.notifyDataSetChanged();
            return true;
        });
    }

    public void send_to_robot(View view){
        adapter.send_to_robot();
        adapter.notifyDataSetChanged();
    }
}
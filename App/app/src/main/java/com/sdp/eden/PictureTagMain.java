package com.sdp.eden;


import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Picture;
import android.graphics.Point;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.RelativeLayout;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class PictureTagMain extends Fragment {

    public View img;

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.picturetag_main, container, false);
    }

    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        img = view.findViewById(R.id.overhead_image);
        Bitmap bmp = BitmapFactory.decodeResource(getResources(), R.drawable.overhead_image);
        Drawable d = new BitmapDrawable(getResources(), bmp);
        img.setBackground(d);
    }


    public static List<Float> getPointCoordinatesFromRoom(Activity activity){
        WindowManager wm = (WindowManager) activity.getSystemService(Activity.WINDOW_SERVICE);
        Point size = new Point();
        wm.getDefaultDisplay().getRealSize(size);

        DisplayMetrics displaymetrics = new DisplayMetrics();
        activity.getWindowManager().getDefaultDisplay().getMetrics(displaymetrics);
        int height = displaymetrics.heightPixels;
        int width = displaymetrics.widthPixels;

        float img_height= (float) (1920*0.387);
        float img_width=(float) (1080*0.85);

        float currentX=  PictureTagLayout.returnX();
        Log.d("testing1", "x  is "+currentX);

        float currentY=  PictureTagLayout.returnY();
        Log.d("testing1", "y  is "+currentY);

        float currentXratio=currentX/img_width;
        float currentYratio=currentY/img_height;
        Log.d("testing1","valueX " +  currentXratio);
        Log.d("testing1","valueY " +  currentYratio);

        return new ArrayList<Float>(Arrays.asList(currentXratio, currentYratio));
    }
}

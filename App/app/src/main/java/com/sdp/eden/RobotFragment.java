package com.sdp.eden;

import android.content.res.Resources;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;


import java.util.List;

public class RobotFragment extends Fragment{

    private static final String TAG = "RobotFragment";
    int pStatus = 0;
    private Handler handler = new Handler();
    TextView batPer;
    TextView tvWater;

    //private TextView batteryStatus;
    //private TextView waterStatus;
    private ProgressBar mProgressBat;
    private ProgressBar mProgressWater;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
       View v =  inflater.inflate(R.layout.fragment_robot,container,false);

//        falsebatteryStatus = v.findViewById(R.id.f_robot_battery_status_text);
//        waterStatus = v.findViewById(R.id.f_robot_water_status_text);
        mProgressBat =  v.findViewById(R.id.circularProgressbar);
        batPer = v.findViewById(R.id.batPer);
        mProgressWater =  v.findViewById(R.id.circularProgressbarWater);
        tvWater = v.findViewById(R.id.watPer);

       return v;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        Resources res = getResources();
        //Drawable drawable = res.getDrawable(R.drawable.circular);

        DbOps.instance.getBatteryStatus(new DbOps.OnGetBatteryStatusFinishedListener() {
            @Override
            public void onGetBatteryStatusFinished(List<BatteryStatus> statuses) {
                if (statuses==null) {
                    mProgressBat.setProgress(0);
                    mProgressWater.setProgress(0);
                    return;
                }

                BatteryStatus status = statuses.get(0);
                double voltage = Double.parseDouble(status.getVoltage());
                Log.d(TAG, "Current voltage: "+voltage);

                int waterAmount = 98; // temp
                tvWater.setText(waterAmount + "%");

                // 8 - 2.5 = 5.5
                int calculatedPercentage = (int) Math.round((voltage+2.5/5.5*100)*100.0/100.0);
                //batteryStatus.setText(calculatedPercentage + "%");
                mProgressBat.setProgress(calculatedPercentage);

                batPer.setText(calculatedPercentage + "%");
                mProgressWater.setProgress(waterAmount);
                mProgressBat.setMax(100);
                mProgressWater.setMax(100);



            }
        });
    }
}

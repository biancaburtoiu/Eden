package com.sdp.eden;

import android.graphics.Color;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

public class RobotFragment extends Fragment{

    private static final String TAG = "RobotFragment";

    private TextView batteryStatus;
    private TextView waterStatus;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
       View v =  inflater.inflate(R.layout.fragment_robot,container,false);

        batteryStatus = v.findViewById(R.id.f_robot_battery_status_text);
        waterStatus = v.findViewById(R.id.f_robot_water_status_text);

       return v;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        DbOps.instance.getBatteryStatus(new DbOps.OnGetBatteryStatusFinishedListener() {
            @Override
            public void onGetBatteryStatusFinished(List<BatteryStatus> statuses) {
                if (statuses==null) {
                    batteryStatus.setText("No voltage to display.");
                    return;
                }

                BatteryStatus status = statuses.get(0);
                Log.d(TAG, "Current voltage: "+status.getVoltage());

                // 8 - 2.5 = 5.5
                double calculatedPercentage = Math.round((status.getVoltage()+2.5/5.5*100)*100.0/100.0);
                batteryStatus.setText("Current battery is: "+ calculatedPercentage + " %");
            }
        });
    }
}

package com.sdp.eden;

import android.graphics.Color;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class RobotFragment extends Fragment{
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
}

package com.sdp.eden;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.TimePicker;

public class AddPlantSchedule extends Fragment {
    private static final String TAG = "AddPlantFragment";

    private TimePicker timePicker;

    private CheckBox checkBox_Monday;
    private CheckBox checkBox_Tuesday;
    private CheckBox checkBox_Wednesday;
    private CheckBox checkBox_Thursday;
    private CheckBox checkBox_Friday;
    private CheckBox checkBox_Saturday;
    private CheckBox checkBox_Sunday;



    public AddPlantSchedule() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_add_plant_schedule, container, false);

        timePicker = view.findViewById(R.id.timePicker);

        checkBox_Monday = view.findViewById(R.id.checkbox_Monday);
        checkBox_Tuesday = view.findViewById(R.id.checkbox_Tuesday);
        checkBox_Wednesday = view.findViewById(R.id.checkbox_Wednesday);
        checkBox_Thursday = view.findViewById(R.id.checkbox_Thursday);
        checkBox_Friday = view.findViewById(R.id.checkbox_Friday);
        checkBox_Saturday = view.findViewById(R.id.checkbox_Saturday);
        checkBox_Sunday = view.findViewById(R.id.checkbox_Sunday);


        return view;
    }


}

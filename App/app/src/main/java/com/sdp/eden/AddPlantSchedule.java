package com.sdp.eden;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;

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

    private EditText quantityInput;
    private TextView scheduleExplanation;

    private Button setScheduleButton;


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
        timePicker.setIs24HourView(true);

        final CheckBox checkBox_Monday = view.findViewById(R.id.checkbox_Monday);
        final CheckBox checkBox_Tuesday = view.findViewById(R.id.checkbox_Tuesday);
        final CheckBox checkBox_Wednesday = view.findViewById(R.id.checkbox_Wednesday);
        final CheckBox checkBox_Thursday = view.findViewById(R.id.checkbox_Thursday);
        final CheckBox checkBox_Friday = view.findViewById(R.id.checkbox_Friday);
        final CheckBox checkBox_Saturday = view.findViewById(R.id.checkbox_Saturday);
        final CheckBox checkBox_Sunday = view.findViewById(R.id.checkbox_Sunday);

        quantityInput = view.findViewById(R.id.quantityInput);

        // TODO: This should contain a written explanation of the schedule:
        // e.g. if the user ticked Monday and Friday and chose time 5pm
        // this string should update as the user checks/unchecks checkboxes
        // and it would say "Plant will be watered on Mondays and Fridays at 5pm"
        scheduleExplanation = view.findViewById(R.id.scheduleExplanation);

        return view;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

//        setScheduleButton = view.findViewById(R.id.setScheduleButton);
//        setScheduleButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                // Add schedule in Users/user/Schedules
//                // If you want to see the schedule of a specific plant query the Schedules where plantName=yourPlantName
//
//                // for checkbox in checkboxes, if checkbox is ticked then add Schedule entry
//                // with that day of the week and the time and the quantity
//                String currentPlant = "bob";
//                String time = timePicker.getHour()+":"+timePicker.getMinute();
//                int quantity = Integer.parseInt(quantityInput.getText().toString());
//
//                if (checkBox_Monday.isChecked()) {
//                    ScheduleEntry scheduleEntry = new ScheduleEntry(currentPlant,"Monday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                    DbOps.instance.addScheduleEntry(scheduleEntry, new DbOps.onAddScheduleEntryFinishedListener() {
//                        @Override
//                        public void onAddScheduleEntryFinished(boolean success) {
//                            Toast.makeText(getContext(), "Added!", Toast.LENGTH_SHORT);
//                        }
//                    });
//                }
//                if (checkBox_Tuesday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Tuesday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//                if (checkBox_Wednesday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Wednesday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//                if (checkBox_Thursday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Thursday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//                if (checkBox_Friday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Friday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//                if (checkBox_Saturday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Saturday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//                if (checkBox_Sunday.isChecked()) {
//                    ScheduleEntry newEntry = new ScheduleEntry(currentPlant,"Sunday", time, quantity);
//                    // TODO: Add newEntry to database in User/users/Schedules
//                }
//            }
//        });
    }
}

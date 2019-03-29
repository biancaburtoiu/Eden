package com.sdp.eden;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ScheduleFragment extends Fragment {

    private static final String TAG = "ScheduleFragment";
    private RecyclerView scheduleRV;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v =  inflater.inflate(R.layout.fragment_schedule,container,false);
        scheduleRV = v.findViewById(R.id.schedule);
        scheduleRV.setLayoutManager(new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false));
        scheduleRV.setAdapter(new ScheduleAdapter());
        return v;
    }
    
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        refresh();
    }

    public void refresh() {
        DbOps.instance.getAllScheduleEntries(new DbOps.OnGetAllSchedulesFinishedListener() {
            @Override
            public void onGetAllSchedulesFinished(List<ScheduleEntry> scheduleEntries) {
                ScheduleAdapter adapter = (ScheduleAdapter) scheduleRV.getAdapter();

                if (scheduleEntries==null) adapter.setSchedules(new ArrayList<>());
                else {
                    adapter.setSchedules(scheduleEntries);
                }
            }
        });
    }


    class ScheduleAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {
        private Map<Integer, List<ScheduleEntry>> schedules = new HashMap<>();


        @NonNull
        @Override
        public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int viewType) {
            if (viewType == 0) { //Title
                View v = LayoutInflater.from(viewGroup.getContext())
                        .inflate(R.layout.fragment_schedule_title, viewGroup, false);
                return new TitleViewHolder(v);
            } else { //Schedule
                View v = LayoutInflater.from(viewGroup.getContext())
                        .inflate(R.layout.fragment_schedule_entry, viewGroup, false);
                return new ScheduleViewHolder(v);
            }
        }

        @Override
        public void onBindViewHolder(@NonNull RecyclerView.ViewHolder viewHolder, int pos) {
            if (viewHolder instanceof TitleViewHolder) {
                TitleViewHolder vh = (TitleViewHolder) viewHolder;
                String title = (String) getItemFromPos(pos);

                //Do title layout
                vh.title.setText(title);
            } else {
                ScheduleViewHolder vh = (ScheduleViewHolder) viewHolder;
                ScheduleEntry schedule = (ScheduleEntry) getItemFromPos(pos);
                //Do schedule layout.

                vh.plant.setText(schedule.getPlantName());
                vh.quantity.setText(schedule.getQuantity()+"ml");
                vh.time.setText(schedule.getTime());
            }
        }

        @Override
        public int getItemCount() {
            return schedules.keySet()
                    .stream()
                    .reduce(schedules.size(), (acc, key) -> acc + schedules.get(key).size());
        }

        @Override
        public int getItemViewType(int pos) {
            Object item = getItemFromPos(pos);
            if (item instanceof String) return 0;
            if (item instanceof ScheduleEntry) return 1;
            return 0; //Will never happen.
        }

        @NonNull
        private Object getItemFromPos(int pos) {
            int currentPos = -1;
            for (int i = 0; i < 7; i++) {
                if (!schedules.containsKey(i)) continue;
                currentPos++;
                if (pos == currentPos) { //Title
                    switch (i) {
                        case 0: return "Monday";
                        case 1: return "Tuesday";
                        case 2: return "Wednesday";
                        case 3: return "Thursday";
                        case 4: return "Friday";
                        case 5: return "Saturday";
                        case 6: return "Sunday";
                    }
                }
                if (pos <= currentPos + schedules.get(i).size()) { //Schedule
                    int index = pos - currentPos - 1;
                    return schedules.get(i).get(index);
                } else {
                    currentPos += schedules.get(i).size();
                }
            }
            return "You shouldn't see this";
        }

        public void setSchedules(List<ScheduleEntry> schedules) {
            this.schedules = new HashMap<>();
            schedules.forEach(schedule -> {
                if (!this.schedules.containsKey(schedule.getDay())) {
                    this.schedules.put(schedule.getDay(), new ArrayList<>());
                }
                this.schedules.get(schedule.getDay()).add(schedule);
            });
            notifyDataSetChanged();
        }

        class TitleViewHolder extends RecyclerView.ViewHolder {
            View view;
            TextView title;
            public TitleViewHolder(@NonNull View itemView) {
                super(itemView);
                this.view = itemView;
                this.title = itemView.findViewById(R.id.title);
            }
        }

        class ScheduleViewHolder extends RecyclerView.ViewHolder {
            View view;
            TextView plant;
            TextView time;
            TextView quantity;
            public ScheduleViewHolder(@NonNull View itemView) {
                super(itemView);
                this.view = itemView;
                this.plant = itemView.findViewById(R.id.plant);
                this.time=itemView.findViewById(R.id.time);
                this.quantity=itemView.findViewById(R.id.quantity);
            }
        }
    }
}

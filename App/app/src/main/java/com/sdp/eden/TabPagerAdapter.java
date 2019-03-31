package com.sdp.eden;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

public class TabPagerAdapter extends FragmentPagerAdapter {

    public static Plant_Cards_Fragment plantCardsFragmentInstance;
    public static ScheduleFragment scheduleFragmentInstance;
    public static PastActivitiesFragment pastActivitiesFragmentInstance;

    TabPagerAdapter(FragmentManager fm){super(fm);}

    @Override
    public Fragment getItem(int i) {
        switch(i){
            default: return new Plant_Cards_Fragment().newInstance();
            case 1: scheduleFragmentInstance = new ScheduleFragment();
                return scheduleFragmentInstance;
            case 2: return new PastActivitiesFragment();
        }
    }

    @Override
    public int getCount() {
        return 3;
    }

    public CharSequence getPageTitle(int position) {
        //this determines the titles displayed on each tab
        if(position==0) {
            return "Plants";
        }else if (position==1){
            return "Schedule";
        } else {
            return "Complete";
        }
    }
}

package com.sdp.eden;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

public class TabPagerAdapter extends FragmentPagerAdapter {

    TabPagerAdapter(FragmentManager fm){super(fm);}

    @Override
    public Fragment getItem(int i) {
        switch(i){
            default: return new Plant_Cards_Fragment().newInstance();
            case 1: return new RobotFragment();
            case 2: return new ScheduleFragment();
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
            return "Robot";
        } else {
            return "Schedule";
        }
    }
}

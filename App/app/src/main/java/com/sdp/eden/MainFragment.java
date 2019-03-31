package com.sdp.eden;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class MainFragment extends Fragment {
    /*This class is for the plant list and the robot info - the ones with tabs.
    * To show a different fragment, you need to begin the transaction on
    * R.id.MainFrameLayout. This way the tabs won't be there for the other fragment.
    * Enable the home button so that you can pop from the back stack and get this
    * fragment back after.
    * */




    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_main,container,false);

        //set up view pager and tab layout, using adapter
        PagerAdapter pagerAdapter = new TabPagerAdapter(getChildFragmentManager());
        ViewPager viewPager = v.findViewById(R.id.MainViewPager);
        viewPager.setAdapter(pagerAdapter);
        TabLayout tabLayout = v.findViewById(R.id.MainTabLayout);
        tabLayout.setupWithViewPager(viewPager);

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                if (tab.getPosition() == 1) {
                    TabPagerAdapter.scheduleFragmentInstance.refreshSchedules();
                }
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });


        return v;
    }

}

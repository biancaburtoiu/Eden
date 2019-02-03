package com.sdp.eden;

import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.TableLayout;
import android.widget.Toolbar;


public class Eden_main extends AppCompatActivity {
    private android.support.v7.widget.Toolbar toolbar;
    public Fragment fr;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.eden_main);

        //set up toolbar at top, and setting listener for home button (back arrow)
        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setHomeButtonEnabled(false);
        toolbar.setNavigationOnClickListener(v -> onBackPressed());

        //the frame layout in eden_main will show the MainFragment layout inside it
        getSupportFragmentManager().beginTransaction().replace(R.id.MainFrameLayout,
                new MainFragment()).commit();


    }

    @Override
    public void onBackPressed() {
        if (getSupportFragmentManager().getBackStackEntryCount() > 0) {
            getSupportFragmentManager().popBackStack();

        }
    }

}

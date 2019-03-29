package com.sdp.eden;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TableLayout;
import android.widget.TextView;
import android.widget.Toolbar;

import com.google.firebase.auth.FirebaseAuth;

import java.util.List;
import java.util.Objects;


public class Eden_main extends AppCompatActivity {
    private android.support.v7.widget.Toolbar toolbar;
    public Fragment fr;
    private static final String TAG = "Eden_mainActivity";


    TextView batPer;
    TextView batText;
    private ProgressBar mProgressBat;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.eden_main);

        //set up toolbar at top, and setting listener for home button (back arrow)
        toolbar = findViewById(R.id.toolbar);
        ImageView battery = toolbar.findViewById(R.id.battery);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setDisplayShowHomeEnabled(false);
        toolbar.setNavigationOnClickListener(v -> onBackPressed());

        //the frame layout in eden_main will show the MainFragment layout inside it
        getSupportFragmentManager().beginTransaction().replace(R.id.MainFrameLayout,
                new MainFragment()).commit();

        DbOps.instance.getBatteryStatus(new DbOps.OnGetBatteryStatusFinishedListener() {
            @Override
            public void onGetBatteryStatusFinished(List<BatteryStatus> statuses) {
                Log.d(TAG, "Returned from database call");
                if (statuses == null) {
                    Log.d(TAG, "Statuses is null");
                    battery.setImageDrawable(getResources().getDrawable(R.drawable.ic_battery_full));
                    return;
                }
                else {
                    Log.d(TAG, "Statuses is NOT null!");

                    BatteryStatus status = statuses.get(0);
                    double voltage = Double.parseDouble(status.getVoltage());
                    Log.d(TAG, "Voltage is: "+voltage);

                    // 8 - 2.5 = 5.5
                    int calculatedPercentage = (int) Math.round((voltage - 2.5) * 100.0 / 5.5);
                    Log.d(TAG, "percentage is: "+calculatedPercentage);
                    if (calculatedPercentage > 90){
                        battery.setImageDrawable(getResources().getDrawable(R.drawable.ic_battery_full));
                    }else if (calculatedPercentage > 50){
                        battery.setImageDrawable(getResources().getDrawable(R.drawable.ic_battery_high));
                    }else if (calculatedPercentage >= 25){
                        battery.setImageDrawable(getResources().getDrawable(R.drawable.ic_battery_mid));
                    }else{
                        battery.setImageDrawable(getResources().getDrawable(R.drawable.ic_battery_low));
                    }
                }
            }
        });


    }

    public void changeFrag(Fragment newFrag) {
        getSupportFragmentManager().beginTransaction().replace(R.id.MainFrameLayout,
                newFrag).addToBackStack(null).commit();
        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

    }

    @Override
    public void onBackPressed() {
        if (getSupportFragmentManager().getBackStackEntryCount()>0) {
            getSupportActionBar().setDisplayShowHomeEnabled(false);
            getSupportActionBar().setDisplayHomeAsUpEnabled(false);
            getSupportFragmentManager().popBackStack();
            }
        }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.toolbar_3dot, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_signout) {
            FirebaseAuth.getInstance().signOut();
            startActivity(new Intent(this, Signin.class));
            finish();
            return true;
        }
        else if (id == R.id.action_batteryStatus) {
            Log.d(TAG, "Entered action_batteryStatus");

            final AlertDialog.Builder builder = new AlertDialog.Builder(Eden_main.this);
            final View view = getLayoutInflater().inflate(R.layout.fragment_robot, null);
            builder.setView(view);

            mProgressBat = view.findViewById(R.id.circularProgressbar);
            batPer = view.findViewById(R.id.batPer);
            batText = view.findViewById(R.id.batteryText);

            DbOps.instance.getBatteryStatus(new DbOps.OnGetBatteryStatusFinishedListener() {
                @Override
                public void onGetBatteryStatusFinished(List<BatteryStatus> statuses) {
                    Log.d(TAG, "Returned from database call");
                    if (statuses == null) {
                        Log.d(TAG, "Statuses is null");
                        mProgressBat.setProgress(0);
                        return;
                    }
                    else {
                        Log.d(TAG, "Statuses is NOT null!");

                        BatteryStatus status = statuses.get(0);
                        double voltage = Double.parseDouble(status.getVoltage());
                        Log.d(TAG, "Voltage is: "+voltage);

                        // 8 - 2.5 = 5.5
                        int calculatedPercentage = (int) Math.round((voltage - 2.5) * 100.0 / 5.5);
                        mProgressBat.setProgress(calculatedPercentage);
                        batPer.setText(calculatedPercentage + "%");
                        batText.setText("Eden currently has "+calculatedPercentage+"% battery.");
                        mProgressBat.setMax(100);

                        AlertDialog editdialog = builder.create();
                        editdialog.show();
                    }
                }
            });

            return true;
        }

        return super.onOptionsItemSelected(item);
    }


}

package com.sdp.eden;

import android.content.Context;
import android.support.v4.app.Fragment;
import android.support.v7.view.ActionMode;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;


import java.util.ArrayList;


public class Toolbar_ActionMode_Callback implements ActionMode.Callback {

    private Context context;
    private RecyclerView_Adapter recyclerView_adapter;
    private ArrayList<Plant> plants;
    private boolean isOtherViewFragment;
    private PlantListFragment frag;
    private int fragid;


    public Toolbar_ActionMode_Callback(Context context, RecyclerView_Adapter recyclerView_adapter,ArrayList<Plant> plants, PlantListFragment frag) {
        this.context = context;
        this.recyclerView_adapter = recyclerView_adapter;
        this.plants = plants;
        this.frag = frag;
    }

    @Override
    public boolean onCreateActionMode(ActionMode mode, Menu menu) {
        mode.getMenuInflater().inflate(R.menu.menu_main, menu);//Inflate the menu_main over action mode
        return true;
    }

    @Override
    public boolean onPrepareActionMode(ActionMode mode, Menu menu) {

        //Sometimes the meu will not be visible so for that we need to set their visibility manually in this method
        //So here show action menu_main according to SDK Levels
        menu.findItem(R.id.action_delete).setShowAsAction(MenuItem.SHOW_AS_ACTION_ALWAYS);

        return true;
    }

    @Override
    public boolean onActionItemClicked(ActionMode mode, MenuItem item) {
        switch (item.getItemId()) {
            case R.id.action_delete:


                //Get recycler view fragment

                if (frag != null) {
                    //If recycler fragment not null

                    frag.deleteRows();//delete selected rows
                    Log.d("testing", "value");



                    break;
                }else {
                    Log.d("testing", "value1");

                }

        }
        return false;
    }


    @Override
    public void onDestroyActionMode(ActionMode mode) {

        //When action mode destroyed remove selected selections and set action mode to null
        //First check current fragment action mode
        recyclerView_adapter.removeSelection();  // remove selection

        if (frag != null) {
            frag.setNullToActionMode();//Set action mode null
        }
    }
}
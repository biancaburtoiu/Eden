package com.sdp.eden;


import android.content.Intent;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class Starting_page extends AppCompatActivity {

    private FirebaseAuth mAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        mAuth = FirebaseAuth.getInstance();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.startingpage);
        getWindow().setStatusBarColor(ContextCompat.getColor(this, R.color.colorPrimary));
    }

    @Override
    public void onStart() {
        super.onStart();
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser currentUser = mAuth.getCurrentUser();
        updateUI(currentUser);
    }

    //Click the button and then into the startingpage page.
    public void createNewAccount(View view){
        Intent intent = new Intent(this, Create_account.class);
        startActivity(intent);
    }

    //Click the button and then into the sign in page.
    public void signIn(View view){
        Intent intent2 = new Intent(this, Signin.class);
        startActivity(intent2);
    }

    //Update the UI, if with valid user, then enter the gameMainActivity.
    private void updateUI(FirebaseUser user) {
        //hideProgressDialog();
        if (user != null) {
            Intent intent = new Intent(this, Eden_main.class);
            startActivity(intent);

        }
    }
}

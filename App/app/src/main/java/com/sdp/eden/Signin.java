package com.sdp.eden;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Patterns;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class Signin extends AppCompatActivity {
    private EditText mEmailField;
    private EditText mPasswordField;
    private FirebaseAuth mAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //Initializing variables
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_page);
        mAuth = FirebaseAuth.getInstance();
        mEmailField = findViewById(R.id.loginemailfield);
        mPasswordField = findViewById(R.id.loginpasswordfield);

        findViewById(R.id.sign_in_button).setOnClickListener(new View.OnClickListener(){
            public  void onClick(View v){
                signIn(mEmailField.getText().toString(), mPasswordField.getText().toString());
            }
        });
    }
       //On button register clicked, start Create_account
    public void register(View view){
        Intent intent=new Intent(this, Create_account.class);
        startActivity(intent);
    }



    private void signIn(String email, String password){
        //validate the input format
        if(!validateForm()){
            return;
        }

        mAuth.signInWithEmailAndPassword(email,password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()){
                            FirebaseUser user = mAuth.getCurrentUser();
                            updateUI(user);
                        } else{
                            Toast.makeText(Signin.this , "Authentication failed.",
                                    Toast.LENGTH_SHORT).show();
                            updateUI(null);
                        }

                    }
                });


    }

    private boolean validateForm() {
        boolean valid = true;
        //give error notice when format is incorrect
        String email = mEmailField.getText().toString();
        if (TextUtils.isEmpty(email)) {
            mEmailField.setError("Required.");
            valid = false;
        } else if(!Patterns.EMAIL_ADDRESS.matcher(email).matches()){
            mEmailField.setError("Email form is required");
        }
        else {
            mEmailField.setError(null);
        }

        String password = mPasswordField.getText().toString();
        if (TextUtils.isEmpty(password)) {
            mPasswordField.setError("Required.");
            valid = false;
        } else if(password.length()<6){
            mEmailField.setError("password requires at least 6 characters");
        }
        else {
            mPasswordField.setError(null);
        }

        return valid;
    }

    private void updateUI(FirebaseUser user) {
        //When user is not null proceed to main activity
        if (user != null) {
            Toast.makeText(Signin.this, "Login succeeded.",
                    Toast.LENGTH_SHORT).show();

            Intent intent = new Intent(this, Eden_main.class);
            startActivity(intent);

        }
    }

    @Override
    protected void onStart (){
        super.onStart();
        //Automatically takes user to main activity when they are already logged in, until they chose to log out
        FirebaseUser user = mAuth.getCurrentUser();
        updateUI(user);
    }





}

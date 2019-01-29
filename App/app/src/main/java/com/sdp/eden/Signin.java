package com.sdp.eden;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
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

    public void register(View view){
        Intent intent=new Intent(this, Create_account.class);
        startActivity(intent);
    }



    private void signIn(String email, String password){
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

        String email = mEmailField.getText().toString();
        if (TextUtils.isEmpty(email)) {
            mEmailField.setError("Required.");
            valid = false;
        } else {
            mEmailField.setError(null);
        }

        String password = mPasswordField.getText().toString();
        if (TextUtils.isEmpty(password)) {
            mPasswordField.setError("Required.");
            valid = false;
        } else {
            mPasswordField.setError(null);
        }

        return valid;
    }

    private void updateUI(FirebaseUser user) {
        if (user != null) {
            Toast.makeText(Signin.this, "Login succeeded.",
                    Toast.LENGTH_SHORT).show();

            Intent intent = new Intent(this, Eden_main.class);
            startActivity(intent);

        } else {
            Toast.makeText(Signin.this, "Login failed.",
                    Toast.LENGTH_SHORT).show();

        }
    }





}

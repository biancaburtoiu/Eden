package com.sdp.eden;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;



public class Create_account extends AppCompatActivity {

    private static final String TAG = "CreateNewAccount";
    private EditText mEmailField;
    private EditText mNameField;
    private EditText mPasswordField;
    private EditText mPasswordConfirmField;
    private FirebaseAuth mAuth;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.registration);
        mEmailField = findViewById(R.id.emailfield);
        mNameField = findViewById(R.id.namefield);
        mPasswordField = findViewById(R.id.passwordfield);
        mPasswordConfirmField = findViewById(R.id.confirmpasswordfield);

        mAuth = FirebaseAuth.getInstance();


        // When the button clicked, if the passwords are the same, register an account,
        // else toast that the passwords are different.
        findViewById(R.id.register).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if(mPasswordField.getText().toString().equals(mPasswordConfirmField.getText().toString())){
                    createAccount(mEmailField.getText().toString(), mPasswordField.getText().toString());
                }else{
                    Toast.makeText(Create_account.this, "Passwords are different.",
                            Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    //Validate the form of the filled email.
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

    private void createAccount (String email, String password ){
        final String userId = mNameField.getText().toString();
        final String eMail = mEmailField.getText().toString();

        //If the filled email address is in invalid form, then stop startingpage and show toast.
        if (!validateForm()) {
            Toast.makeText(Create_account.this, "Invalid email form.",
                    Toast.LENGTH_SHORT).show();
            return;
        }

        // [START create_user_with_email]
        mAuth.createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign up success, update UI with the signed-in user's information
                            FirebaseUser currentUser = mAuth.getCurrentUser();
                            updateUI(currentUser);

                        } else {
                            // If sign up fails,  a message to the user.
                            Log.w(TAG, "createUserWithEmail:failure", task.getException());
                            updateUI(null);
                        }
                    }
                });
    }

    //When cancel button clicked, back to the first page.


    //Update the UI, if with valid user, then enter the gameMainActivity.
    private void updateUI(FirebaseUser user) {
        if (user != null) {
            Toast.makeText(Create_account.this, "Starting_page succeeded.",
                    Toast.LENGTH_SHORT).show();

            Intent intent = new Intent(this, Eden_main.class);
            startActivity(intent);

        } else {
            Toast.makeText(Create_account.this, "Starting_page failed.",
                    Toast.LENGTH_SHORT).show();

        }
    }


}
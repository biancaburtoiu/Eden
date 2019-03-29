package com.sdp.eden;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;

public class PictureTagView extends RelativeLayout implements OnEditorActionListener{

    private Context context;
    private TextView tvPictureTagLabel;
    private EditText etPictureTagLabel;
    private View loTag;
    public enum Status{Normal,Edit}
    public enum Direction{Left,Right}
    private Direction direction = Direction.Left;
    private InputMethodManager imm;
    private static final int ViewWidth = 80;
    private static final int ViewHeight = 50;

    public PictureTagView(Context context,Direction direction) {
        super(context);
        this.context = context;
        this.direction = direction;
        initViews();
        init();
        initEvents();
    }


    protected void initViews(){
        LayoutInflater.from(context).inflate(R.layout.picturetagview, this,true);
        tvPictureTagLabel = (TextView) findViewById(R.id.tvPictureTagLabel);
        etPictureTagLabel = (EditText) findViewById(R.id.etPictureTagLabel);
        loTag = findViewById(R.id.loTag);
    }

    protected void init(){
        imm = (InputMethodManager)context.getSystemService(Context.INPUT_METHOD_SERVICE);
        directionChange();
    }


    protected void initEvents(){
        //etPictureTagLabel.setOnEditorActionListener(this);
    }

    public void setStatus(Status status){
/*        switch(status){
            case Normal:
                tvPictureTagLabel.setVisibility(View.VISIBLE);
                etPictureTagLabel.clearFocus();
                tvPictureTagLabel.setText(etPictureTagLabel.getText());
                etPictureTagLabel.setVisibility(View.GONE);
                //hide keyboard
                imm.hideSoftInputFromWindow(etPictureTagLabel.getWindowToken() , 0);
                break;
            case Edit:
                tvPictureTagLabel.setVisibility(View.GONE);
                etPictureTagLabel.setVisibility(View.VISIBLE);
                etPictureTagLabel.requestFocus();
                //showing keyboard
                imm.toggleSoftInput(0, InputMethodManager.SHOW_FORCED);
                break;
        }*/
    }
    @Override
    public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
        setStatus(Status.Normal);
        return true;
    }
    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        super.onLayout(changed, l, t, r, b);
        View parent = (View) getParent();
        //int halfParentW = (int) (parent.getWidth()*0.5);
        if(l<=40){
            direction = Direction.Left;
        }
        else{
            direction = Direction.Right;
        }
        directionChange();
    }
    private void directionChange(){
        switch(direction){
            case Left:
                loTag.setBackgroundResource(R.drawable.circle_);
                break;
            case Right:
                loTag.setBackgroundResource(R.drawable.circle_);
                break;
        }
    }
    public static int getViewWidth(){
        return ViewWidth;
    }
    public static int getViewHeight(){
        return ViewHeight;
    }
}
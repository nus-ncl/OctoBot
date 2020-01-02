package com.webbrowsingbot.app;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;

public class InputInfo{
    private String url; // Url that contains the input fields
    private ArrayList<HashMap<String, Object>> data;
    private String submit;

    public String getUrl(){
        return this.url;
    }

    public ArrayList<HashMap<String, Object>> getData(){
        return this.data;
    }

    public String getSubmit(){
        return this.submit;
    }

    public static InputInfo getInputInfo(String url, ArrayList<InputInfo> inputinfo){
        if(inputinfo == null){
            return null;
        }
        for(InputInfo i: inputinfo){
            if(i.url.equalsIgnoreCase(url)){
                return i;
            }
        }
        return null;
    }

    public static ArrayList<InputInfo> parse(FileReader file){
        //Declare gson object
        Gson gson = new Gson();

        //Set the type and get the information out of the json file
        Type type = new TypeToken<ArrayList<InputInfo>>(){}.getType();
        return gson.fromJson(file, type);
    }

    public static ArrayList<InputInfo> parse(String jsonContent){
        //Declare gson object
        Gson gson = new Gson();

        //Set the type and get the information out of the json file
        Type type = new TypeToken<ArrayList<InputInfo>>(){}.getType();
        return gson.fromJson(jsonContent, type);
    }
}
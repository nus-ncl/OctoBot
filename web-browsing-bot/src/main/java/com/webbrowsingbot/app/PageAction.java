package com.webbrowsingbot.app;

import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class PageAction{
    private String url;
    private ArrayList<HashMap<String, Object>> actions;

    public String getUrl() {
        return this.url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public ArrayList<HashMap<String,Object>> getActions()

    {
		return this.actions;
	}

    public void setActions(ArrayList<HashMap<String,Object>> actions)
    {
		this.actions = actions;
	}

    public static ArrayList<PageAction> parse(FileReader f){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<PageAction>>(){}.getType();
        return gson.fromJson(f, type);
    }

    public static PageAction getPageAction(String url, ArrayList<PageAction> pageActions){
        if(pageActions == null){
            return null;
        }
        for(PageAction p: pageActions){
            if(url.matches(p.url)){
                return p;
            }
        }
        return null;
    }
}
package com.webbrowsingbot.app;

import java.io.FileReader;
import java.util.HashMap;
import com.google.gson.Gson;

public class LoginInformation{
    private String loginUrl;
    private String logoutUrl;
    private HashMap<String, String> credentials;

    public String getLoginUrl() {
        return this.loginUrl;
    }

    public void setLoginUrl(String loginUrl) {
        this.loginUrl = loginUrl;
    }

    public String getLogoutUrl() {
        return this.logoutUrl;
    }

    public void setLogoutUrl(String logoutUrl) {
        this.logoutUrl = logoutUrl;
    }

    public HashMap<String, String> getCredentials()
    {
		return this.credentials;
	}

    public void setCredentials(HashMap<String, String> credentials)
    {
		this.credentials = credentials;
	}

    public LoginInformation(String loginUrl, String logoutUrl, HashMap<String, String> credentials){
        this.loginUrl = loginUrl;
        this.logoutUrl = logoutUrl;
        this.credentials = credentials;
    }

    public static LoginInformation parse(FileReader file){
        Gson gson = new Gson();
        return gson.fromJson(file, LoginInformation.class);
    }


}
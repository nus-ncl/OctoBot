package com.webbrowsingbot.app;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;

import org.openqa.selenium.WebDriver;

public class LoginLogoutAction {
    private String username; //Username is defined as the first action that has a value attribute inside.
    private PageAction loginAction;
    private PageAction logoutAction;

    public LoginLogoutAction(String username, PageAction loginAction, PageAction logoutAction){
        this.username = username;
        this.loginAction = loginAction;
        this.logoutAction = logoutAction;
    }

    @Override
    public String toString(){
        String s = "{";
        s += String.format("username: %s, ", this.username);
        s += "}";
        return s;
    }

    public PageAction getLoginAction() {
        return this.loginAction;
    }

    public void setLoginAction(PageAction loginAction) {
        this.loginAction = loginAction;
    }

    public PageAction getLogoutAction() {
        return this.logoutAction;
    }

    public void setLogoutAction(PageAction logoutAction) {
        this.logoutAction = logoutAction;
    }
    
    @SuppressWarnings("unchecked")
    //Find the usernames, username is defined as the first action with a value attribute
    private static ArrayList<String> getUsernames(ArrayList<HashMap<String, Object>> loginActions){
        for(HashMap<String, Object> action: loginActions){
            if(action.get("value") != null){
                Object objVal = action.get("value");
                ArrayList<String> output = null;
                if(objVal.getClass() == String.class){
                    output = new ArrayList<String>();
                    output.add((String)objVal);
                }else{
                    output = (ArrayList<String>)objVal;
                }
                return output;
            }
        }
        return null;
    }

    //Converts json file into java objects
    public static LoginLogoutAction parse(FileReader f){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<LoginLogoutAction>>(){}.getType();
        //Obtains information from json
        ArrayList<LoginLogoutAction> loginLogoutActionsArrayList = gson.fromJson(f, type);
        
        //Creates new new arraylist to store new information after rearranging data from json
        ArrayList<LoginLogoutAction> reformattedLoginLogoutActionsArrayList = new ArrayList<LoginLogoutAction>();
        
        //Does the reformating here
        for(LoginLogoutAction loginLogoutAction: loginLogoutActionsArrayList){
            //Get the login actions from the json file
            ArrayList<HashMap<String, Object>> loginActions = loginLogoutAction.loginAction.getActions();
            
            //Find the usernames, username is defined as the first action with a value attribute
            ArrayList<String> usernames = getUsernames(loginActions);
            for(String username: usernames){
                LoginLogoutAction lla = new LoginLogoutAction(username, loginLogoutAction.loginAction, loginLogoutAction.logoutAction);
                reformattedLoginLogoutActionsArrayList.add(lla);
            }
        }
        
        return loginLogoutActionsArrayList.get(0);
    }

    public void performLogin(WebDriver driver, String loginUrl){
        // Figure out whether to load the webpage
        if(loginUrl != null){
            try{
                driver.get(loginUrl);
            }catch(Exception e){
                System.err.printf("Error getting %s: %s\n", loginUrl, e);
                return;
            }
        }

        //Do the login steps
        loginAction.doActions(driver);
    }

    public void performLogout(WebDriver driver, String logoutUrl){
        // Figure out whether to load the webpage
        if(logoutUrl != null){
            try{
                driver.get(logoutUrl);
            }catch(Exception e){
                System.err.printf("Error getting %s: %s\n", logoutUrl, e);
                return;
            }
        }

        //Do the logout steps
        logoutAction.doActions(driver);
    }

}
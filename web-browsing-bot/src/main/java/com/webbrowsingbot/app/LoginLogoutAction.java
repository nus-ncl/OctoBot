package com.webbrowsingbot.app;

import com.webbrowsingbot.app.PageAction;
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
        s += String.format("loginAction: %s, ", this.loginAction.getActions().get(0).get("value"));
        s += String.format("loginAction: %s, ", this.loginAction.getActions().get(1).get("value"));
        s += "}";
        return s;
    }

    public String getUsername() {
        return this.username;
    }

    public void setUsername(String username) {
        this.username = username;
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
    

    public static ArrayList<LoginLogoutAction> getAllPossibleLoginActions(String url, ArrayList<LoginLogoutAction> loginLogoutActions){
        ArrayList<LoginLogoutAction> output = new ArrayList<LoginLogoutAction>();

        if(loginLogoutActions != null){
            for(LoginLogoutAction l: loginLogoutActions){
                String path = Utils.getPath(url);
                
                String loginUrl = l.getLoginAction().getUrl();
                String loginPath = l.getLoginAction().getPath();
                
                boolean urlMatch = (loginUrl == null) ? false : url.matches(loginUrl);
                boolean pathMatch = (loginPath == null) ? false : path.matches(loginPath);
                if(urlMatch || pathMatch){
                    output.add(l);
                }
            }
        }

        return output;
    }

    public static LoginLogoutAction getUserLogoutAction(String url, String username, ArrayList<LoginLogoutAction> loginLogoutActions){
        LoginLogoutAction loginLogoutAction = null;
        for(LoginLogoutAction l: loginLogoutActions){
            if(l.getUsername().equals(username)){
                loginLogoutAction = l;
            }
        }

        if(loginLogoutAction == null){
            return null;
        }

        String logoutPath = loginLogoutAction.getLogoutAction().getPath();
        String logoutUrl = loginLogoutAction.getLogoutAction().getUrl();
        String path = Utils.getPath(url);
        boolean pathMatch = (logoutPath == null) ? true : path.matches(logoutPath);
        boolean urlMatch = (logoutUrl == null) ? true : url.matches(logoutUrl);

        if(pathMatch && urlMatch){
            return loginLogoutAction;
        }else{
            return null;
        }
    }

    @SuppressWarnings("unchecked")
    //Find the usernames, username is defined as the first action with a value attribute
    private static ArrayList<LoginLogoutAction> reformat(LoginLogoutAction loginLogoutActions){
        //Get the login actions
        ArrayList<HashMap<String, Object>> loginActions = loginLogoutActions.getLoginAction().getActions();
        
        //Obtain all the usernames in an arraylist
        ArrayList<String> usernameArrayList = null;
        for(HashMap<String, Object> action: loginActions){
            if(action.get("value") != null){
                Object objVal = action.get("value");
                if(objVal.getClass() == String.class){
                    usernameArrayList = new ArrayList<String>();
                    usernameArrayList.add((String)objVal);
                }else{
                    usernameArrayList = (ArrayList<String>)objVal;
                }
                break;
            }
        }
        
        // Do some preliminary checks
        if(usernameArrayList == null){
            return null;
        }

        //Loops every username to create a unique loginlogoutaction for all user
        ArrayList<LoginLogoutAction> output = new ArrayList<LoginLogoutAction>();
        for(int i = 0; i < usernameArrayList.size(); i++){
            //Reformat login_action
            String path = loginLogoutActions.getLoginAction().getPath();
            String url = loginLogoutActions.getLoginAction().getUrl();
            ArrayList<HashMap<String, Object>> actions = new ArrayList<HashMap<String, Object>>();
            PageAction newLoginActions = new PageAction(url, path, actions);

            for(HashMap<String, Object> action: loginActions){
                //Ensure that the instances are different instances
                action = new HashMap<String, Object>(action);

                if(action.get("value") != null){
                    Object objVal = action.get("value");
                    if(objVal.getClass() == String.class){
                        newLoginActions.getActions().add(action);
                    }else{
                        //Obtain the i'th index from the list
                        ArrayList<String> values = (ArrayList<String>)objVal;
                        action.replace("value", values.get(i%values.size()));
                        newLoginActions.getActions().add(action);
                    }
                }else{
                    newLoginActions.getActions().add(action);
                }
            }
            output.add(new LoginLogoutAction(usernameArrayList.get(i), newLoginActions, loginLogoutActions.getLogoutAction()));
        }
        return output;
    }

    //Converts json file into java objects
    public static ArrayList<LoginLogoutAction> parse(FileReader f){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<LoginLogoutAction>>(){}.getType();
        //Obtains information from json
        ArrayList<LoginLogoutAction> loginLogoutActionsArrayList = null;
        loginLogoutActionsArrayList = gson.fromJson(f, type);

        //Creates new new arraylist to store new information after rearranging data from json
        ArrayList<LoginLogoutAction> reformattedLoginLogoutActionsArrayList = new ArrayList<LoginLogoutAction>();
        
        //Does the reformating here
        for(LoginLogoutAction loginLogoutAction: loginLogoutActionsArrayList){  
            //Find the usernames, username is defined as the first action with a value attribute
            ArrayList<LoginLogoutAction> l = reformat(loginLogoutAction);
            reformattedLoginLogoutActionsArrayList.addAll(l);
        }

        return reformattedLoginLogoutActionsArrayList;
    }

    public String performLogin(WebDriver driver, String loginUrl){
        // Figure out whether to load the webpage
        if(loginUrl != null){
            try{
                driver.get(loginUrl);
            }catch(Exception e){
                System.err.printf("Error getting %s: %s\n", loginUrl, e);
                return null;
            }
        }

        //Do the login steps
        System.out.println("\033[1;36mPerforming login\033[0m");
        loginAction.doActions(driver);

        return this.username;
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
        System.out.println("\033[1;36mPerforming logout\033[0m");
        logoutAction.doActions(driver);

        return;
    }

}
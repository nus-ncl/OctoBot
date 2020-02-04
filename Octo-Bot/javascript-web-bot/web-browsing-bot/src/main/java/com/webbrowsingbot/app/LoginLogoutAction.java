package com.webbrowsingbot.app;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.openqa.selenium.WebDriver;

public class LoginLogoutAction {
    private PageAction loginAction;
    private PageAction logoutAction;

    public LoginLogoutAction(PageAction loginAction, PageAction logoutAction){
        this.loginAction = loginAction;
        this.logoutAction = logoutAction;
    }

    @Override
    public String toString(){
        String s = "{";
        s += String.format("loginAction: %s, ", this.loginAction.getActions().get(0).get("value"));
        s += String.format("loginAction: %s, ", this.loginAction.getActions().get(1).get("value"));
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
    

    public static String getRandomUsername(String url, HashMap<String, LoginLogoutAction> loginLogoutActions){
        if(loginLogoutActions == null){
            return null;
        }

        ArrayList<String> usernames = new ArrayList<String>();
        for(String username: loginLogoutActions.keySet()){            
            LoginLogoutAction l = loginLogoutActions.get(username);
            
            boolean urlMatch = Utils.matchUrl(url, l.getLoginAction());

            if(urlMatch){
                usernames.add(username);
            }
        }

        if(usernames.size() <= 0){
            return null;
        }

        //Generate a random one
        int randint = (int)(Math.random()*usernames.size());
        return usernames.get(randint);
    }

    public static LoginLogoutAction getUserLogoutAction(String url, String username, HashMap<String, LoginLogoutAction> loginLogoutActions){
        if(loginLogoutActions == null){
            return null;
        }
        
        LoginLogoutAction loginLogoutAction = loginLogoutActions.get(username);

        if(loginLogoutAction == null){
            return null;
        }

        boolean urlMatch = Utils.matchUrl(url, loginLogoutAction.getLogoutAction());

        if(urlMatch){
            return loginLogoutAction;
        }else{
            return null;
        }
    }

    @SuppressWarnings("unchecked")
    //Find the usernames, username is defined as the first action with a value attribute
    private static HashMap<String, LoginLogoutAction> reformat(LoginLogoutAction loginLogoutActions){
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
        
        // Do some checks
        if(usernameArrayList == null){
            return null;
        }

        //Loops every username to create a unique hashmap entry for all user
        HashMap<String, LoginLogoutAction> output = new HashMap<String, LoginLogoutAction>();
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
            output.put(usernameArrayList.get(i), new LoginLogoutAction(newLoginActions, loginLogoutActions.getLogoutAction()));
        }
        return output;
    }

    //Converts json file into java objects
    public static HashMap<String, LoginLogoutAction> parse(String loginJson){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<LoginLogoutAction>>(){}.getType();
        
        //Obtains information from json
        ArrayList<LoginLogoutAction> loginLogoutActionsArrayList = null;
        loginLogoutActionsArrayList = gson.fromJson(loginJson, type);

        //Creates new new arraylist to store new information after rearranging data from json
        HashMap<String, LoginLogoutAction> reformattedLoginLogoutActions = new HashMap<String, LoginLogoutAction>();
        
        //Does the reformating here
        for(LoginLogoutAction loginLogoutAction: loginLogoutActionsArrayList){  
            //Find the usernames, username is defined as the first action with a value attribute
            HashMap<String, LoginLogoutAction> l = reformat(loginLogoutAction);
            reformattedLoginLogoutActions.putAll(l);
        }

        return reformattedLoginLogoutActions;
    }

    public boolean performLogin(WebDriver driver, String loginUrl){
        // Figure out whether to load the webpage
        if(loginUrl != null){
            try{
                driver.get(loginUrl);
            }catch(Exception e){
                System.err.printf("\033[91mError getting %s: %s\033[0m\n", loginUrl, e);
                return false;
            }
        }

        //Do the login steps
        System.out.println("\033[1;36mPerforming login\033[0m");
        loginAction.doActions(driver);
        return true;
    }

    public void performLogout(WebDriver driver, String logoutUrl){
        // Figure out whether to load the webpage
        if(logoutUrl != null){
            try{
                driver.get(logoutUrl);
            }catch(Exception e){
                System.err.printf("\033[91mError getting %s: %s\033[0m\n", logoutUrl, e);
                return;
            }
        }

        //Do the logout steps
        System.out.println("\033[1;36mPerforming logout\033[0m");
        logoutAction.doActions(driver);

        return;
    }

}
package com.webbrowsingbot.app;

import com.google.gson.Gson;
import java.io.FileReader;

import org.openqa.selenium.WebDriver;

public class LoginLogoutAction {
    private PageAction loginAction;
    private PageAction logoutAction;

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

    public static LoginLogoutAction parse(FileReader f){
        Gson gson = new Gson();

        return gson.fromJson(f, LoginLogoutAction.class);
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
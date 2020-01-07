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

    public void performLogin(WebDriver driver, boolean loadUrl){
        // Figure out whether to load the webpage
        String loginUrl = this.loginAction.getUrl();
        if(loadUrl){
            try{
                driver.get(loginUrl);
            }catch(Exception e){
                return;
            }
        }

        //Do the login steps
        loginAction.doActions(driver);
    }

    public void performLogout(WebDriver driver, boolean loadUrl){
        // Figure out whether to load the webpage
        String logoutUrl = this.logoutAction.getUrl();
        if(loadUrl){
            driver.get(logoutUrl);
        }

        //Do the logout steps
        logoutAction.doActions(driver);
    }

}
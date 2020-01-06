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
            driver.get(loginUrl);
        }

        //Print some message
        System.out.println("\033[1;92mPerforming login... \033[0m");

        //Do the login steps
        loginAction.doActions(driver);
    }

    public void performLogout(WebDriver driver, boolean loadUrl){
        // Figure out whether to load the webpage
        String logoutUrl = this.logoutAction.getUrl();
        if(loadUrl){
            driver.get(logoutUrl);
        }

        //Print some message
        System.out.printf("\033[1;92mPerforming logout...\033[0m %s\n", logoutUrl);

        //Do the logout steps
        logoutAction.doActions(driver);
    }

}
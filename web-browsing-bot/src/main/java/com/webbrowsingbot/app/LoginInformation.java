package com.webbrowsingbot.app;

import java.io.FileReader;
import com.google.gson.Gson;

public class LoginInformation {
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

    public static LoginInformation parse(FileReader f){
        Gson gson = new Gson();

        return gson.fromJson(f, LoginInformation.class);
    }

}
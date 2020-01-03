package com.webbrowsingbot.app;

import java.lang.Math;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;

//This bot will randomly browse webpages
public class BrowserBot{
    private int minTime, maxTime;
    private WebDriver driver;
    private LoginInformation loginInfo;
    private boolean isLoggedIn;
    private ArrayList<String> urlsRequireLogin;
    private ArrayList<String> urls;
    private ArrayList<PageAction> pageActions;

    //Constructor #1
    public BrowserBot(WebDriver driver){
        this(driver, null, null, null, null);
    }

    //Constructor #2
    public BrowserBot(WebDriver driver, ArrayList<String> urls, ArrayList<String> urlsRequireLogin, LoginInformation loginInfo, ArrayList<PageAction> pageActions){
        this.driver = driver;
        this.urls = urls;
        this.urlsRequireLogin = urlsRequireLogin;
        this.pageActions = pageActions;
        this.loginInfo = loginInfo;
        this.minTime = 2000;
        this.maxTime = 5000;
    }

    /* This function will take in a */
    public void browse(){
        if(this.urls != null){
            this.browseWithCrawl();
        }else{
            this.browseNoCrawl(null);
        }
    }

    public void browseWithCrawl(){
        for(;;){
            //Choose a random page to visit
            String url;
            if(isLoggedIn){
                int randint = (int)(Math.random()*urlsRequireLogin.size());
                url = urlsRequireLogin.get(randint);
            }else{
                int randint = (int)(Math.random()*urls.size());
                url = urls.get(randint);
            }

            //Enter the URL
            try{
                this.driver.get(url);
            }catch(Exception e){
                //JUST MOVE ON
                System.err.printf("Error getting webpage: %s\n", e);
            }

            //Logout things.
            if(loginInfo != null){
                if(url.contains(loginInfo.getLogoutAction().getUrl())){
                    isLoggedIn = false;
                }
            }

            if(driver.getCurrentUrl().equals(url)){
                System.out.println(url);
            }else{
                System.out.printf("%s -> %s: %b\n", url, driver.getCurrentUrl(), isLoggedIn);
                url = driver.getCurrentUrl();
            }

            //Try this logic to do login first
            if(loginInfo != null){
                if(url.contains(loginInfo.getLoginAction().getUrl())){
                    if(!isLoggedIn){
                        Utils.performLogin(driver, null, loginInfo.getLoginAction());
                    }
                    isLoggedIn = true;
                }
            }
            
            //Do actions
            PageAction pageAction = PageAction.getPageAction(url, pageActions);
            if(pageAction != null){
                Utils.doActions(this.driver, pageAction);
            }
            
            //Sleep a bit
            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.println("Somehow failed to sleep(?)");
            }
        }
    }

    public void browseNoCrawl(String url){
        //Go to that page
        this.driver.get(url);

        //Find links in page
        

        //Choose a link to go into

        //
    }
}
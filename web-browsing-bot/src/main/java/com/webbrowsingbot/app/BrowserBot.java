package com.webbrowsingbot.app;

import java.lang.Math;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;

//This bot will randomly browser webpages
public class BrowserBot{
    private int minTime, maxTime;
    private WebDriver driver;
    private LoginInformation loginInfo;
    private boolean isLoggedIn;
    private ArrayList<String> urlsRequireLogin;
    private ArrayList<String> urls;
    private ArrayList<InputInfo> inputValues;

    //Constructor #1
    public BrowserBot(WebDriver driver){
        this(driver, new ArrayList<String>(), new ArrayList<String>(), new ArrayList<InputInfo>());
    }

    //Constructor #2
    public BrowserBot(WebDriver driver, ArrayList<String> urls, ArrayList<String> urlsRequireLogin, ArrayList<InputInfo> inputValues){
        this.driver = driver;
        this.urls = urls;
        this.urlsRequireLogin = urlsRequireLogin;
        this.inputValues = inputValues;
        this.minTime = 2000;
        this.maxTime = 5000;
    }

    /* This function will take in a */
    public void browse(){
        if(this.urlsRequireLogin != null){
            this.browseWithCrawl();
        }else{
            this.browseNoCrawl(null);
        }
    }

    public void browseWithCrawl(){
        for(;;){
            //Choose a random page to visit
            int randint = (int)(Math.random()*urls.size());
            String url = urls.get(randint);

            //Enter the URL
            this.driver.get(url);

            //Try this logic to do login first
            if(url.equals(loginInfo.getLoginUrl())){
                Utils.performLogin(driver, loginInfo.getCredentials());
            }
            
            //Please fill it up if values are provided
            Utils.fillInputs(this.driver, url, inputValues);

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
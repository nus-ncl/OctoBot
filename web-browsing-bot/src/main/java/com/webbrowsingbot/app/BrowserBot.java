package com.webbrowsingbot.app;

import java.lang.Math;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;

//This bot will randomly browse webpages
public class BrowserBot{
    private WebDriver driver;
    private String domain;
    private String loggedInUser;
    private HashMap<String, LoginLogoutAction> loginLogoutActions;
    private ArrayList<PageAction> pageActions;
    private int minTime, maxTime;

    //For browse no crawl
    HashMap<String, ArrayList<String>> urls;

    //For browse with crawl
    private ArrayList<String> blacklistUrls;

    //Constructor #1
    public BrowserBot(WebDriver driver){
        this(driver, null, null, null, null);
    }

    //Constructor #2
    public BrowserBot(WebDriver driver, String domain, HashMap<String, ArrayList<String>> urls, HashMap<String, LoginLogoutAction> loginLogoutActions, ArrayList<PageAction> pageActions){
        this.driver = driver;
        this.domain = domain;
        this.pageActions = pageActions;
        this.loginLogoutActions = loginLogoutActions;
        this.minTime = 2000;
        this.maxTime = 5000;

        //For browse with crawl
        this.urls = urls;
    
        //For browse no crawl
        this.blacklistUrls = new ArrayList<String>();
    }

    /* This function will take in a */
    public void browse(String url, int duration){
        if(this.urls != null){
            this.browseWithCrawl(duration);
        }else{
            this.browseNoCrawl(url, duration);
        }
        System.out.printf("\033[1;36mTerminating because %d seconds are over %n\033[0m", duration);
    }

    public boolean processPage(String url){
        //Enter the URL
        try{
            this.driver.get(url);
        }catch(org.openqa.selenium.TimeoutException e){
            System.err.printf("\033[91mTimeout loading %s: %s\033[0m\n", url, e);
            return false;
        }catch(org.openqa.selenium.WebDriverException e){
            System.err.printf("\033[91mError getting webpage %s: %s\033[0m\n", url, e);
            return false;
        }

        //Logout things.
        LoginLogoutAction logoutAction = LoginLogoutAction.getUserLogoutAction(url, loggedInUser, loginLogoutActions);
        if(logoutAction != null){
            logoutAction.performLogout(driver, null);
            loggedInUser = null;
        }

        if(driver.getCurrentUrl().equals(url)){
            System.out.printf("GET: %s\n", url);
        }else{
            System.out.printf("GET: %s -> %s\n", url, driver.getCurrentUrl());
            url = driver.getCurrentUrl();
        }

        //Try this logic to do login first
        String username = LoginLogoutAction.getRandomUsername(url, loginLogoutActions);
        if(username != null){
            LoginLogoutAction loginAction = loginLogoutActions.get(username);
            loginAction.performLogin(driver, null);
            loggedInUser = username;
        }
        
        //Do actions
        PageAction pageAction = PageAction.getPageAction(url, pageActions);
        if(pageAction != null){
            pageAction.doActions(this.driver);
        }

        return true;
    }

    public void browseWithCrawl(int duration){
        LocalDateTime endTime = Utils.calculateEndTime(duration);
        while(Utils.haveTime(endTime)){
            //Choose a random page to visit
            ArrayList<String> arrOfUrls = urls.get(loggedInUser);
            int randint = (int)(Math.random()*arrOfUrls.size());
            String url = arrOfUrls.get(randint);
            
            //Process the page
            this.processPage(url);
            
            //Sleep a bit
            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.println("Somehow failed to sleep(?)");
            }
        }
    }

    public void browseNoCrawl(String url, int duration){
        // Declare variables (All the Urls)
        String prevUrl = "", nextUrl = "", baseUrl = url;

        // Time things
        LocalDateTime endTime = Utils.calculateEndTime(duration);
        while(Utils.haveTime(endTime)){
            //Important boolean variable
            boolean goBack = false;

            //Validate the URL first
            boolean inBlacklist = blacklistUrls.contains(url);
            if(inBlacklist){
                // Go back to previous page
                goBack = true;
            }

            //Process the page
            boolean successful = this.processPage(url);
            if(!successful){
                blacklistUrls.add(url);
                // Go back to previous page
                goBack = true;
            }

            //Find links in page
            ArrayList<String> linksInPage = Utils.getLinks(this.driver, this.domain, this.blacklistUrls);

            // If there are no links on that page.
            if(linksInPage == null || linksInPage.size() <= 0) {
                goBack = true;
            }
            else {
                //Choose a link to go into
                int randint = (int) (linksInPage.size() * Math.random());
                nextUrl = linksInPage.get(randint);
            }

            //Configure the URL to go back if goBack is true
            if(goBack) {
                // Randomness will dictate whether the browser bot will go in a loop. The more times it loops, the higher chance it has to breaking out of the loop.
                int randint = (int)(Math.random()*2);
                if(randint <= 0){
                    nextUrl = prevUrl;
                }else{
                    nextUrl = baseUrl;
                }
            }

            /* Preps the loop for the next iteration */
            //Save prev page
            prevUrl = url;
            //Loads next page
            url = nextUrl;

            //Sleep a while
            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.printf("Failed to sleep: %s\n", e);
            }
        }
    }
}
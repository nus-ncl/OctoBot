package com.webbrowsingbot.app;

import java.lang.Math;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;

//This bot will randomly browse webpages
public class BrowserBot{
    private WebDriver driver;
    private String domain;
    private String loggedInUser;
    private ArrayList<LoginLogoutAction> loginLogoutActions;
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
    public BrowserBot(WebDriver driver, String domain, HashMap<String, ArrayList<String>> urls, ArrayList<LoginLogoutAction> loginLogoutActions, ArrayList<PageAction> pageActions){
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
    public void browse(String url){
        if(this.urls != null){
            this.browseWithCrawl();
        }else{
            this.browseNoCrawl(url);
        }
    }

    public boolean processPage(String url){
        //Enter the URL
        try{
            this.driver.get(url);
        }catch(org.openqa.selenium.TimeoutException e){
            System.err.printf("Timeout loading %s: %s\n", url, e);
            return false;
        }catch(org.openqa.selenium.WebDriverException e){
            System.err.printf("Error getting webpage %s: %s\n", url, e);
            return false;
        }

        //Logout things.
        if(loggedInUser != null){
            ArrayList<LoginLogoutAction> allLogoutActionss = LoginLogoutAction.getAllPossibleLogoutActions(url, loginLogoutActions);
            if(allLogoutActionss.size() > 0){
                int randint = (int)(Math.random()*allLogoutActionss.size());
                LoginLogoutAction logoutAction = allLogoutActionss.get(randint);
                logoutAction.performLogout(driver, null);
                loggedInUser = null;
            }
        }

        if(driver.getCurrentUrl().equals(url)){
            System.out.printf("GET: %s\n", url);
        }else{
            System.out.printf("GET: %s -> %s\n", url, driver.getCurrentUrl());
            url = driver.getCurrentUrl();
        }

        //Try this logic to do login first
        if(loggedInUser == null){
            ArrayList<LoginLogoutAction> allLoginActions = LoginLogoutAction.getAllPossibleLoginActions(url, loginLogoutActions);
            if(allLoginActions.size() > 0){
                int randint = (int)(Math.random()*allLoginActions.size());
                LoginLogoutAction loginAction = allLoginActions.get(randint);
                loggedInUser = loginAction.performLogin(driver, null);
            }
        }
        
        //Do actions
        PageAction pageAction = PageAction.getPageAction(url, pageActions);
        if(pageAction != null){
            pageAction.doActions(this.driver);
        }

        return true;
    }

    public void browseWithCrawl(){
        for(;;){
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

    public void browseNoCrawl(String url){
        String prevPage = url;
        for(;;){
            //Validate the URL first
            boolean inBlacklist = blacklistUrls.contains(url);
            if(inBlacklist){
                // Go back to previous page
                url = prevPage;
                continue;
            }

            //Process the page
            boolean successful = this.processPage(url);
            if(!successful){
                blacklistUrls.add(url);
                // Go back to previous page
                url = prevPage;
                continue;
            }

            //Find links in page
            ArrayList<String> linksInPage = Utils.getLinks(this.driver, this.domain, this.blacklistUrls);

            // If there are no links on that page.
            if(linksInPage == null || linksInPage.size() <= 0){
                url = prevPage; // GOes to the previous page
                continue;
            }

            //Save prev page
            prevPage = url;

            //Choose a link to go into
            int randint = (int)(linksInPage.size()*Math.random());
            url = linksInPage.get(randint);

            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.printf("Failed to sleep: %s\n", e);
            }
        }
    }
}
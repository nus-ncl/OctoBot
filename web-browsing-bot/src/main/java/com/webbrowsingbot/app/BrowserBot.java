package com.webbrowsingbot.app;

import java.lang.Math;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.WebDriver;

//This bot will randomly browse webpages
public class BrowserBot{
    private WebDriver driver;
    private boolean isLoggedIn;
    private LoginLogoutAction loginLogoutAction;
    private ArrayList<PageAction> pageActions;
    private int minTime, maxTime;

    //For browse no crawl
    private ArrayList<String> urls;
    private ArrayList<String> urlsRequireLogin;

    //For browse with crawl
    private ArrayList<String> blacklistUrls;

    //Constructor #1
    public BrowserBot(WebDriver driver){
        this(driver, null, null, null, null);
    }

    //Constructor #2
    public BrowserBot(WebDriver driver, ArrayList<String> urls, ArrayList<String> urlsRequireLogin, LoginLogoutAction loginLogoutAction, ArrayList<PageAction> pageActions){
        this.driver = driver;
        this.pageActions = pageActions;
        this.loginLogoutAction = loginLogoutAction;
        this.minTime = 2000;
        this.maxTime = 5000;

        //For browse with crawl
        this.urls = urls;
        this.urlsRequireLogin = urlsRequireLogin;
    
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
            System.err.printf("Error getting webpage %s: %s\n", url, e);
            return false;
        }

        //Logout things.
        if(loginLogoutAction != null){
            if(url.contains(loginLogoutAction.getLogoutAction().getUrl())){
                if(isLoggedIn){
                    loginLogoutAction.performLogout(driver, false);
                }
                isLoggedIn = false;
            }
        }

        if(driver.getCurrentUrl().equals(url)){
            //System.out.printf("GET: %s\n", url);
        }else{
            //System.out.printf("GET: %s -> %s\n", url, driver.getCurrentUrl());
            url = driver.getCurrentUrl();
        }

        //Try this logic to do login first
        if(loginLogoutAction != null){
            if(url.contains(loginLogoutAction.getLoginAction().getUrl())){
                if(!isLoggedIn){
                    loginLogoutAction.performLogin(driver, false);
                }
                isLoggedIn = true;
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
            String url;
            if(isLoggedIn){
                int randint = (int)(Math.random()*urlsRequireLogin.size());
                url = urlsRequireLogin.get(randint);
            }else{
                int randint = (int)(Math.random()*urls.size());
                url = urls.get(randint);
            }

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
        String baseUrl = url;
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
            ArrayList<String> linksInPage = Utils.getLinks(driver, baseUrl, this.blacklistUrls);

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
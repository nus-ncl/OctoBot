package com.webbrowsingbot.app;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.*;

//This bot will randomly browse webpages
public class BrowserBot {
    private WebDriver driver;
    private String domain;
    private String loggedInUser;
    private HashMap<String, LoginLogoutAction> loginLogoutActions;
    private ArrayList<PageAction> pageActions;
    private int minTime, maxTime;

    // For browse no crawl
    private boolean sameDomain;
    private HashMap<String, ArrayList<String>> urls;

    // For browse with crawl
    private ArrayList<String> blacklistUrls;

    // Constructor #1
    public BrowserBot(WebDriver driver) {
        this(driver, null, null, null, null, false);
    }

    // Constructor #2
    public BrowserBot(WebDriver driver, String domain, HashMap<String, ArrayList<String>> urls,
            HashMap<String, LoginLogoutAction> loginLogoutActions, ArrayList<PageAction> pageActions,
            boolean sameDomain) {
        this.driver = driver;
        this.domain = domain;
        this.pageActions = pageActions;
        this.loginLogoutActions = loginLogoutActions;
        this.minTime = 2000;
        this.maxTime = 5000;

        // For browse with crawl
        this.urls = urls;
        this.sameDomain = sameDomain;

        // For browse no crawl
        this.blacklistUrls = new ArrayList<String>();
    }

    /* This function will take in a */
    public void browse(String url, int duration) {
        if (this.urls != null) {
            this.browseWithCrawl(duration);
        } else {
            this.browseNoCrawl(url, duration);
        }

        System.out.printf("\033[1;36mTerminating because %d seconds are over %n\033[0m", duration);
    }

    public boolean processPage(String url){
        // Enter the URL
        try {
            this.driver.get(url);
            
            //This is just so that the redirect will work
            TimeUnit.SECONDS.sleep(2); //They say that this is not good practice but there is no solid webdriverrwait expected condition
        } catch (InterruptedException e) {
            System.err.println("Something wrong with sleeping");
        } catch (TimeoutException e) {
            System.err.printf("\033[91mTimeout loading %s: %s\033[0m\n", url, e);
            // return false;
        } catch (WebDriverException e) {
            System.err.printf("\033[91mError getting webpage %s: %s\033[0m\n", url, e);
            return false;
        }

        //Logout things.
        LoginLogoutAction logoutAction = LoginLogoutAction.getUserLogoutAction(url, loggedInUser, loginLogoutActions);
        if(logoutAction != null){
            logoutAction.performLogout(driver, null);
            loggedInUser = null;
        }

        try{
            if(driver.getCurrentUrl().equals(url)){
                System.out.printf("GET: %s\n", url);
            }else{
                System.out.printf("GET: %s -> %s\n", url, driver.getCurrentUrl());
                url = driver.getCurrentUrl();
            }
        }catch(UnhandledAlertException e){
            System.err.printf("\033[91mUnhandled alert, trying to close it\033[0m%n");
        }
        // Check if it is the login URL
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
            //Sleep a bit
            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.println("Somehow failed to sleep");
            }

            //Choose a random page to visit
            ArrayList<String> arrOfUrls = urls.get(loggedInUser);
            int randint = (int)(Math.random()*arrOfUrls.size());
            String url = arrOfUrls.get(randint);
            
            //Process the page
            this.processPage(url);
        }
    }

    public void browseNoCrawl(String url, int duration){
        // Declare variables (All the Urls)
        String prevUrl = "", nextUrl = "", baseUrl = url;

        // Time things
        LocalDateTime endTime = Utils.calculateEndTime(duration);
        while(Utils.haveTime(endTime)){
            // Sleep a while
            int sleepDuration = (int)((maxTime-minTime)*Math.random())+minTime;
            try{
                TimeUnit.MILLISECONDS.sleep(sleepDuration);
            }catch(Exception e){
                System.err.printf("Failed to sleep: %s\n", e);
            }

            // Important boolean variable
            boolean goBack = false;

            // Validate the URL first
            boolean inBlacklist = blacklistUrls.contains(url);
            if(inBlacklist){
                // Go back to previous page
                goBack = true;
            }

            // Process the page
            boolean successful = this.processPage(url);
            if(!successful){
                blacklistUrls.add(url);
                // Go back to previous page
                goBack = true;
            }

            //Find links in page
            ArrayList<Link> linksInPage = Utils.getLinks(this.driver, this.domain, this.blacklistUrls, sameDomain);

            // If there are no links on that page.
            if(linksInPage == null || linksInPage.size() <= 0) {
                goBack = true;
            }else if(linksInPage.size() == 1 && url.equals(linksInPage.get(0).getHref())){ //If there is only one choice\
                //If there is only one link, and the one link is the current URL, go back
                goBack = true;
            }else {
                Link chosenLink = Link.chooseRandLink(linksInPage);
                nextUrl = chosenLink.getHref();
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
        }
    }
}
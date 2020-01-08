package com.webbrowsingbot.app;

import java.util.ArrayList;
import java.util.List;
//Selenium imports
import org.openqa.selenium.By;
//import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Crawler{
    private ArrayList<String> visitedUrls;
    private WebDriver driver;
    private String domain;
    private int maxDepth;
    private LoginLogoutAction loginLogoutAction;

    public Crawler(WebDriver driver){
        this.driver = driver;
        this.visitedUrls = new ArrayList<String>();
    }

    public void setLoginLogoutAction(LoginLogoutAction loginLogoutAction){
        this.loginLogoutAction = loginLogoutAction;
    }

    public void setDomain(String domain){
        this.domain = domain;
    }

    public boolean performLogin(){
        if(loginLogoutAction == null){
            return false;
        }
        loginLogoutAction.performLogin(driver, true);
        return true;
    }

    public void startCrawl(String url){
        startCrawl(url, -1);
    }
    
    public ArrayList<String> startCrawl(String url, int maxDepth){
        this.maxDepth = maxDepth;

        //Actual crawling function
        this.visit(url, 0, true);

        /* End of crawl stuff */
        //Save the visited URLs
        ArrayList<String> arr = new ArrayList<String>(visitedUrls);
        visitedUrls.clear();        
        return arr;
    }

    public void visit(String url, int curDepth, boolean toLoadUrl){
        //If link is visited, then dont bother entering it
        if(this.visitedUrls.contains(url) || (curDepth > this.maxDepth && this.maxDepth != -1)){
            return;
        }

        //Load the URL
        if(toLoadUrl){
            try{
                if(loginLogoutAction == null || !url.contains(loginLogoutAction.getLogoutAction().getUrl()))
                    this.driver.get(url);
            }catch(org.openqa.selenium.TimeoutException e){
                System.err.printf("Webpage timeout %s: %s\n", url, e);
                //this.visitedUrls.add(url); //Saves the URL into the arraylist
                return;
            }catch(org.openqa.selenium.WebDriverException e){
                System.err.printf("Error getting page %s: %s\n", url, e);
                //this.visitedUrls.add(url); //Saves the URL into the arraylist
                return;
            }
        }
        this.visitedUrls.add(url); //Saves the URL into the arraylist

        //Obtains all links in the current link
        ArrayList<String> webLinks = null;
        //If next depth is not going to be get accessed, then dont bother getting links for the current URL
        if(curDepth+1 <= this.maxDepth || this.maxDepth == -1){
            webLinks = Utils.getLinks(this.driver, this.domain, new ArrayList<String>());
        }

        //Debug information
        System.out.println("\033[1;94m## Current URL ##\033[0m");
        System.out.println("URL\t\t:\t"+ url);
        System.out.println("Current Depth\t:\t"+ curDepth);
        System.out.println("Links\t\t:\t" + webLinks.size());

        if(webLinks == null || webLinks.size() <= 0){
            return;
        }

        //Access all the links
        for(String link: webLinks){
            this.visit(link, curDepth+1, true);
        }
    }
}

class CrawlerUtils{
    public static List<WebElement> getAllButtons(WebDriver driver){
        return driver.findElements(By.cssSelector("button"));
    }

    public static List<WebElement> findAllInputs(WebDriver driver){
        return driver.findElements(By.cssSelector("input, textarea"));
    }
}
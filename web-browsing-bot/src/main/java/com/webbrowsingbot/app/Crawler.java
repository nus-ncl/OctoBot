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
    private String baseUrl;
    private int maxDepth;
    private LoginInformation loginInfo;

    public Crawler(WebDriver driver){
        this.driver = driver;
        this.visitedUrls = new ArrayList<String>();
    }

    public void setLoginInformation(LoginInformation loginInfo){
        this.loginInfo = loginInfo;
    }

    public void setBaseUrl(String baseUrl){
        this.baseUrl = baseUrl;
    }

    public boolean performLogin(){
        if(loginInfo == null){
            return false;
        }
        Utils.performLogin(driver, loginInfo.getLoginAction().getUrl(), loginInfo.getLoginAction());
        return true;
    }

    public void startCrawl(){
        startCrawl(-1);
    }
    
    public ArrayList<String> startCrawl(int maxDepth){
        this.maxDepth = maxDepth;

        //Actual crawling function
        this.visit(this.baseUrl, 0, true);

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
                if(loginInfo == null || !url.contains(loginInfo.getLogoutAction().getUrl()))
                    this.driver.get(url);
            }catch(Exception e){
                System.out.println(e);
            }
        }
        this.visitedUrls.add(url); //Saves the URL into the arraylist

        //Obtains all links in the current link
        ArrayList<String> webLinks = null;
        //If next depth is not going to be get accessed, then dont bother getting links for the current URL
        if(curDepth+1 <= this.maxDepth || this.maxDepth == -1){
            webLinks = Utils.getLinks(this.driver, this.baseUrl, new ArrayList<String>());
        }

        //Debug information
        System.out.println("\n\033[1;94m## Current URL ##\033[0m");
        System.out.println("URL\t\t:\t"+ url);
        System.out.println("Current Depth\t:\t"+ curDepth);
        if(webLinks == null || webLinks.size() <= 0){
            return;
        }
        System.out.println("Links\t\t: ");
        for(int i = 0; i < webLinks.size(); i++){
            System.out.println( i+1 + ") " + webLinks.get(i));
        }

        //Click all the buttons
        // List<WebElement> buttons = CrawlerUtils.getAllButtons(this.driver);
        // System.out.println("Buttons");
        // for(WebElement b: buttons){
        //     if(!b.getText().equals("")){
        //         System.out.println(b.getText());
        //     }
        // }

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
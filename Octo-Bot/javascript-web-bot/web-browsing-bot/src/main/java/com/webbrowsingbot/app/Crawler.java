package com.webbrowsingbot.app;

//Java imports
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

//Selenium imports
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Crawler{
    private ArrayList<String> visitedUrls;
    private WebDriver driver;
    private String domain;
    private int maxDepth;
    private boolean sameDomain;
    private LoginLogoutAction loginLogoutAction;
    private HashMap<String, LoginLogoutAction> loginLogoutActions;

    public Crawler(WebDriver driver, boolean sameDomain){
        this.driver = driver;
        this.sameDomain = sameDomain;
        this.visitedUrls = new ArrayList<String>();
    }

    public void setLoginLogoutActions(HashMap<String, LoginLogoutAction> loginLogoutActions){
        if(loginLogoutActions == null){
            return;
        }
        //Makes a new instance because this object will modify the variable by removing items
        this.loginLogoutActions = new HashMap<String, LoginLogoutAction>(loginLogoutActions);
    }

    public void setDomain(String domain){
        this.domain = domain;
    }

    public String performLogin(URI uri){
        if(this.loginLogoutActions == null || this.loginLogoutActions.size() <= 0){
            return null;
        }

        if(this.loginLogoutAction != null){
            this.performLogout(uri);
        }

        //Gets the next loginLogoutAction
        String username = (String)this.loginLogoutActions.keySet().toArray()[0];
        this.loginLogoutAction = this.loginLogoutActions.get(username);
        this.loginLogoutActions.remove(username);

        String loginUrl = this.loginLogoutAction.getLoginAction().getUrl();
        if(loginUrl == null){
            loginUrl = Utils.craftUrl(uri, this.loginLogoutAction.getLoginAction().getPath());
        }

        this.loginLogoutAction.performLogin(this.driver, loginUrl);
        return username;
    }

    public boolean performLogout(URI uri){
        if(loginLogoutAction == null){
            return false;
        }

        String logoutUrl = loginLogoutAction.getLogoutAction().getUrl();
        if(logoutUrl == null){
            logoutUrl = Utils.craftUrl(uri, loginLogoutAction.getLogoutAction().getPath());
        }

        loginLogoutAction.performLogout(driver, logoutUrl);
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
                // Get logout action, loginLogoutAction can be null to represent not logged in user
                PageAction logoutAction = (loginLogoutAction == null) ? null : loginLogoutAction.getLogoutAction();
                
                //Check whether the url is a logout url, if the logoutAction is null, no error will be thrown but isLogoutUrl will be false;
                boolean isLogoutUrl = Utils.matchUrl(url, logoutAction);
                
                if(!isLogoutUrl) {//If it is not the logout URL, then load the page
                    this.driver.get(url);
                }
            }catch(org.openqa.selenium.TimeoutException e){
                System.err.printf("\033[91mWebpage timeout %s: %s\033[0m\n", url, e);
                //this.visitedUrls.add(url); //Saves the URL into the arraylist
                return;
            }catch(org.openqa.selenium.WebDriverException e){
                System.err.printf("\033[91mError getting page %s: %s\033[0m\n", url, e);
                //this.visitedUrls.add(url); //Saves the URL into the arraylist
                return;
            }
        }
        this.visitedUrls.add(url); //Saves the URL into the arraylist

        //Obtains all links in the current link
        ArrayList<Link> webLinks = null;
        //If next depth is not going to be get accessed, then dont bother getting links for the current URL
        if(curDepth+1 <= this.maxDepth || this.maxDepth == -1){
            webLinks = Utils.getLinks(this.driver, this.domain, new ArrayList<String>(), sameDomain);
        }

        //Debug information
        System.out.println("\033[1;94m## Current URL ##\033[0m");
        System.out.println("URL\t\t:\t"+ url);
        System.out.println("Current Depth\t:\t"+ curDepth);
        System.out.println("Links\t\t:\t" + ((webLinks == null) ? "null" : webLinks.size()));

        if(webLinks == null || webLinks.size() <= 0){
            return;
        }

        //Access all the links
        for(Link link: webLinks){
            this.visit(link.getHref(), curDepth+1, true);
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
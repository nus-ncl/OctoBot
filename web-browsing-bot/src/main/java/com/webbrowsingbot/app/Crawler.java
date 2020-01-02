package com.webbrowsingbot.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.lang.Math;
import java.util.concurrent.TimeUnit;
//Selenium imports
import org.openqa.selenium.By;
//import org.openqa.selenium.Keys;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;


public class Crawler{
    private ArrayList<String> allVisitedUrls;
    private ArrayList<String> visitedUrls;
    private WebDriver driver;
    private JavascriptExecutor js;
    private String baseUrl;
    private String loginUrl;
    private int maxDepth;
    private ArrayList<InputInfo> inputValues = null;
    private HashMap<String, String> loginCredentials;

    public Crawler(WebDriver driver){
        this.driver = driver;
        this.visitedUrls = new ArrayList<String>();
        this.allVisitedUrls = new ArrayList<String>();
        this.js = (JavascriptExecutor)this.driver;
    }

    public void setInputInformation(ArrayList<InputInfo> inputValues){
        this.inputValues = inputValues;
    }

    public void setLoginInformation(HashMap<String, String> credentials){
        if(credentials == null){
            return;
        }
        this.loginUrl = credentials.get("url");
        credentials.remove("url");
        this.loginCredentials = credentials;
    }

    public void setBaseUrl(String baseUrl){
        this.baseUrl = baseUrl;
    }

    public void printAllVisitedLinks(){
        //Remove duplicates
        LinkedHashSet<String> hashSet = new LinkedHashSet<String>(this.allVisitedUrls);
        ArrayList<String> visitedUrlsWithoutDuplicates = new ArrayList<String>(hashSet);

        //Actual stuff
        System.out.println("Max depth: " + this.maxDepth);
        System.out.println("\033[36m## Visited Links ##\033[0m");
        for(int i = 0; i < visitedUrlsWithoutDuplicates.size(); i++){
            System.out.println(i+1 + ") " + visitedUrlsWithoutDuplicates.get(i));
        }
    }

    public boolean performLogin(){
        String login_url = this.loginUrl;
        if(login_url == null || login_url.equals("")){
            return false;
        }

        //Gets into the login page
        driver.get(login_url);
        //Print some message
        System.out.println("\033[92mPerforming login... \033[0m"+ login_url);

        /* Do the actual login */
        //Obtain inputs from the webpage
        List<WebElement> elements = CrawlerUtils.findAllInputs(this.driver);
                
        //Loops through the elements and check for username / password
        WebElement formElement = null;
        for(WebElement e: elements){
            try{
                String attrName = e.getAttribute("name").toLowerCase();

                if(loginCredentials.containsKey(attrName)){
                    e.sendKeys(loginCredentials.get(attrName));

                    formElement = (WebElement)js.executeScript("return arguments[0].closest('form');", e);
                }
            }catch(org.openqa.selenium.ElementNotInteractableException exception){
                System.out.println("ElementNotInteractive: " + exception);
            }
        }

        //Submit the form
        formElement.submit();

        //Sleep for a while 
        try{
            TimeUnit.MILLISECONDS.sleep(750);
        }catch(Exception e){
            System.out.println("Something wrong with sleep (somehow): " + e);
        }

        //Test for successful login (To be done)
        return true;
    }

    public void startCrawl(){
        startCrawl(-1);
    }
    
    public void startCrawl(int maxDepth){
        this.maxDepth = maxDepth;

        //Actual crawling function
        this.visit(this.baseUrl, 0, true);

        //Do final cleanup
        if(this.inputValues != null && this.inputValues.size() != 0){
            //Try to access the pages and try to input.
            for(InputInfo i: inputValues){
                String url = i.getUrl();
                this.driver.get(i.getUrl());

                //If constantly getting redirected away then dont bother
                if(!this.driver.getCurrentUrl().equals(url)){
                    continue;
                }

                fillInputs(url);
            }
        }

        /* End of crawl stuff */
        //Save the visited URLs
        allVisitedUrls.addAll(visitedUrls);
        visitedUrls.clear();        
    }

    public void visit(String url, int curDepth, boolean toLoadUrl){
        //If link is visited, then dont bother entering it
        if(this.visitedUrls.contains(url) || (curDepth > this.maxDepth && this.maxDepth != -1)){
            return;
        }

        //Load the URL
        //Sleep for a while 
        try{
            TimeUnit.MILLISECONDS.sleep(750);
        }catch(Exception e){
            System.out.println("Something wrong with sleep (somehow): " + e);
        }

        //Load the URL
        if(toLoadUrl){
            try{
                this.driver.get(url);
            }catch(Exception e){
                System.out.println(e);
            }
        
            //url = driver.getCurrentUrl();
        }
        if(!url.equalsIgnoreCase(baseUrl)){ //Adds to array list
            this.visitedUrls.add(url); //Saves the URL into the arraylist
        }

        //Obtains all links in the current link
        ArrayList<String> webLinks = null;
        //If next depth is not going to be get accessed, then dont bother getting links for the current URL
        if(curDepth+1 <= this.maxDepth || this.maxDepth == -1){
            webLinks = CrawlerUtils.getLinks(this.driver, this.baseUrl);
        }

        if(webLinks == null || webLinks.size() <= 0){
            return;
        }

        //Debug information
        System.out.println("\033[1;33m## New URL ##\033[0m");
        System.out.println("URL\t\t:\t"+ url);
        System.out.println("Current Depth\t:\t"+ curDepth);
        System.out.println("Links\t\t: ");
        for(int i = 0; i < webLinks.size(); i++){
            System.out.println( i+1 + ") " + webLinks.get(i));
        }

        //Fill in the inputs
        this.fillInputs(url);

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

    /* This method will check whether it is a url with inputs, then fill in the input and click the submit action if there is one */
    public void fillInputs(String url){
        //Check whether the URL has any inputs to fill
        InputInfo inputinfo = InputInfo.getInputInfo(url, this.inputValues);
        if(inputinfo == null){
            return;
        }

        //Fill in the inputs
        int randint = (int)(Math.random()*100);
        for(HashMap<String, Object> d: inputinfo.getData()){
            //Obtain the selector from the hashmap
            boolean usingName = d.get("name") != null;
            String selector = ((usingName) ? String.format("[name='%s']", (String)d.get("name")) : String.format("#%s", (String)d.get("id")));
            if(selector == null){
                continue;
            }

            // Check whether the value is of type String or ArrayList
            ArrayList<String> value = null;
            if(d.get("value").getClass() == String.class){
                value = new ArrayList<String>();
                value.add((String)d.get("value"));
            }else{
                value = (ArrayList<String>) d.get("value");
            }

            //Obtain the value string
            System.out.println("Randint: " + randint%value.size());
            String finalValue = value.get(randint%value.size());
            
            //Obtain the input element
            ArrayList<WebElement> we = (ArrayList<WebElement>)this.driver.findElements(By.cssSelector(selector));
            
            if(we.size() == 0){
                continue;
            }
            
            for(WebElement e: we){
                js.executeScript("arguments[0].setAttribute('value', arguments[1])", e, finalValue);
            }
        }

        String submit = inputinfo.getSubmit();
        if(submit != null){
            this.driver.findElement(By.cssSelector(submit)).click();
        }
        inputValues.remove(inputinfo);
    }
}

class CrawlerUtils{
    static String[] blacklist_url = {"http://192.168.40.173:8000/static/trainee/ovpn/linuxclient.ovpn", "http://192.168.40.173:8000/static/trainee/ovpn/winclient.ovpn"};

    public static boolean isLoginUrl(String url){
        url = url.toLowerCase();
        if(url.matches(".*login.*")){
            return true;
        }
        return false;
    }

    // Obtains all web links and stores them onto an arraylist
    public static ArrayList<String> getLinks(WebDriver driver, String baseUrl){
        System.out.println("\033[94mFilling in form fields...\033[0m");
        //This portion finds easy links (means anchor tag with href)
        List<WebElement> elements = driver.findElements(By.cssSelector("a[href]"));
        
        //Final output variable
        ArrayList<String> webLinks = new ArrayList<String>();

        for(WebElement we: elements){
            String url = we.getAttribute("href");

            //Perform URL sanitisation
            url = url.trim();
            url = url.split("#")[0];

            //Check to make sure string is not empty or # before adding to the arraylist
            boolean toAddToArrayList = !url.trim().equals("") && !webLinks.contains(url) && url.contains(baseUrl) && !url.contains("logout") && !url.matches(".*(.ovpn|export).*");
            if(toAddToArrayList){
                webLinks.add(url);
            }
        }
        return webLinks;
    }

    public static List<WebElement> getAllButtons(WebDriver driver){
        return driver.findElements(By.cssSelector("button"));
    }

    public static List<WebElement> findAllInputs(WebDriver driver){
        return driver.findElements(By.cssSelector("input, textarea"));
    }
}
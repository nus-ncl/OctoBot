package com.webbrowsingbot.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Utils{
    /* This method will check whether it is a url with inputs, then fill in the input and click the submit action if there is one */
    public static void doActions(WebDriver driver, PageAction pageAction){
        //DEBUG 
        System.out.printf("\n\033[1;92mFilling in inputs...\033[0m %s\n", pageAction.getUrl());

        //Fill in the inputs
        int randint = (int)(Math.random()*100);
        for(HashMap<String, Object> d: pageAction.getActions()){
            //Obtain the selector from the hashmap
            String selector = null;
            if(d.get("id") != null){
                selector = String.format("#%s", d.get("id"));
            }else if(d.get("css") != null){
                selector = (String)d.get("css");
            }else if(d.get("name") != null){
                selector = String.format("[name='%s']", d.get("name"));
            }

            if(selector == null){
                continue;
            }

            //Obtain the elements
            ArrayList<WebElement> we = (ArrayList<WebElement>)driver.findElements(By.cssSelector(selector));
            if(we.size() == 0){
                continue;
            }

            //Decide what to do with the element
            if(d.get("action") != null){
                String action = ((String)d.get("action"));

                if(action.equalsIgnoreCase("click")){
                    for(WebElement e: we){
                        e.click();
                    }
                }
            }
            else if(d.get("value") != null){
                ArrayList<String> value = null;
                // Check whether the value is of type String or ArrayList
                if(d.get("value").getClass() == String.class){
                    value = new ArrayList<String>();
                    value.add((String)d.get("value"));
                }else{
                    value = (ArrayList<String>) d.get("value");
                }

                //Obtain the value string
                String finalValue = value.get(randint%value.size());
                
                for(WebElement e: we){
                    e.sendKeys(finalValue);
                }
            }
        }
    }

    public static void performLogin(WebDriver driver, String loginUrl, PageAction loginAction){
        //Print some message
        System.out.println("\033[1;92mPerforming login... \033[0m");

        if(loginUrl != null){
            driver.get(loginUrl);
        }

        Utils.doActions(driver, loginAction);
    }

    public static void performLogout(){
        
    }

    // Obtains all web links and stores them onto an arraylist
    public static ArrayList<String> getLinks(WebDriver driver, String baseUrl, ArrayList<String> blacklistUrl){
        //This portion finds easy links (means anchor tag with href)
        List<WebElement> linkElements = driver.findElements(By.cssSelector("a[href]"));
        
        //Final output variable
        ArrayList<String> linksInPage = new ArrayList<String>();

        for(WebElement we: linkElements){
            String url = we.getAttribute("href");

            //Perform URL sanitisation
            url = url.trim();
            url = url.split("#")[0];
            
            //Check to make sure string is not empty or # before adding to the arraylist
            boolean isEmpty = url.trim().equals("");
            boolean isRepeated = linksInPage.contains(url);
            boolean sameHostname = url.contains(baseUrl);
            boolean inBlacklist = blacklistUrl.contains(url);
            boolean toAddToArrayList = !isEmpty && !isRepeated && sameHostname && !inBlacklist;
            if(toAddToArrayList){
                linksInPage.add(url);
            }
        }
        return linksInPage;
    }
}
package com.webbrowsingbot.app;

import java.util.ArrayList;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Utils{
    public static void printVisitedLinks(String[] ... allUrls){
        for(String[] urls: allUrls){
            if(urls != null){
                System.out.println("## Urls ##");
                for(int i = 0; i < urls.length; i++){
                    System.out.printf("%d) %s\n", i+1, urls[i]);
                }
            }
        }
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
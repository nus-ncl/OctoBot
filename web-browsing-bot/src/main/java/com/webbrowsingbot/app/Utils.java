package com.webbrowsingbot.app;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Utils{
    public static URI parseURLtoURI(String url){
        //Adds http if needed
        url = cleanseUrl(url);

        try{
            return new URI(url);
        }catch(URISyntaxException e){
            System.err.println(e);
            return null;
        }
    }
    
    //Appends protocol if does not have http
    public static String cleanseUrl(String url){
        //Check whether URL starts with http
        if(!url.startsWith("http")){
            url = String.format("%s://%s", "http", url);
        }
        return url;
    }
    
    public static String getDomain(URI uri){
        //Check whether the uri has a port
        if(uri.getPort() < 0){
            return uri.getHost();
        }else{
            return String.format("%s:%d", uri.getHost(), uri.getPort());
        }
    }

    public static String getPath(String url){
        try{
            URI uri = new URI(url);
            return uri.getPath();
        }catch(URISyntaxException e){
            System.err.printf("Failed to get URI object: %s\n", e);
            return null;
        }
    }

    public static ArrayList<String> convertToStringArrayList(String input){
        ArrayList<String> output = new ArrayList<String>();
        output.add(input);
        return output;
    }
    public static ArrayList<String> convertToStringArrayList(ArrayList<String> input){
        return input;
    }

    @SuppressWarnings("unchecked")
    public static String chooseItem(Object obj, int randint){
        ArrayList<String> output = null;
        if(obj.getClass() == String.class){
            output = new ArrayList<String>();
            output.add((String)obj);
        }else{
            output = (ArrayList<String>)obj;
        }
        
        return output.get(randint%output.size());
    }

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
    public static ArrayList<String> getLinks(WebDriver driver, String domain, ArrayList<String> blacklistUrl){
        //This portion finds easy links (means anchor tag with href)
        List<WebElement> linkElements = driver.findElements(By.cssSelector("a[href]"));
        
        //Final output variable
        ArrayList<String> linksInPage = new ArrayList<String>();

        for(WebElement we: linkElements){
            String url = "";
            try{
                url = we.getAttribute("href");
            }catch(Exception e){
                //Probably stale element exception
            }

            //Perform URL sanitisation
            url = url.trim();
            url = url.split("#")[0];
            
            //Check to make sure string is not empty or # before adding to the arraylist
            boolean isEmpty = url.trim().equals("");
            boolean isRepeated = linksInPage.contains(url);
            boolean sameHostname = url.contains(domain);
            boolean inBlacklist = blacklistUrl.contains(url);
            boolean toAddToArrayList = !isEmpty && !isRepeated && sameHostname && !inBlacklist;
            if(toAddToArrayList){
                linksInPage.add(url);
            }
        }
        return linksInPage;
    }
}
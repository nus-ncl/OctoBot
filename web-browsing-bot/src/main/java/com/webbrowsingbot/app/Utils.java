package com.webbrowsingbot.app;

import java.net.URI;
import java.net.URISyntaxException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.UnhandledAlertException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Utils{
    public static URI parseURLtoURI(String url){
        //Adds http if needed
        url = cleanseUrl(url);

        try{
            return new URI(url);
        }catch(URISyntaxException e){
            System.err.printf("\033[91mError with getting URI object: %s\033[0m\n", e);
            return null;
        }
    }
    
    //Appends protocol if does not have http
    private static String cleanseUrl(String url){
        //Check whether URL starts with http
        if(!url.startsWith("http")){
            url = String.format("%s://%s", "http", url);
        }
        return url;
    }

    public static String getPath(String url){
        try{
            URI uri = new URI(url);
            return uri.getPath();
        }catch(URISyntaxException e){
            System.err.printf("\033[91mFailed to get URI object: %s\033[0m\n", e);
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
        return getLinks(driver, domain, blacklistUrl, true);
    }

    //Returns null for problems, empty list for no links, or list of urls
    public static ArrayList<String> getLinks(WebDriver driver, String domain, ArrayList<String> blacklistUrl, boolean sameDomain){
        //This portion finds easy links (means anchor tag with href)
        List<WebElement> linkElements = null;
        
        //This may throw timeout exception because implicit wait is set
        try{
            linkElements = driver.findElements(By.cssSelector("a[href]"));
        }catch(TimeoutException e){
            System.err.printf("\033[91mTimeoutException: Cannot find links\033[0m%n");
            return null;
        }catch(UnhandledAlertException e){
            System.err.printf("\033[91mUnhandled alert exception: Trying to close the alert\033[0m%n");
            Alert alert = driver.switchTo().alert();
            alert.accept();
        }catch(Exception e){
            System.err.printf("\033[91mError getting links: %s\033[0m%n", e);
            return null;
        }

        //Final output variable
        ArrayList<String> linksInPage = new ArrayList<String>();

        if(linkElements == null){
            return linksInPage;
        }

        for(WebElement we: linkElements){
            String url = "";

            try{
                url = we.getAttribute("href");
            }catch(org.openqa.selenium.StaleElementReferenceException e){
                //Probably stale element exception
            }catch(Exception e){
                System.err.printf("\033[91mError obtaining href attribute: %s\033[0m\n", e);
            }

            if(url == null){
                System.err.println("\033[91mURL is null\033[0m");
                continue;
            }
            //Perform URL sanitisation
            url = url.trim();
            url = url.split("#")[0];
            
            //Check to make sure string is not empty or # before adding to the arraylist
            boolean isEmpty = url.trim().equals("");
            boolean isRepeated = linksInPage.contains(url);
            boolean sameHostname = (sameDomain) ? url.contains(domain) : true;
            boolean inBlacklist = blacklistUrl.contains(url);
            boolean toAddToArrayList = !isEmpty && !isRepeated && sameHostname && !inBlacklist;
            if(toAddToArrayList){
                linksInPage.add(url);
            }
        }
        return linksInPage;
    }

    public static LocalDateTime calculateEndTime(int duration){
        LocalDateTime now = LocalDateTime.now();
        return (duration > 0) ? now.plusSeconds(duration) : null;
    }

    public static boolean haveTime(LocalDateTime endTime){
        LocalDateTime now = LocalDateTime.now();
        
        //Still have time
        return (endTime == null) ? true : now.isBefore(endTime);
    }
}
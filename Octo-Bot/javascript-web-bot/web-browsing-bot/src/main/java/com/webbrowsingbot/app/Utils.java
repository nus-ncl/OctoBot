package com.webbrowsingbot.app;

import java.net.URI;
import java.net.URISyntaxException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.*;

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

    public static boolean matchUrl(String url, PageAction pageAction){
        if(url == null || pageAction == null){
            return false;
        }
        String actionPath = pageAction.getPath();
        String actionUrl = pageAction.getUrl();
        String path = getPath(url);
        boolean pathMatch = (actionPath == null) ? false : path.matches(actionPath);
        boolean urlMatch = (actionUrl == null) ? false : url.matches(actionUrl);

        return pathMatch || urlMatch;
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
    public static ArrayList<Link> getLinks(WebDriver driver, String domain, ArrayList<String> blacklistUrl){
        return getLinks(driver, domain, blacklistUrl, true);
    }

    //Returns null for problems, empty list for no links, or list of urls
    public static ArrayList<Link> getLinks(WebDriver driver, String domain, ArrayList<String> blacklistUrl, boolean sameDomain){
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
        }catch(Exception e){
            System.err.printf("\033[91mError getting links: %s\033[0m%n", e);
            return null;
        }

        //Final output variable
        ArrayList<Link> linksInPage = new ArrayList<Link>();

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

            // If the URL location is valid, then add to array list
            if(toAddToArrayList){
                Point location = we.getLocation();
                Link l = new Link(url, location, driver.manage().window().getSize());
                linksInPage.add(l);
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

    //Takes the protocol, host, and port and add together with the respective path
    public static String craftUrl(URI uri, String loginLogoutPath){
        String path = uri.getPath();
        String fullUrl = uri.toString();
        return fullUrl.substring(0, fullUrl.length() - path.length()) + loginLogoutPath;
    }

    public static void doTests(WebDriver driver, URI uri, String testUser, HashMap<String, LoginLogoutAction> loginLogoutActionHashMap, ArrayList<PageAction> pageActionArrayList){
        LoginLogoutAction l = null;
        if(testUser != null && loginLogoutActionHashMap != null){
            l = loginLogoutActionHashMap.get(testUser);
        }
        
        if(l != null){
            String loginUrl = l.getLoginAction().getUrl();
            if(loginUrl == null){
                loginUrl = craftUrl(uri, l.getLoginAction().getPath());
            }
            l.performLogin(driver, loginUrl);
        }

        if(pageActionArrayList != null){
            for(PageAction p : pageActionArrayList){
                String actionUrl = p.getUrl();
                if(actionUrl == null){
                    actionUrl = craftUrl(uri, p.getPath());
                }
                driver.get(actionUrl);
                try{
                    TimeUnit.SECONDS.sleep(2);
                }catch(InterruptedException e){
                    System.err.println("Something went wrong with sleeping");
                }

                try{
                    String currentPath = getPath(driver.getCurrentUrl());
                    String actionPath = getPath(actionUrl);
                    if(!currentPath.contains(actionPath)){
                        continue;
                    }
                }catch(UnhandledAlertException e){
                    System.err.printf("\033[91mUnhandled alert, trying to close it\033[0m%n");
                }

                p.doActions(driver);
            }
        }

        if(l != null){
            String logoutUrl = l.getLogoutAction().getUrl();
            if(logoutUrl == null){
                logoutUrl = craftUrl(uri, l.getLogoutAction().getPath());
            }
            l.performLogout(driver, logoutUrl);
        }
    }
}
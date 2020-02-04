package com.webbrowsingbot.app;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.openqa.selenium.By;
import org.openqa.selenium.ElementNotVisibleException;
import org.openqa.selenium.InvalidElementStateException;
import org.openqa.selenium.Keys;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.UnhandledAlertException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;


public class PageAction{
    private String url; // URL means full URL
    private String path; // Path means anything behind the domain
    private ArrayList<HashMap<String, Object>> actions;

    public PageAction(){

    }

    public PageAction(String url, String path, ArrayList<HashMap<String, Object>> actions){
        this.url = url;
        this.path = path;
        this.actions = actions;
    }

    public String getPath() {
        return this.path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getUrl() {
        return this.url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public ArrayList<HashMap<String,Object>> getActions()

    {
		return this.actions;
	}

    public void setActions(ArrayList<HashMap<String,Object>> actions)
    {
		this.actions = actions;
	}

    public static ArrayList<PageAction> parse(String actionJson){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<PageAction>>(){}.getType();
        return gson.fromJson(actionJson, type);
    }

    public static PageAction getPageAction(String url, ArrayList<PageAction> pageActions){
        if(pageActions == null){
            return null;
        }

        //Extract path from URL
        for(PageAction p: pageActions){
            boolean urlMatch = Utils.matchUrl(url, p);
            
            if(urlMatch){
                return p;
            }
        }
        return null;
    }

    public void doActions(WebDriver driver){
        //DEBUG 
        try{
            System.out.printf("\033[1;92mDoing actions...\033[0m %s\n", driver.getCurrentUrl());
        }catch(UnhandledAlertException e){
            System.err.printf("\033[91mUnhandled alert, trying to close it\033[0m%n");
        }
        
        //Fill in the inputs
        if(this.actions == null){
            return;
        }

        int randint = (int)(Math.random()*100);
        for(HashMap<String, Object> d: this.getActions()){
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

            try {
                new WebDriverWait(driver, 5).until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(selector)));
            }catch(TimeoutException e){
            }

            //Obtain the elements
            WebElement webElement = null;
            try{
                webElement = driver.findElement(By.cssSelector(selector));
            }catch(NoSuchElementException e){
                System.err.printf("\033[91mNo such element: %s\033[0m%n", selector);
                continue;
            }

            if(webElement == null){
                continue;
            }

            //Decide what to do with the element
            String sentValue = null; //DEBUG Things
            String finalAction = null;
            try{
                if(d.get("action") != null){
                    String action = Utils.chooseItem(d.get("action"), randint).toLowerCase();
                    String[] actions = action.split(" ");

                    finalAction = "Action";
                    sentValue = action;
                    for(String a: actions){
                        if(a.equals("click")){
                            webElement.click();
                        }else if(a.equals("clear")){
                            webElement.clear();
                        }else if(a.equals("submit")){
                            webElement.submit();
                        }
                    }
                }else if(d.get("key") != null){
                    finalAction = "Key";
                    String key = Utils.chooseItem(d.get("key"), randint).toUpperCase();
                    String[] keyArr = key.split(" ");

                    sentValue = key;
                    for(String k: keyArr){
                        webElement.sendKeys(Keys.valueOf(k));
                    }
                }
                else if(d.get("value") != null){
                    finalAction = "Fill";
                    //Obtain the value string
                    String finalValue = Utils.chooseItem(d.get("value"), randint);

                    sentValue = finalValue;
                    webElement.sendKeys(finalValue);
                }
            }catch(ElementNotVisibleException e){
                System.err.printf("\033[91mElement not visible: %s\033[0m\n", selector);
            }catch(InvalidElementStateException e){
                System.err.printf("\033[91mInvalid element state exception: %s\033[0m\n", selector);
            }catch(Exception e){
                System.err.printf("\033[91mError doing action: %s\033[0m\n", e);
            }

            //DEBUG Things
            System.out.printf("%s: %s=%s\n", finalAction, selector, sentValue);

        }
    }
}
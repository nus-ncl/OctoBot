package com.webbrowsingbot.app;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;

import org.openqa.selenium.*;
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

    public static ArrayList<PageAction> parse(FileReader f){
        Gson gson = new Gson();

        Type type = new TypeToken<ArrayList<PageAction>>(){}.getType();
        return gson.fromJson(f, type);
    }

    public static PageAction getPageAction(String url, ArrayList<PageAction> pageActions){
        if(pageActions == null){
            return null;
        }

        //Extract path from URL
        for(PageAction p: pageActions){
            String path = Utils.getPath(url);
            boolean urlMatch = (p.url == null) ? true : url.matches(p.url);
            boolean pathMatch = (p.path == null) ? true : path.matches(p.path);
            if(urlMatch && pathMatch){
                return p;
            }
        }
        return null;
    }

    public void doActions(WebDriver driver){
        //DEBUG 
        System.out.printf("\033[1;92mDoing actions...\033[0m %s\n", driver.getCurrentUrl());

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

            //Wait for 3 seconds or until the element is clickable
            try{
                new WebDriverWait(driver, 3).until(ExpectedConditions.elementToBeClickable(By.cssSelector(selector)));
            }catch(Exception e){
                //Dont show the error
            }

            //Obtain the elements
            WebElement webElement = null;
            try {
                webElement = (WebElement)driver.findElement(By.cssSelector(selector));
            }catch(NoSuchElementException e){
                System.err.printf("\033[91mNo such element: %s\033[0m%n", selector);
                continue;
            }

            if(webElement == null){
                continue;
            }

            try {
                new WebDriverWait(driver, 3)
                    .until(ExpectedConditions.elementToBeClickable(webElement));
            }catch(TimeoutException e){
                //Ignore and don't print error message
            }
            //Decide what to do with the element
            String sentValue = null; //DEBUG Things
            String finalAction = null;
            try{
                if(d.get("action") != null){
                    finalAction = "Click";
                    String action = Utils.chooseItem(d.get("action"), randint);

                    if(action.equalsIgnoreCase("click")){
                        sentValue = "click";
                        webElement.click();
                    }
                }else if(d.get("key") != null){
                    finalAction = "Key";
                    String key = Utils.chooseItem(d.get("key"), randint);
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
            }catch(org.openqa.selenium.ElementNotVisibleException e){
                System.err.printf("\033[91mElement not visible: %s\033[0m\n", selector);
                continue;
            }catch(Exception e){
                System.err.printf("\033[91mError doing action: %s\033[0m\n", e);
                continue;
            }

            //DEBUG Things
            System.out.printf("%s: %s=%s\n", finalAction, selector, sentValue);
        }
    }
}
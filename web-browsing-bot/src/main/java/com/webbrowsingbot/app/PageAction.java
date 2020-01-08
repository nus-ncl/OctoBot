package com.webbrowsingbot.app;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;


public class PageAction{
    private String url;
    private ArrayList<HashMap<String, Object>> actions;

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
        for(PageAction p: pageActions){
            if(url.matches(p.url)){
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
                new WebDriverWait(driver, 3).ignoring(StaleElementReferenceException.class).until(ExpectedConditions.elementToBeClickable(By.cssSelector(selector)));
            }catch(Exception e){
                //Dont show the error
            }
            //Obtain the elements
            ArrayList<WebElement> we = (ArrayList<WebElement>)driver.findElements(By.cssSelector(selector));
            if(we.size() == 0){
                //If the element does not exist, just try another element
                System.err.printf("Failed to find element: %s\n", selector);
                continue;
            }

            //Decide what to do with the element
            try{
                if(d.get("action") != null){
                    String action = Utils.chooseItem(d.get("action"), randint);

                    if(action.equalsIgnoreCase("click")){
                        for(WebElement e: we){
                            e.click();
                        }
                    }
                }else if(d.get("key") != null){
                    String key = Utils.chooseItem(d.get("key"), randint);
                    String[] keyArr = key.split(" ");

                    for(WebElement e: we){
                        for(String k: keyArr){
                            e.sendKeys(Keys.valueOf(k));
                        }
                    }
                }
                else if(d.get("value") != null){
                    //Obtain the value string
                    String finalValue = Utils.chooseItem(d.get("value"), randint);
                    
                    for(WebElement e: we){
                        e.sendKeys(finalValue);
                    }
                }
            }catch(Exception e){
                System.err.printf("Error doing action: %s\n", e);
                continue;
            }
        }
    }
}
package com.webbrowsingbot.app;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class Utils{
    /* This method will check whether it is a url with inputs, then fill in the input and click the submit action if there is one */
    public static void fillInputs(WebDriver driver, String url, ArrayList<InputInfo> inputValues){
        //Check whether the URL has any inputs to fill
        InputInfo inputinfo = InputInfo.getInputInfo(url, inputValues);
        if(inputinfo == null){
            return;
        }

        //Some variable declration here
        JavascriptExecutor js = (JavascriptExecutor)driver;

        //DEBUG 
        System.out.printf("\n\033[1;92mFilling in inputs...\033[0m %s\n", inputinfo.getUrl());

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
            String finalValue = value.get(randint%value.size());
            
            //Obtain the input element
            ArrayList<WebElement> we = (ArrayList<WebElement>)driver.findElements(By.cssSelector(selector));
            
            if(we.size() == 0){
                continue;
            }
            
            for(WebElement e: we){
                js.executeScript("arguments[0].value = arguments[1]", e, finalValue);
            }
        }

        //Submit the damn thing
        String submit = inputinfo.getSubmit();
        if(submit != null){
            List<WebElement> submitBtns = driver.findElements(By.cssSelector(submit));
            for(WebElement submitBtn: submitBtns)
                js.executeScript("arguments[0].click()", submitBtn);
        }
        inputValues.remove(inputinfo);
    }

    public static void performLogin(WebDriver driver, HashMap<String, String> loginCredentials){
        //Print some message
        System.out.println("\n\033[1;92mPerforming login... \033[0m");

        //Fill in credentials
        int temporarycountvariable = 0;
        WebElement form = null;
        JavascriptExecutor js = (JavascriptExecutor)driver;
        for(String key: loginCredentials.keySet()){
            List<WebElement> webElements = driver.findElements(By.cssSelector(String.format("[name='%s']", key)));
            for(WebElement we: webElements){
                js.executeScript("arguments[0].value = arguments[1]", we, loginCredentials.get(key));
            }
            if(temporarycountvariable <= 0){
                form = (WebElement)js.executeScript("return arguments[0].closest('form');", webElements.get(0));
                temporarycountvariable++;
            }
        }

        //Find the login button somehow
        WebElement submitBtn = driver.findElement(By.cssSelector("[type='submit']")); //Please change this
        submitBtn.click();
    }

    public static void performLogout(){
        
    }
}
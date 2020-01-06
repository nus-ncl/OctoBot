package com.webbrowsingbot.app;

import java.io.File;
import java.util.concurrent.TimeUnit;

//Selenium imports
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class BrowserSelector{
    private static String jarFilePath = null;
    
    public static void getJarFilePath() throws Exception{
        jarFilePath = new File(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent();
    }
    
    public static WebDriver getFirefoxDriver() throws Exception{
        if(jarFilePath == null){
            getJarFilePath();
        }
        System.setProperty("webdriver.gecko.driver", jarFilePath+"/drivers/geckodriver");
        System.setProperty(FirefoxDriver.SystemProperty.BROWSER_LOGFILE, "/dev/null");

        WebDriver driver = new FirefoxDriver();
        driver.manage().timeouts().pageLoadTimeout(3, TimeUnit.SECONDS);
        
        //driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS); //https://www.machmetrics.com/speed-blog/average-page-load-times-websites-2018/
	
        return driver;
    }
}
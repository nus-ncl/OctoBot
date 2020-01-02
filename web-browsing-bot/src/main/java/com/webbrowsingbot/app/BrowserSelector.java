package com.webbrowsingbot.app;

import java.io.File;
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

        return new FirefoxDriver();
    }
}
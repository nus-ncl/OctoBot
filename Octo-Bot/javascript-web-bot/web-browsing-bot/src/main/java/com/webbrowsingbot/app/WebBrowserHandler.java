package com.webbrowsingbot.app;

//Java imports
import java.io.File;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.UnexpectedAlertBehaviour;
//Selenium imports
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.remote.CapabilityType;

public class WebBrowserHandler{
    private static String jarFilePath = null;
    
    public static void getJarFilePath() throws Exception{
        jarFilePath = new File(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent();
    }

    public static WebDriver getDriver(String browser, String userAgent, boolean headless) throws Exception{
        if(jarFilePath == null){
            getJarFilePath();
        }

        //Try to make the browser format uniform
        browser = browser.strip().toLowerCase();

        //Initialise the proper driver
        WebDriver driver = null;
        switch(browser){
            case "firefox":
                //Set property
                System.setProperty("webdriver.gecko.driver", jarFilePath+"/drivers/geckodriver");
                System.setProperty(FirefoxDriver.SystemProperty.BROWSER_LOGFILE, "/dev/null"); //Disable output

                //Set options
                FirefoxOptions firefoxOptions = new FirefoxOptions();
                if(headless) {
                    firefoxOptions.setHeadless(true);
                }

                //Setting up user agent
                if(userAgent != null){
                    firefoxOptions.addPreference("general.useragent.override", userAgent);
                }

                firefoxOptions.setCapability(CapabilityType.UNEXPECTED_ALERT_BEHAVIOUR, UnexpectedAlertBehaviour.ACCEPT);
                driver = new FirefoxDriver(firefoxOptions);
                break;

            case "chrome":
                //Set property
                System.setProperty("webdriver.chrome.driver", jarFilePath+"/drivers/chromedriver");
                System.setProperty("webdriver.chrome.silentOutput", "true");

                //Chrome options
                ChromeOptions chromeOptions = new ChromeOptions();
                //If headless
                if(headless){
                    chromeOptions.setHeadless(true);
                }

                //If user creates his own userAgent
                if(userAgent != null){
                    chromeOptions.addArguments(String.format("user-agent=%s", userAgent));
                }

                // This is for chrome to launch properly
                chromeOptions.addArguments("--no-sandbox", "--disable-dev-shm-usage");
                chromeOptions.setCapability(CapabilityType.UNEXPECTED_ALERT_BEHAVIOUR, UnexpectedAlertBehaviour.ACCEPT);
                driver = new ChromeDriver(chromeOptions);
                break;
        }

        if(driver != null){
            driver.manage().timeouts().pageLoadTimeout(60, TimeUnit.SECONDS);
            driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS); //https://www.machmetrics.com/speed-blog/average-page-load-times-websites-2018/	
            
            return driver;
        }

        return null;
    }
}
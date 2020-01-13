package com.webbrowsingbot.app;

//Java imports
import java.io.File;
import java.util.concurrent.TimeUnit;

//Selenium imports
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.firefox.FirefoxProfile;

public class WebBrowserHandler{
    private static String jarFilePath = null;
    
    public static void getJarFilePath() throws Exception{
        jarFilePath = new File(Main.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent();
    }

    public static WebDriver getDriver(String browser, boolean headless) throws Exception{
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
                FirefoxOptions options = new FirefoxOptions();
                if(headless) {
                    options.setHeadless(true);
                }

                driver = new FirefoxDriver(options);
                break;
            
            case "chrome":
                //Set property
                System.setProperty("webdriver.chrome.driver", jarFilePath+"/drivers/chromedriver");
                System.setProperty("webdriver.chrome.silentOutput", "true");

                //Chrome options
                ChromeOptions chromeOptions = new ChromeOptions();
                if(headless){
                    chromeOptions.setHeadless(true);
                }
                // This is for chrome to launch properly
                chromeOptions.addArguments("--no-sandbox", "--disable-dev-shm-usage");
                driver = new ChromeDriver(chromeOptions);
                break;
        }

        if(driver != null){
            driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
            driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS); //https://www.machmetrics.com/speed-blog/average-page-load-times-websites-2018/	
            
            return driver;
        }

        return null;
    }
}
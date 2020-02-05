package com.webbrowsingbot.app;

import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;

//Selenium imports
import org.openqa.selenium.WebDriver;

//Argparse4j imports
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.impl.Arguments;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;

public class Main {
    public static ArgumentParser createArgumentParser(){
        ArgumentParser parser = ArgumentParsers.newFor("prog").build()
                                .description("Bot that browses the web");
        parser.addArgument("-b", "--browser") //Browser
              .metavar("BROWSER_NAME")
              .setDefault("chrome")
              .type(String.class)
              .help("Browser to utilise (Default chrome)");
        parser.addArgument("-c", "--crawl") //Crawl first or not
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Boolean on whether to crawl first or not");
        parser.addArgument("-d", "--depth") //Max depth
              .metavar("DEPTH")
              .type(Integer.class)
              .help("Depth to crawl website from entrypoint");
        parser.addArgument("-H", "--headless") //Max depth
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Boolean to launch browser in headless mode");
        parser.addArgument("-o", "--other-domain") //Allow other domain
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Allow to crawl to different domain");
        parser.addArgument("-t", "--time") //Time to browse
              .metavar("DURATION")
              .type(Integer.class)
              .help("Max time to browse (seconds)");
        parser.addArgument("-T", "--test") //Time to browse
              .metavar("USERNAME")
              .nargs("?")
              .setConst("")
              .type(String.class)
              .help("Test user actions");
        parser.addArgument("-u", "--user-agent") //Time to browse
              .metavar("USER_AGENT")
              .type(String.class)
              .help("User agent to use");
        parser.addArgument("-l", "--login")
              .type(String.class)
              .metavar("LOGIN_JSON")
              .help("JSON configuration for login");
        parser.addArgument("-a", "--action")
              .metavar("ACTION_JSON")
              .type(String.class)
              .help("JSON configuration for actions");
        parser.addArgument("url")
              .type(String.class)
              .help("URL to crawl and do actions");
        return parser;
    }

    public static void main(String[] args)throws Exception {
        /* Start of argparse */
        //Parse arguments using argparse4j
        ArgumentParser parser = createArgumentParser();
        Namespace res = null;
        try {
            res = parser.parseArgs(args);
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        //Parse the arguments
        //To crawl parameter
        boolean toCrawl = res.get("crawl");

        //Depth
        int depth = (res.get("depth") == null) ? -1 : res.get("depth");

        //Time
        int maxDuration = (res.get("time") == null) ? -1: res.get("time");

        //Test
        String testUser = (String)res.get("test");

        //Same domain
        boolean sameDomain = !(boolean)res.get("other_domain");

        //Headless
        boolean isHeadless = (boolean)res.get("headless");

        //Actions
        String actionJson = res.get("action");
        ArrayList<PageAction> pageActions = null;
        try{
            if(actionJson != null)
                pageActions = PageAction.parse(actionJson);
        }catch(Exception e){
            System.err.printf("\033[91mSomething went wrong parsing page actions: %s\033[0m\n", e);
            System.exit(1);
        }

        //Login
        String loginJson = res.get("login");
        HashMap<String, LoginLogoutAction> loginLogoutAction = null;
        try{
            if(loginJson!=null)
                loginLogoutAction = LoginLogoutAction.parse(loginJson);   
        }catch(Exception e){
            System.err.printf("\033[91mSomething went wrong parsing login and logout information: %s\033[0m\n", e);
            System.exit(1);
        }

        //URL
        String url = res.get("url");
        String browser = (String)res.get("browser");
        String userAgent = (String)res.get("user_agent");
        /* End of argparse */

        //Parse into URI
        URI uri = Utils.parseURLtoURI(url);
        if(uri == null){
            System.exit(1);
        }
        url = uri.toString();

        /* Start of printing argparse arguments */
        System.out.println("\033[1;93m## Arguments ##\033[0m");
        System.out.printf("URL\t\t:\t%s\n", url);
        System.out.printf("Browser\t\t:\t%s\n", browser);
        System.out.printf("Crawl\t\t:\t%b\n", toCrawl);
        System.out.printf("Max depth\t:\t%d\n", depth);
        System.out.printf("Headless\t:\t%b\n", isHeadless);
        System.out.printf("Same domain\t:\t%b\n", sameDomain);
        System.out.printf("Time\t\t:\t%d\n", maxDuration);
        System.out.printf("Test\t\t:\t%s\n", testUser);
        System.out.printf("User agent\t:\t%s\n", userAgent);
        System.out.printf("Login file\t:\t%s\n", loginJson!=null);
        System.out.printf("Action file\t:\t%s\n", actionJson!=null);
        /* End of printing argparse arguments */

        //BrowserSelection (We stick with firefox for now)     
        WebDriver driver = WebBrowserHandler.getDriver(browser, userAgent, isHeadless);
        if(driver == null){
            System.err.printf("\033[91mBrowser '%s' cannot be found\033[0m\n", browser);
            System.exit(1);
        }

        //If test, execute test first
        if(testUser != null){
            Utils.doTests(driver, uri, testUser, loginLogoutAction, pageActions);
            driver.quit();
            System.exit(0);
        }

        //Crawler section
        HashMap<String, ArrayList<String>> urls = null;
        if(toCrawl){
            //Initialize crawler
            Crawler crawler = new Crawler(driver, sameDomain);
            //Set URL to crawl
            crawler.setDomain(uri.getHost());
            //Set login credentials
            crawler.setLoginLogoutActions(loginLogoutAction);
            
            //Declare URLS variable
            urls = new HashMap<String, ArrayList<String>>();

            //Start initial crawl
            ArrayList<String> urlsCrawled = crawler.startCrawl(url, depth);
            urls.put(null, urlsCrawled);

            //Perform login & crawl the website again
            String username = null;
            while((username=crawler.performLogin(uri)) != null){
                urlsCrawled = crawler.startCrawl(url, depth);
                urls.put(username, urlsCrawled);
            }

            System.out.println("\033[1;36mCrawled links:\033[0m");
            System.out.println(urls);

            driver.quit();

            driver = WebBrowserHandler.getDriver(browser, userAgent, isHeadless);
        }

        // Start the actual browsing
        BrowserBot browserBot = new BrowserBot(driver, uri.getHost(), urls, loginLogoutAction, pageActions, sameDomain);
        browserBot.browse(url, maxDuration);

        // After finish browsing, quit
        driver.quit();
    }
}
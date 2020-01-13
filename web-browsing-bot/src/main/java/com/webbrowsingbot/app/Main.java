package com.webbrowsingbot.app;

//Java imports
import java.io.FileReader;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
//Argparse4j imports
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.impl.Arguments;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;
//Selenium imports
import org.openqa.selenium.WebDriver;

public class Main {
    public static ArgumentParser createArgumentParser(){
        ArgumentParser parser = ArgumentParsers.newFor("prog").build()
                                .description("Bot that browses the web");
        parser.addArgument("-b", "--browser") //Browser
              .metavar("browser_name")
              .setDefault("firefox")
              .type(String.class)
              .help("Browser to utilise");
        parser.addArgument("-c", "--crawl") //Crawl first or not
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Boolean on whether to crawl first or not");
        parser.addArgument("-d", "--depth") //Max depth
              .metavar("depth")
              .type(Integer.class)
              .help("Depth to crawl website from entrypoint");
        parser.addArgument("--headless") //Max depth
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Boolean to launch browser in headless mode");
        parser.addArgument("-o", "--other-domain") //Allow other domain
              .action(Arguments.storeTrue())
              .type(Boolean.class)
              .help("Allow to crawl to different domain");
        parser.addArgument("-t", "--time") //Time to browse
              .type(Integer.class)
              .help("Max time to browse (seconds)");
        parser.addArgument("-l", "--login-file")
              .type(String.class)
              .metavar("login_file")
              .help("File that contains login credentials");
        parser.addArgument("-a", "--action-file")
              .metavar("action_file")
              .type(String.class)
              .help("File that contains actions to do on selected page(s)");
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

        //Same domain
        boolean sameDomain = !(boolean)res.get("other_domain");

        //Headless
        boolean isHeadless = (boolean)res.get("headless");

        //Actions
        String file_name = res.get("action_file");
        ArrayList<PageAction> pageActions = null;
        try{
            if(file_name != null)
                pageActions = PageAction.parse(new FileReader(file_name));
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }catch(Exception e){
            System.err.printf("Something went wrong parsing page actions: %s\n", e);
            System.exit(1);
        }

        //Login
        String loginfile_name = res.get("login_file");
        HashMap<String, LoginLogoutAction> loginLogoutAction = null;
        try{
            if(loginfile_name!=null)
                loginLogoutAction = LoginLogoutAction.parse(new FileReader(loginfile_name));   
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }
        catch(Exception e){
            System.err.printf("Something went wrong parsing login and logout information: %s\n", e);
            System.exit(1);
        }

        //URL
        String url = res.get("url");
        String browser = (String)res.get("browser");
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
        System.out.printf("Other domain\t:\t%b\n", sameDomain);
        System.out.printf("Time\t\t:\t%d\n", maxDuration);
        System.out.printf("Login file\t:\t%s\n", loginfile_name);
        System.out.printf("Action file\t:\t%s\n", file_name);
        /* End of printing argparse arguments */

        //BrowserSelection (We stick with firefox for now)     
        WebDriver driver = WebBrowserHandler.getDriver(browser, isHeadless);
        if(driver == null){
            System.err.printf("Browser '%s' cannot be found\n", browser);
            System.exit(1);
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

            driver = WebBrowserHandler.getDriver(browser, isHeadless);
        }

        // Start the actual browsing
        BrowserBot browserBot = new BrowserBot(driver, uri.getHost(), urls, loginLogoutAction, pageActions);
        browserBot.browse(url, maxDuration);

        // After finish browsing, quit
        driver.quit();
    }
}
package com.webbrowsingbot.app;

//Java imports
import java.io.FileReader;
import java.net.URI;
import java.util.ArrayList;
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
        parser.addArgument("-a", "--action-file")
              .metavar("action_file")
              .help("File that contains values to form input fields");
        parser.addArgument("-b", "--browser")
              .metavar("browser_name")
              .setDefault("firefox")
              .help("Browser to utilise");
        parser.addArgument("-c", "--crawl")
              .action(Arguments.storeTrue())
              .help("File that contains values to form input fields");
        parser.addArgument("-d", "--depth")
              .metavar("depth")
              .help("Max depth to crawl");
        parser.addArgument("-l", "--login-file")
              .metavar("login_file")
              .help("File that contains login credentials");
        parser.addArgument("url")
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
            System.out.println("\033[1;93m## Arguments ##\033[0m");
            System.out.printf("URL\t\t:\t%s\n", (String)res.get("url"));
            System.out.printf("Browser\t\t:\t%s\n", (String)res.get("browser"));
            System.out.printf("Crawl\t\t:\t%s\n", Boolean.toString(res.get("crawl")));
            System.out.printf("Max depth\t:\t%s\n", (String)res.get("depth"));
            System.out.printf("Login file\t:\t%s\n", (String)res.get("login_file"));
            System.out.printf("Action file\t:\t%s\n", (String)res.get("action_file"));
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        //Parse the arguments
        //To crawl parameter
        boolean toCrawl = false;
        if(res.get("crawl") != null){
            toCrawl = res.get("crawl");
        }

        //Depth
        int depth = -1;
        if(res.get("depth") != null){
            try{
                depth = Integer.parseInt((String)res.get("depth"));
            }catch(NumberFormatException e){
                System.err.printf("Invalid value for depth: %s\n", e);
                System.exit(1);
            }
        }

        //Actions
        String file_name = res.get("action_file");
        ArrayList<PageAction> pageActions = null;
        try{
            if(file_name != null)
                pageActions = PageAction.parse(new FileReader(file_name));
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }

        //Login
        String loginfile_name = res.get("login_file");
        LoginLogoutAction loginLogoutAction = null;
        try{
            if(loginfile_name!=null)
                loginLogoutAction = LoginLogoutAction.parse(new FileReader(loginfile_name));   
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }

        //URL
        String url = res.get("url");
        /* End of argparse */

        //BrowserSelection (We stick with firefox for now)
        String browser = (String)res.get("browser");          
        WebDriver driver = WebBrowserHandler.getDriver(browser);
        if(driver == null){
            System.err.printf("Browser '%s' cannot be found\n", browser);
            System.exit(1);
        }
        
        //Parse into URI
        URI uri = Utils.parseURLtoURI(url);
        if(uri == null){
            System.exit(1);
        }
        url = uri.toString();
        
        // loginLogoutAction.performLogin(driver, true);
        // for(PageAction p: pageActions){
        //     driver.get(p.getUrl());
        //     p.doActions(driver);
        // }
        // driver.quit();
        // System.exit(0);
        
        //Crawler section
        ArrayList<String> urls = null, urlsRequireLogin = null;
        if(toCrawl){
            //Initialize crawler
            Crawler crawler = new Crawler(driver);
            //Set URL to crawl
            crawler.setDomain(uri.getHost());
            //Set login credentials
            crawler.setLoginLogoutAction(loginLogoutAction);
            
            //Start initial crawl
            urls = crawler.startCrawl(url, depth);

            //Perform login & crawl the website again
            urlsRequireLogin = null;
            if(crawler.performLogin(uri)){
                urlsRequireLogin = crawler.startCrawl(url, depth);
            }

            //Utils.printVisitedLinks(urls.toArray(new String[urls.size()]), urlsRequireLogin.toArray(new String[urlsRequireLogin.size()]));

            driver.quit();

            driver = WebBrowserHandler.getDriver(browser);
        }

        //Start the actual browsing
        BrowserBot browserBot = new BrowserBot(driver, uri.getHost(), urls, urlsRequireLogin, loginLogoutAction, pageActions);
        browserBot.browse(url);
    }
}
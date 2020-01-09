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
        parser.addArgument("-b", "--browser")
              .metavar("browser_name")
              .setDefault("firefox")
              .help("Browser to utilise");
        parser.addArgument("-c", "--crawl")
              .action(Arguments.storeTrue())
              .help("Boolean on whether to crawl first or not");
        parser.addArgument("-d", "--depth")
              .metavar("depth")
              .help("Depth to crawl website from entrypoint");
        parser.addArgument("-o", "--other-domain")
              .action(Arguments.storeTrue())
              .help("Allow to crawl to different domain");
        parser.addArgument("-l", "--login-file")
              .metavar("login_file")
              .help("File that contains login credentials");
        parser.addArgument("-a", "--action-file")
              .metavar("action_file")
              .help("File that contains actions to do on selected page(s)");
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

            //Output things
            System.out.println("\033[1;93m## Arguments ##\033[0m");
            System.out.printf("URL\t\t:\t%s\n", (String)res.get("url"));
            System.out.printf("Browser\t\t:\t%s\n", (String)res.get("browser"));
            System.out.printf("Crawl\t\t:\t%s\n", Boolean.toString(res.get("crawl")));
            System.out.printf("Max depth\t:\t%s\n", (String)res.get("depth"));
            System.out.printf("Other domain\t:\t%s\n", Boolean.toString(res.get("other_domain")));
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

        //Same domain
        boolean sameDomain = false;
        if(res.get("other_domain") != null){
            sameDomain = !(boolean)res.get("other_domain");
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
        }catch(Exception e){
            System.err.printf("Something went wrong parsing page actions: %s\n", e);
            System.exit(1);
        }

        //Login
        String loginfile_name = res.get("login_file");
        ArrayList<LoginLogoutAction> loginLogoutAction = null;
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

            System.out.println(urls);
            //Utils.printVisitedLinks(urls.toArray(new String[urls.size()]), urlsRequireLogin.toArray(new String[urlsRequireLogin.size()]));

            driver.quit();

            driver = WebBrowserHandler.getDriver(browser);
        }

        //Start the actual browsing
        BrowserBot browserBot = new BrowserBot(driver, uri.getHost(), urls, loginLogoutAction, pageActions);
        browserBot.browse(url);
    }
}
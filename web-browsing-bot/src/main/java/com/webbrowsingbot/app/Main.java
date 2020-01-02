package com.webbrowsingbot.app;

//Gson
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
//Java imports
import java.io.FileReader;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
//Argparse4j imports
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;
//Selenium imports
import org.openqa.selenium.WebDriver;


public class Main {
    public static ArgumentParser createArgumentParser(){
        ArgumentParser parser = ArgumentParsers.newFor("prog").build()
                                .description("Bot that browses the web");
        parser.addArgument("-d", "--depth")
              .metavar("depth")
              .help("Max depth to crawl");
        parser.addArgument("-i", "--input-file")
              .metavar("input_file")
              .help("File that contains values to form input fields");
        parser.addArgument("-l", "--login-file")
              .metavar("login_file")
              .help("File that contains login credentials");
        parser.addArgument("url")
              .help("URL to crawl and do actions");
        return parser;
    }

    public static HashMap<String, String> parseLoginCredentials(FileReader login_file){
        //Declare gson object
        Gson gson = new Gson();

        //Set the type and get the information out of the json file
        Type type = new TypeToken<HashMap<String, String>>(){}.getType();
        return gson.fromJson(login_file, type);
    }

    public static void main(String[] args)throws Exception {
        //Parse arguments using argparse4j
        ArgumentParser parser = createArgumentParser();
        Namespace res = null;
        try {
            res = parser.parseArgs(args);
            System.out.println("\033[1;93m## Arguments ##\033[0m");
            System.out.printf("URL\t\t:\t%s\n", res.get("url"));
            System.out.printf("Max depth\t:\t%s\n", res.get("depth"));
            System.out.printf("Login file\t:\t%s\n", res.get("login_file"));
            System.out.printf("Input file\t:\t%s\n", res.get("input_file"));
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        //Parse the arguments
        int depth = -1;
        if(res.get("depth") != null){
            try{
                depth = Integer.parseInt((String)res.get("depth"));
            }catch(NumberFormatException e){
                System.err.printf("Invalid value for depth: %s\n", e);
                System.exit(0);
            }
        }
        
        String file_name = res.get("input_file");
        ArrayList<InputInfo> inputInfo = null;
        try{
            if(file_name != null)
                inputInfo = InputInfo.parse(new FileReader(file_name));
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }

        String loginfile_name = res.get("login_file");
        LoginInformation loginInfo = null;
        try{
            if(loginfile_name!=null)
                loginInfo = LoginInformation.parse(new FileReader(loginfile_name));   
        }catch(java.io.FileNotFoundException e){
            System.err.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }
        //Parameters
        String url = res.get("url");

        //BrowserSelection (We stick with firefox for now)          
        WebDriver driver = BrowserSelector.getFirefoxDriver();
        
        driver.get("http://192.168.40.129:8000/login");

        //Initialize crawler
        Crawler crawler = new Crawler(driver);

        //Set URL to crawl
        crawler.setBaseUrl(url);

        //Set input information
        crawler.setInputInformation(inputInfo);

        //Set login credentials
        crawler.setLoginInformation(loginInfo);
        
        //Start initial crawl
        ArrayList<String> urls = crawler.startCrawl(depth);

        //Perform login & crawl the website again
        ArrayList<String> urlsRequireLogin = null;
        if(crawler.performLogin()){
            urlsRequireLogin = crawler.startCrawl(depth);
        }

        //Start the actual browsing
        BrowserBot browser = new BrowserBot(driver, urls, urlsRequireLogin, inputInfo);
        browser.browse();
        driver.quit();
    }
}
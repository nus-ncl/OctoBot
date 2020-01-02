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
            System.out.println("## Arguments ##");
            System.out.printf("URL\t\t:\t%s\n", res.get("url"));
            System.out.printf("Login file\t:\t%s\n", res.get("login_file"));
            System.out.printf("Input file\t:\t%s\n", res.get("input_file"));
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        //Parse the arguments
        String file_name = res.get("input_file");
        ArrayList<InputInfo> inputInfo = null;
        try{
            if(file_name != null)
                inputInfo = InputInfo.parse(new FileReader(file_name));
        }catch(java.io.FileNotFoundException e){
            System.out.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }

        String loginfile_name = res.get("login_file");
        HashMap<String, String> loginCredential = null;
        try{
            if(loginfile_name!=null)
                loginCredential = parseLoginCredentials(new FileReader(loginfile_name));   
        }catch(java.io.FileNotFoundException e){
            System.out.printf("Cannot open file reader: %s\n", e);
            System.exit(1);
        }
        //Parameters
        String url = res.get("url");

        //BrowserSelection (We stick with firefox for now)          
        WebDriver driver = BrowserSelector.getFirefoxDriver();
        
        //driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        
        //Initialize crawler
        Crawler crawler = new Crawler(driver);

        //Set URL to crawl
        crawler.setBaseUrl(url);

        //Set input information
        crawler.setInputInformation(inputInfo);

        //Set login credentials
        crawler.setLoginInformation(loginCredential);
        
        //Start initial crawl
        crawler.startCrawl();

        //Perform login & crawl the website again
        if(crawler.performLogin()){
            crawler.startCrawl();
        }
        
        //Output stuff
        crawler.printAllVisitedLinks();
        
        driver.quit();
    }
}
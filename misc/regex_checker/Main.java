//Arg 1 is regex, arg2 is string
public class Main{
    public static void main(String[] args){
        if(args.length <= 0){
            System.err.println("Usage: prog <regex> <string>");
        }

        boolean match = args[1].matches(args[0]);
        System.out.println(match);
    }
}
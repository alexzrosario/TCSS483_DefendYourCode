import java.io.PrintStream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Scanner;

public class Main {
    private static PrintStream errors;
    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);
        try {
            errors = new PrintStream("errorlog.txt"); 
        } catch (Exception e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        //Enter a first name
        //String firstName = name(scan);
        //Enter a last name
        //String lastName = name(scan);
        //sum two integers
        int sum = sum(scan);
        
        //System.out.println(sum);
        //System.out.println(firstName+lastName);
        errors.close();
    }
    
    public static String name(Scanner scan) {
        String theString = "";
        boolean matches = false;
        while(!matches){
            System.out.println("Enter a valid name (Start with a capital letter followed by a-z or a '-'): ");
            theString = scan.nextLine();
            Pattern p = Pattern.compile("^[A-Z][-a-z]{1,49}$");
            Matcher m = p.matcher(theString);
            matches = m.matches();
            if (!matches) {
                errors.println("ERROR in name(): Invalid Name Entered");
            }
        }
        System.out.println("Name Accepted");
        return theString;
    }

    public static int sum(Scanner scan) {
        long i1, i2, theSum = 0;
        boolean flag = false;
        while (!flag) {
            try {
                System.out.println("Enter a valid int: ");
                i1 = scan.nextLong();
                System.out.println("Enter another valid int: ");
                i2 = scan.nextLong();
                if (i1 + i2 > Integer.MAX_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured");
                    System.out.println("Integer values too large");
                }else if(i1 > Integer.MAX_VALUE || i2 > Integer.MAX_VALUE){
                    errors.println("ERROR in sum(): One or both int larger than " + Integer.MAX_VALUE);
                    System.out.println("Integers must be < " + Integer.MAX_VALUE);
                }else if(i1 < Integer.MIN_VALUE || i2 < Integer.MIN_VALUE){
                    errors.println("ERROR in sum(): One or both int smaller than " + Integer.MIN_VALUE);
                    System.out.println("Integers must be > " + Integer.MIN_VALUE);
                }else{
                    flag=true;
                    theSum = i1 + i2;
                }
            } catch (Exception e) {
                errors.println("ERROR in sum(): Value entered is not a int");
                scan.nextLine();
            }
        }
        return ((int)theSum);
        
    }
}



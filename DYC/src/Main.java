import java.io.File;
import java.io.PrintStream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Scanner;


public class Main {
    private static PrintStream errors;
    private static PrintStream passwordStorage;
    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);
        try {
            errors = new PrintStream("errorlog.txt");
            passwordStorage = new PrintStream("password.txt");  
        } catch (Exception e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        //Enter a first name
        //String firstName = name(scan);
        //Enter a last name
        //String lastName = name(scan);
        //sum two integers
        //int[] results = sum(scan);
        //create function for input/output files
    
        String inputfile = readInputFile(scan);
        String outputfile = readInputFile(scan,inputfile);
        //salt and hash password
        //createPassword(scan);
        //verifyPassword(scan);

        //System.out.println(results[0]);
        //System.out.println(results[1]);
        //System.out.println(sum);
        //System.out.println(firstName+lastName);
        errors.close();
        passwordStorage.close();
    }
    
    public static String name(Scanner scan) {
        String theString = "";
        boolean matches = false;
        while(!matches){
            System.out.println("\nEnter a valid name (Start with a capital letter followed by a-z or a '-'): ");
            theString = scan.nextLine();
            Pattern p = Pattern.compile("^[A-Z][-a-z]{1,49}$");
            Matcher m = p.matcher(theString);
            matches = m.matches();
            if (!matches) {
                System.out.println("Invalid Name Entered.");
                errors.println("ERROR in name(): Invalid Name Entered.");
            }
        }
        System.out.println("Name Accepted.");
        return theString;
    }

    public static int[] sum(Scanner scan) {
        long i1, i2 = 0;
        boolean flag = false;
        int[] results = new int[2];
        while (!flag) {
            try {
                System.out.println("\nEnter a valid int: ");
                i1 = scan.nextLong();
                System.out.println("Enter another valid int: ");
                i2 = scan.nextLong();
                if(i1 > Integer.MAX_VALUE || i2 > Integer.MAX_VALUE){
                    errors.println("ERROR in sum(): One or both int larger than " + Integer.MAX_VALUE);
                    System.out.println("Integers must be < " + Integer.MAX_VALUE);
                }else if(i1 < Integer.MIN_VALUE || i2 < Integer.MIN_VALUE){
                    errors.println("ERROR in sum(): One or both int smaller than " + Integer.MIN_VALUE);
                    System.out.println("Integers must be > " + Integer.MIN_VALUE);
                }else if (i1 + i2 > Integer.MAX_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured.");
                    System.out.println("Sum of integer values too large.");
                }else if (i1 * i2 > Integer.MAX_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured.");
                    System.out.println("Product of integer values too large.");
                }else if (i1 + i2 < Integer.MIN_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured.");
                    System.out.println("Sum of integer values too small.");
                }else if (i1 * i2 < Integer.MIN_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured.");
                    System.out.println("Product of integer values too small.");
                }else{
                    flag=true;
                    results[0] = (int) (i1 + i2);
                    results[1] = (int) (i1 * i2);
                }
            } catch (Exception e) {
                errors.println("ERROR in sum(): Value Entered is not a int.");
                scan.nextLine();
            }
        }
        return (results);
  
    }

    public static void createPassword(Scanner scan) {
        String password = "";
        boolean matches = false;
        while (!matches) {
            System.out.println("\nPasswords must be at least 10 char long and contain:\n"+
                               "1 uppercase, 1 lowercase , 1 digit\n"+
                               "1 punctuation [-+_!@#$%^&*.,?]\n"+
                               "No whitespaces allowed");
            System.out.println("Enter a valid password: ");
            password = scan.nextLine();
            if (password.contains(" ")) {
                errors.println("ERROR in createPassword(): Password contains a space.");
                System.out.println("Password cannot contain a space.");
                continue;
            }
            Pattern p = Pattern.compile("(?!.*\\s)(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?]).{10,}");
            Matcher m = p.matcher(password);
            matches = m.matches();
            if (!matches) {
                errors.println("ERROR in createPassword(): Invalid Password Entered.");
                System.out.println("Password does not meet criteria.");
            }
        }
        //jBCrypt Implementation Found Here
        //http://www.mindrot.org/projects/jBCrypt/#download
        String salt = BCrypt.gensalt(12);
        String hash = BCrypt.hashpw(password, salt);
        passwordStorage.println(hash);
        passwordStorage.close();
    }

    public static void verifyPassword(Scanner scan) {
        String password,pwHash = "";
        boolean matches = false;
        while (!matches) {
            System.out.println("\nEnter a your password: ");
            password = scan.nextLine();
            if (password.contains(" ")) {
                errors.println("ERROR in verifyPassword(): Password contains a space.");
                System.out.println("Password cannot contain a space.");
                continue;
            }else{
                Scanner pwFile=null;
                try {
                    pwFile = new Scanner(new File("password.txt"));
                } catch (Exception e) {
                    System.out.println("File Not Found.");
                    errors.println("ERROR in verifyPassword(): File Not Found. ");
                    e.printStackTrace();
                }
                if (pwFile.hasNextLine()) {
                    pwHash = pwFile.nextLine();
                }
                if (BCrypt.checkpw(password, pwHash)){
                    System.out.println("Passwords match.");
                    matches=true;
                }else{
                    System.out.println("Passwords do not match.");
                    errors.println("ERROR in verifyPassword(): Passwords do not match. ");
                }
            }
        }
        
    }

    public static String readInputFile(Scanner scan, String...string) {
        String filename = "";
        boolean valid = false;
        while (!valid) {
            System.out.println("\nPlease type in a valid text file name.");
            System.out.println("Text file must end in .txt cannot have the following characters:\n" +
                               "<, >, :, \", /, \\, |, ?, *");
            filename = scan.nextLine();
            Pattern p = Pattern.compile("^(?!password\\.txt$|errorlog\\.txt$)[a-zA-Z0-9!@#$%^&()_+=-]+\\.txt$");
            Matcher m = p.matcher(filename);
            valid = m.matches();
            for (String s: string) {
                if(s != null && filename.equals(s)){
                    valid = false;
                    System.out.println("File names must be different.");
                    errors.println("ERROR in readInputFile(): File names match. ");
                }
                
                
            }
            if(string.length == 0){
                File f = new File(filename);
                if (!f.exists()) {
                    System.out.println("Text file does not exist.");
                    errors.println("ERROR in readInputFile(): Text file does not exist. "); 
                    valid = false;
                }
            }
            if (!valid) {
                System.out.println("Text file does not meet criteria please try again.");
                errors.println("ERROR in readInputFile(): Text file does not meet criteria. ");
            }
        }
        System.out.println("File name accepted.");
        return filename;
    }

    public static void writeOutput() {

    }
}



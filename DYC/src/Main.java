import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.*;
import javax.crypto.*;
import javax.crypto.spec.PBEKeySpec;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Arrays;
import java.util.HexFormat;
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
//        int[] results = sum(scan);
        //create function for input/output files
        System.out.println("reads from input file");
        String inputfile = readInputFile(scan);
        String outputfile = readInputFile(scan);
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

    public static int[] sum(Scanner scan) {
        long i1, i2 = 0;
        boolean flag = false;
        int[] results = new int[2];
        while (!flag) {
            try {
                System.out.println("Enter a valid int: ");
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
                    errors.println("ERROR in sum(): Integer Overflow Occured");
                    System.out.println("Sum of integer values too large");
                }else if (i1 * i2 > Integer.MAX_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured");
                    System.out.println("Product of integer values too large");
                }else if (i1 + i2 < Integer.MIN_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured");
                    System.out.println("Sum of integer values too small");
                }else if (i1 * i2 < Integer.MIN_VALUE) {
                    errors.println("ERROR in sum(): Integer Overflow Occured");
                    System.out.println("Product of integer values too small");
                }else{
                    flag=true;
                    results[0] = (int) (i1 + i2);
                    results[1] = (int) (i1 * i2);
                }
            } catch (Exception e) {
                errors.println("ERROR in sum(): Value Entered is not a int");
                scan.nextLine();
            }
        }
        return (results);
  
    }

    public static void createPassword(Scanner scan) throws InvalidKeySpecException, NoSuchAlgorithmException, IOException {
        String password = "";
        boolean matches = false;
        while (!matches) {
            System.out.println("Passwords must be at least 10 char long and contain:\n"+
                               "1 uppercase, 1 lowercase , 1 digit\n"+
                               "1 punctuation [-+_!@#$%^&*.,?]\n"+
                               "No whitespaces allowed");
            System.out.println("Enter a valid password: ");
            password = scan.nextLine();
            if (password.contains(" ")) {
                errors.println("ERROR in createPassword(): Password contains a space");
                System.out.println("Password cannot contain a space");
                continue;
            }
            Pattern p = Pattern.compile("(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?]).{10,}");
            Matcher m = p.matcher(password);
            matches = m.matches();
            if (!matches) {
                errors.println("ERROR in createPassword(): Invalid Password Entered");
                System.out.println("Password does not meet criteria");
            }
        }
        //PBKDF2 Implementation Found Here
        //https://www.baeldung.com/java-password-hashing
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[16];
        random.nextBytes(salt);
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 65536, 128);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        byte[] hash = factory.generateSecret(spec).getEncoded();
    }

    public static void verifyPassword(Scanner scan) {
        String password = "";
    }

    public static String readInputFile(Scanner scan) {
        String filename = "";
        boolean valid = false;
        while (!valid) {
            System.out.println("Please type in a valid text file name.");
            System.out.println("Text file must end in .txt cannot have the following characters:\n" +
                    "<, >, :, \", /, \\, |, ?, *");
            filename = scan.nextLine();
            Pattern p = Pattern.compile("^(?!password\\.txt$|errorlog\\.txt$)[a-zA-Z0-9!@#$%^&()_+=-]+\\.txt$");
            Matcher m = p.matcher(filename);
            valid = m.matches();
            if (!valid) {
                System.out.print("Text file does not meet criteria please try again.");
            }
        }
        System.out.println("NEW FILE HAS BEEN MADE LEGO");
        return filename;
    }
    public static void writeOutput() {

    }
}



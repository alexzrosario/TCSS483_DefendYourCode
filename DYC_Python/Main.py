import bcrypt
import os
import re
class Main:
    def __init__(self):
        pass
    
    def main(self):
        os.chdir('TCSS483_DefendYourCode')
        errorsLog = open('errorlog.txt', 'a')
        passwordStorage = open('password.txt', 'w+b')
        
        # Enter a first name
        firstName = self.__name(errorsLog, "first")
        # Enter a last name
        lastName = self.__name(errorsLog, "last")
        
        # Sum and Multiply two integers
        sum, prod, firstDigit, secondDigit = self.__sum(errorsLog)
        
        # Function for input/output files
        print("Now reading Input file.")
        inputFile = self.__readInputFile(errorsLog, "input")
        print("Now reading Output file.")
        outputFile = self.__readInputFile(errorsLog, "output", inputFile)
        
        # Enter password
        # Salt and Hash Password
        self.__createPassword(errorsLog, passwordStorage)
        # Verify password
        self.__verifyPassword(errorsLog, passwordStorage)
        
        contents = [firstName, lastName, sum, prod, firstDigit, secondDigit, inputFile]
        self.__writeOutput(errorsLog, contents, outputFile)
        errorsLog.close()
        passwordStorage.close()
    
    def __name(self, errorsLog, section):
        nameString = ""
        matches = False
        while not matches:
            nameString = input(f"\nEnter a valid {section} name (Start with a capital letter followed by a-z or a '-'): ")
            matches = re.match("^[A-Z][-a-z]{1,49}$", nameString)
            if not matches:
                errorsLog.write("ERROR in name(): Invalid Name Entered\n")
                print("Invalid Name Entered")
        print("Name Accepted")
        return nameString
    
    def __sum(self, errorsLog):
        i1, i2, sum, prod = 0, 0, 0, 0
        flag = False
        while not flag:
            try:
                i1 = int(input("\nEnter a valid int (Between -2147483648 and 2147483647): "))
                i2 = int(input("Enter another valid int (Between -2147483648 and 2147483647): "))
                
                if i1 > 2147483647 or i2 > 2147483647:
                    errorsLog.write("ERROR in sum(): One or both int larger than 2147483647\n")
                    print("Integers must be < 2147483647")
                elif i1 < -2147483648 or i2 < -2147483648:
                    errorsLog.write("ERROR in sum(): One or both int smaller than -2147483648\n")
                    print("Integer must be > -2147483648")
                elif i1 + i2 > 2147483647:
                    errorsLog.write("ERROR in sum(): Integer Overflow Occurred\n")
                    print("Sum of integer values too large")
                elif i1 * i2 > 2147483647:
                    errorsLog.write("ERROR in sum(): Integer Overflow Occurred\n")
                    print("Product of integer values too large")
                elif i1 + i2 < -2147483648:
                    errorsLog.write("ERROR in sum(): Integer Underflow Occurred\n")
                    print("Sum of integer values too small")
                elif i1 * i2 < -2147483648:
                    errorsLog.write("ERROR in sum(): Integer Underflow Occurred\n")
                    print("Product of integer values too small")
                else:
                    flag = True
                    sum = i1 + i2
                    prod = i1 * i2
            except:
                errorsLog.write("ERROR in sum(): Value entered is not a int\n")
                print("Input must be an integer")
        
        return sum, prod, i1, i2
    
    def __createPassword(self, errorsLog, passStor):
        passwordString = ""
        matches = False
        while not matches:
            print("\nPassword must be at least 10 characters long and contains:")
            print("at least 1 uppercase character, 1 lowercase character, 1 digit character")
            print("and 1 punctuation. No whitespaces allowed")
            passwordString = input("Enter a valid password: ")
            if passwordString.__contains__(' '):
                errorsLog.write("ERROR in createPassword(): Password contains a space\n")
                print("Password cannot contain a space")
                continue
            
            matches = re.match("(?!.*\s)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?]).{10,}", passwordString)
            if not matches:
                print("Password does not meet criteria")
                errorsLog.write("ERROR in createPassword(): Invalid Password Entered\n")
        
        passwordString = passwordString.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwordString, salt)
        print("Password Accepted!")
        passStor.write(hashed)
        passStor.flush()
    
    def __verifyPassword(self, errorsLog, hash):
        passwordString = ""
        matches = False
        
        while not matches:
            passwordString = input("\nVerify your password: ")
            
            try:
                hash.seek(0)
                currPass = hash.readlines()[0]
            except:
                print("File Not Found")
                errorsLog.write("ERROR in verifyPassword(): File Not Found\n")
                return

            passwordString = passwordString.encode('utf-8')
            hashed = bcrypt.hashpw(passwordString, currPass)
            
            if hashed == currPass:
                matches = True
                print("Password matches")
            else:
                print("Password does not match")
                errorsLog.write("ERROR in verifyPassword(): Passwords do not match.\n")
                
    def __readInputFile(self, errorsLog, section, *string):
        fileName = ""
        valid = False
        while not valid:
            print('\nText file must end in .txt and cannot have the following characters:')
            print('<, >, :, \", /, \\, |, ?, *')
            fileName = input(f"Please type in a valid {section} text file name: ")
            valid = re.match("^(?!password\.txt$|errorlog\.txt$)[a-zA-Z0-9!@#$%^&()_+=-]+\.txt$", fileName)

            for i in string:
                if i != None and fileName == i:
                    print("File names must be different.")
                    errorsLog.write("ERROR in readInputFile(): Text file does not exist.\n")
                    valid = False
                    
            if len(string) == 0:
                if not os.path.isfile(fileName):
                    print("Text file does not exist.")
                    errorsLog.write("ERROR in readInputFile(): Text file does not exist.\n")
                    valid = False
            
            if not valid:
                print("Text file does not meet criteria! Please try again!")
                errorsLog.write("ERROR in getInputFile(): Input File Does Not Meet Criteria\n")
        
        print("File name accepted")
        return fileName
    
    def __writeOutput(self, errorsLog, contents, outputFile):
        myFile = outputFile
        string = ""
        try:
            if not os.path.exists(outputFile):
                with open(outputFile, 'w+'):
                    pass
                print(f"\nFile created: {myFile}")
            else:
                print("\nFile already exists. Overwriting file.")
            
            writer = open(myFile, 'w')
            
            string += f"First Name: {contents[0]}\n"
            string += f"Last Name: {contents[1]}\n"
            string += f"First Integer: {contents[4]}\n"
            string += f"Second Integer: {contents[5]}\n"
            string += f"Sum: {contents[2]}\n"
            string += f"Product: {contents[3]}\n"
            string += f"Input File Name: {contents[6]}\n"
            inputFileContent = self.__getInputFile(errorsLog, contents[6])
            string += f"Input File Contents:\n{inputFileContent}"
            writer.write(string)
            writer.close()
            print("Output File Written")
        except:
            print("Error has occurred printing message")
            errorsLog.write("ERROR in writeOutput(): File Not Found\n")
            
    def __getInputFile(self, errorsLog, input):
        fileContent = ""
        try:
            with open(input, 'r') as file:
                for line in file:
                    fileContent += line
        except:
            print("Cannot get input from file")
            errorsLog.write("ERROR in getInputFile(): Cannot get input from file\n")
            
        return fileContent
                    
if __name__ == "__main__":
    m = Main()
    m.main()
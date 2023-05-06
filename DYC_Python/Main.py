import bcrypt
import os
import re
class Main:
    def __init__(self):
        pass
    
    def main(self):
        # os.chdir(os.path.dirname(__file__))
        # os.chdir("/..")
        os.chdir('TCSS483_DefendYourCode')
        # print(os.getcwd()) 
        errorsLog = open('./errorlog.txt', 'a')
        passwordStorage = open('./password.txt', 'w+b')
        
        # Enter a first name
        firstName = self.__name(errorsLog)
        # Enter a last name
        lastName = self.__name(errorsLog)
        
        # Sum and Multiply two integers
        sum, prod, firstDigit, secondDigit = self.__sum(errorsLog)
        
        # Function for input/output files
        inputFile = self.__readInputFile(errorsLog)
        outputFile = self.__readInputFile(errorsLog, inputFile)
        
        # Enter password
        # Salt and Hash Password
        self.__createPassword(errorsLog, passwordStorage)
        # Verify password
        self.__verifyPassword(errorsLog, passwordStorage)
        
        contents = [firstName, lastName, sum, prod, firstDigit, secondDigit, inputFile]
        self.__writeOutput(errorsLog, contents, outputFile)
        errorsLog.close()
        passwordStorage.close()
    
    def __name(self, errorsLog):
        nameString = ""
        matches = False
        while not matches:
            nameString = input("Enter a valid name (Start with a capital letter followed by a-z or a '-'): ")
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
                i1 = int(input("Enter a valid int (Between -2147483648 and 2147483647): "))
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
        
        return sum, prod, i1, i2
    
    def __createPassword(self, errorsLog, passStor):
        passwordString = ""
        matches = False
        while not matches:
            print("Password must be at least 10 characters long and contains:")
            print("at least 1 uppercase character, 1 lowercase character, 1 digit character")
            print("and 1 punctuation. No whitespaces allowed")
            passwordString = input("Enter a valid password: ")
            # if passwordString.__contains__(' '):
            #     errorsLog.write("ERROR in createPassword(): Password contains a space\n")
            #     print("Password cannot contain a space")
            #     continue
            
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
            passwordString = input("Verify your password: ")
            
            try:
                hash.seek(0)
                currPass = hash.readlines()[0]
            except:
                print("File Not Found")
                errorsLog.write("ERROR in verifyPassword(): File Not Found")
                return

            passwordString = passwordString.encode('utf-8')
            hashed = bcrypt.hashpw(passwordString, currPass)
            
            if hashed == currPass:
                matches = True
                print("Password matches")
            else:
                print("Password does not match")
                errorsLog.write("ERROR in verifyPassword(): Passwords do not match.")
                
    def __readInputFile(self, errorsLog, *string):
        fileName = ""
        valid = False
        while not valid:
            print('Text file must end in .txt and cannot have the following characters:')
            print('<, >, :, \", /, \\, |, ?, *')
            fileName = input("Please type in a valid text file name: ")
            valid = re.match("^(?!password\.txt$|errorlog\.txt$)[a-zA-Z0-9!@#$%^&()_+=-]+\.txt$", fileName)

            for i in string:
                if i != None and fileName == i:
                    print("File names must be different.")
                    errorsLog.write("ERROR in readInputFile(): Text file does not exist.")
                    valid = False
                    
            if len(string) == 0:
                if not os.path.isfile(fileName):
                    print("Text file does not exist.")
                    errorsLog.write("ERROR in readInputFile(): Text file does not exist.")
                    valid = False
            
            if not valid:
                print("Text file does not meet criteria! Please try again!")
                errorsLog.write("ERROR in getInputFile(): Input File Does Not Meet Criteria\n")
        
        print("File name accepted")
        return fileName
    
    def __writeOutput(self, errorsLog, contents, outputFile):
        myFile = None
        try:
            if not os.path.exists(outputFile):
                myFile = open(outputFile, 'w+')
                print(f"File created: {myFile.name}")
            else:
                print("File already exists.")
            myFile.close()
            
            writer = open(myFile, 'w')
            writer.write(f"First Name: {contents[0]}\n")
            writer.write(f"Last Name: {contents[1]}\n")
            writer.write(f"First Integer: {contents[4]}\n")
            writer.write(f"Second Integer: {contents[5]}\n")
            writer.write(f"Sum: {contents[2]}\n")
            writer.write(f"Product: {contents[3]}\n")
            writer.write(f"Input File Name: {contents[6]}\n")
            string = self.__getInputFile(errorsLog, contents[6])
            writer.write(f"Input File Contents:\n{string}")
            writer.close()
        except:
            print("Errot has occurred printing message")
            errorsLog.write("ERROR in writeOutput(): File Not Found")
            
    def __getInputFile(self, errorsLog, input):
        fileContent = ""
        try:
            with open(input, 'r') as file:
                for line in file:
                    fileContent += line
                    print(line)
        except:
            print("Cannot get input from file")
            errorsLog.write("ERROR in getInputFile(): Cannot get input from file")
            
        return fileContent
                    
if __name__ == "__main__":
    m = Main()
    m.main()
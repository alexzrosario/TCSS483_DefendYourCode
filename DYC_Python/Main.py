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
        # firstName = self.__name(errorsLog)
        # file.write(firstName + "\n")
        # Enter a last name
        # lastName = self.__name(errorsLog)
        
        # Sum two integers
        # sum, prod = self.__sum(errorsLog)
        # print(sum)
        # print(prod)
        
        inputFile = self.__getInputFile(errorsLog)
        print()
        outputFile = self.__getInputFile(errorsLog, inputFile)
        print()
        
        # out = self.__getOutputFile(errorsLog)
        # outputFile = open(out, 'w')
        
        #with open('./password.txt', 'w+b') as passwordStorage:
        # Enter password
        # self.__createPassword(errorsLog, passwordStorage)
        print()
        # Verify password
        # verifyPassword = self.__verifyPassword(errorsLog, passwordStorage)
        print()
        
        # contents = [firstName, lastName, sum, prod, inputFile]
        contents = None
        writeOutput = self.__writeOutputFile(errorsLog, outputFile, contents)
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
        
        return sum, prod
    
    def __getInputFile(self, errorsLog, *string):
        inputFile = ""
        valid = False
        while not valid:
            print('Text file must end in .txt and cannot have the following characters:')
            print('<, >, :, \", /, \\, |, ?, *')
            inputFile = input("Please type in a valid text file name: ")
            valid = re.match("^(?!password\.txt$|errorlog\.txt$)[a-zA-Z0-9!@#$%^&()_+=-]+\.txt$", inputFile)
            
            # print(string)

            for i in string:
                if i != None and inputFile == i:
                    valid = False
                    
            # print(string[0])
            # if string[0] != None and inputFile.equals(string[0]):
            #     valid = False
            
            if not valid:
                errorsLog.write("ERROR in getInputFile(): Input File Does Not Meet Criteria\n")
                print("Text file does not meet criteria! Please try again!\n")
        return inputFile
    
    def __writeOutputFile(self, errorsLog, outputFile, contents):
        try:
            openOutputFile = open(outputFile, 'w')
        except:
            errorsLog.write("ERROR in writeOutputFile(): File Not Found")
            print("File Not Found")
            return
        
        for i in contents:
            openOutputFile.write(i + "\n")
            
    
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
                errorsLog.write("ERROR in createPassword(): Invalid Password Entered\n")
                print("Password does not meet criteria")
        
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
                errorsLog.write("ERROR in verifyPassword(): File Not Found")
                print("File Not Found")
                return

            passwordString = passwordString.encode('utf-8')
            hashed = bcrypt.hashpw(passwordString, currPass)
            
            if hashed == currPass:
                matches = True
                print("Password matches")
            else:
                errorsLog.write("ERROR in verifyPassword(): Passwords do not match.")
                print("Password does not match")

if __name__ == "__main__":
    m = Main()
    m.main()
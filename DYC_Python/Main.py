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
        passwordStorage = "./password.txt"
        
        errorsFile = './errorlog.txt'
        
        errorsLog = open(errorsFile, 'a')
        sample = open(passwordStorage, 'ab')
        # Enter a first name
        # firstName = self.__name(errorsLog)
        # file.write(firstName + "\n")
        # Enter a last name
        # lastName = self.__name(errorsLog)
        
        # Sum two integers
        # sum = self.__sum(errorsLog)
        # print(sum)
        
        # Enter password
        password = self.__createPassword(errorsLog)
        sample.write(password)
        sample.write('\n'.encode('utf-8'))
        errorsLog.close()
        sample.close()
    
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
        i1, i2, sum = 0, 0, 0
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
                    print("Integer values too large")
                elif i1 + i2 < -2147483648:
                    errorsLog.write("ERROR in sum(): Integer Underflow Occurred\n")
                    print("Integer value too small")
                else:
                    flag = True
                    sum = i1 + i2
            except:
                errorsLog.write("ERROR in sum(): Value entered is not a int\n")
        
        return sum
    
    def __inputFile(self):
        pass
    
    def __outputFile(self):
        pass
    
    def __createPassword(self, errorsLog):
        passwordString = ""
        matches = False
        while not matches:
            print("Passwords must be at least 10 characters long and contains:")
            print("at least 1 uppercase character, 1 lowercase character, 1 digit character")
            print("and 1 punctuation. No whitespaces allowed")
            passwordString = input("Enter a valid password: ")
            if passwordString.__contains__(' '):
                errorsLog.write("ERROR in createPassword(): Password contains a space\n")
                print("Password cannot contain a space")
                continue
            
            matches = re.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?]).{10,}", passwordString)
            if not matches:
                errorsLog.write("ERROR in createPassword(): Invalid Password Entered\n")
                print("Password does not meet criteria")
        
        passwordString = passwordString.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwordString, salt)
        print(hashed)
        return hashed
    
    def __verifyPassword(self, errorsLog):
        pass

if __name__ == "__main__":
    m = Main()
    m.main()
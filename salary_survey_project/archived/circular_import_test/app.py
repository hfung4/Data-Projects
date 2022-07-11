import survey
import survey.config.core



def main():
    package_root_path = survey.config.core.PACKAGE_ROOT
    print(f"PACKAGE_ROOT called from main function is : {package_root_path}")

if (__name__=="__main__"):
    main()
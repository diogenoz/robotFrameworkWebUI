*** Settings ***
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library SeleniumLibrary
Library ScreenCapLibrary
Resource keywords/keyword1/keyword1.robot  
*** Test Cases ***
Valid Login
    Open Browser    ${ENV_SERVER}    ${BROWSER}
    Take Screenshot    name=screenshot1  format=jpg  quality=0
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Close Browser


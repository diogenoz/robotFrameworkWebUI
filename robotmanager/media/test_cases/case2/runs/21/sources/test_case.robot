*** Settings ***
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

Resource /media/keywords/keyword1/keyword1.robot  
*** Test Cases ***
Valid Login
    Open Browser    ${ENV_SERVER}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Close Browser


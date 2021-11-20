Resource keywords/keyword1/keyword1.robot  
*** Settings ***
Resource keywords/keyword1/keyword1.robot  
...
Resource keywords/keyword1/keyword1.robot  
...               The system specific keywords created here form our own
Resource keywords/keyword1/keyword1.robot  
...               domain specific language. They utilize keywords provided
Resource keywords/keyword1/keyword1.robot  
...               by the imported SeleniumLibrary.
Resource keywords/keyword1/keyword1.robot  
Library           SeleniumLibrary
Resource keywords/keyword1/keyword1.robot  

*** Test Cases ***Valid Login    Open Browser    ${ENV_SERVER}    ${BROWSER}
Resource keywords/keyword1/keyword1.robot  
    Maximize Browser Window
Resource keywords/keyword1/keyword1.robot  
    Set Selenium Speed    ${DELAY}
Resource keywords/keyword1/keyword1.robot  
    Close Browser
Resource keywords/keyword1/keyword1.robot  


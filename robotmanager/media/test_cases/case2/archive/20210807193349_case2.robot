Resource keywords/keyword1/keyword1.robot  
Resource keywords/keyword1/keyword1.robot  *** Settings ***Documentation     A resource file with reusable keywords and variables.......               The system specific keywords created here form our own...               domain specific language. They utilize keywords provided...               by the imported SeleniumLibrary.Library           SeleniumLibrary*** Test Cases ***Valid Login    Open Browser    ${ENV_SERVER}    ${BROWSER}    Maximize Browser Window    Set Selenium Speed    ${DELAY}    Close Browser
Resource keywords/keyword1/keyword1.robot  
*** Settings ***......               The system specific keywords created here form our own...               domain specific language. They utilize keywords provided...               by the imported SeleniumLibrary.*** Test Cases ***Valid Login    Open Browser    ${SERVER}    ${BROWSER}    Maximize Browser Window    Set Selenium Speed    ${DELAY}    Close Browser
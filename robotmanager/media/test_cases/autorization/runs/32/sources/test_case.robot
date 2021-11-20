*** Settings ***
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary
Library           ScreenCapLibrary

*** Test Cases ***
Valid Login
    Open Browser    ${ENV_SERVER}    ${BROWSER}
    Input Text     id:user  ${ENV_USER}
    Input Text     id:pass    ${ENV_PASSWORD}
    Click Button    id:loginHiddenButton
    Maximize Browser Window
    Take Screenshot 
    Set Selenium Speed    ${DELAY}
    Close Browser


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
    Click Button     //html/body/div/form/table/tbody/tr[1]/td[2]/a
    Input Text     id:userNameInput  ${ENV_USER}
    Input Text     id:passwordInput    ${ENV_PASSWORD}
    Click Button    id:loginForm
    Maximize Browser Window
    Take Screenshot 
    Set Selenium Speed    ${DELAY}
    Close Browser


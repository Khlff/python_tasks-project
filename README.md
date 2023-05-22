* ### Task name: HTTP(S) Webserver
* ### This is an http server that operates in two modes:
    #### 1)Accepts the URL of the site in any encoding and saves all images from it. A gui client is written for this mode. 
    #### 2)Accepts the URL of the site in any encoding and sends the html of this site with the cut-out advertisement.

## Installation
### To install the application, you need to clone the repository:
```
git clone https://github.com/Khlff/python_tasks-project.git
cd python_tasks-project
```
          
* ### Launching locally:
  ```
  python -m venv venv;
  ```
  Linux:
      ```
    venv/bin/activate
      ```
  Windows:
      ```
    venv/Scripts/activate
      ```
  ```
  pip install -r requirements.txt;
  python server.py -path -mode [--port] [--help];
  ```

##  
###  Made by Nikita Khlopunov and Dmitry Kryuchkov

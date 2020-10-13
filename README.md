# CUGBAutoSubmit
An automatic script for CUGB's JailBreak application  
中国地质大学（北京）备案制出入校自动申请脚本  
***免责声明（Disclaimer）：使用该脚本而可能引起的法律责任和学校追究等责任由使用者个人承担，与开发者无关。本项目仅供参考学习之用，为了您和他人的健康着想，请如实填报出校信息！***
## UPDATES
### **2020/10/13 - This update version resolved:**  
- A new feature for the site that uses https and CAS Auth.  
- Now you can get the status of application after about 5 minutes.  
## REQUIREMENTS
pip install requests  
pip install bs4  
pip install esprima  
## USER MANNUL (Updated on 2020/10/13)
### Modify
>main.py:  
>>  
>>line 51:  ```uname = ''  # Input your Student Number, e.g. 2005190001```  
>>line 52:  ```upwd = ''  # Input your portals' password, e.g. 123456```  
>>**For example:  
>>'200120000X' (Your Student Number), '123456' (The Last Six Number of Your ID Card)**  
>>  
>>line 119:  ``` ...,"c1":"182XXXX1234","c2":"临时出校","c17":"学19楼","c18":"110X",...```  
>>**For example:  
>>'182XXXX1234' (Your telephone number), '学19楼' (Your building number) & '110X'(Your room number)**  
>>  
>>line 123:  ``` 'uploadFileStr': '''{"c16":[]}''',```  
>>**Notice:  
>>The value of "uploadFileStr" need to be captured from Fiddler or Charles when you submit the information manually**  
>>  
>iMessage.py:
>>line 9:  ```"from": "example@example.com",``` **e.g. username(send_from)@163.com**  
>>line 10:  ```"to": "example@example.com",``` **e.g. username(send_to)@gmail.com**  
>>line 11:  ```"hostname": "smtp.example.com",``` **e.g. smtp.163.com**  
>>line 12:  ```"username": "example@example.com",``` **e.g. username(send_from)@163.com**  
>>line 13:  ```"password": "******",``` **e.g. 163mail API key**
>>  
### Run
WINDOWS:  ```python main.py```

Linux:  ```python3 main.py``` or ***(Recommend)*** set a crontab  ```1 16 * * * python3 /usr/local/src/CUGBAutoSubmit/main.py```
## STATEMENT
Some core code is from the author cmzz on CSDN (url: https://blog.csdn.net/qq_40965177/article/details/105986587)

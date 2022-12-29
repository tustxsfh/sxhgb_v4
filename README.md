# sxhgb_v4 山西好干部在线学习

## 学习环境

- Python 3.8 
- selenium 4.7.2
- Chrome 108
- chromedriver
- tesseract-ocr
- 其他依赖详见 requriments.txt

### 如需在docker中运行，请移步 [sxhgb_docker](https://github.com/tustxsfh/sxhgb_docker)

## 学习步骤

1. 安装 Python
2. 安装 tesseract-ocr
3. 下载本项目 
```
git clone https://github.com/tustxsfh/sxhgb_v4.git
```
4. 安装依赖
 ```python
 pip -r install requriments.txt
 ```
5. 运行
```python
python main.py
```
6. 按提示填入帐号、密码、学习时长等信息

## api 说明

  
- find_peixun() 下载专题培训url

- find_course() 下载课程url

- keicheng() 课程按顺序学习

- kecheng_random() 课程随机学习

- peixun() 专题培训按顺序学习

- peixun_random() 专题培训随机学习


## 注意事项

- find_peixun()    find_course() 只在需要更新学习内容时使用，取消注释即可

- keicheng()    kecheng_random()    peixun()    peixun_random()     使用一个即可，其余注释掉。  

- 默认使用  kecheng_random() 课程按顺序学习


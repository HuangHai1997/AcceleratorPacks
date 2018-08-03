import os
import re
import time
import xml.etree.ElementTree as ET


# 加载当前页面并且保存至目录D:/TestAboutAndroid中 命名方式为name.xml 其中name为用户输入函数的参数
def LoadPage(name):
    os.popen("adb shell uiautomator dump /data/local/tmp/{}.xml".format(name))
    os.popen("adb pull /data/local/tmp/{}.xml ".format(name) + "D:/TestAboutAndroid")
    time.sleep(2)               # 加入time.sleep 因为程序执行到保存xml需要一定的时间


# 解析目标页面TargetPage 中的目标位置TargetApp 最后return该位置的坐标值
def ParsePage(TargetPage,TargetApp):
    tree = ET.parse('{}.xml'.format(TargetPage))    # 加载文档，并进行解析
    root=tree.getroot()                         # 获取根元素
    time.sleep(0.5)
    # 遍历所有Tag为node的节点 ，如果该节点存在一个attrib：text且text对应的值为计算器 则保存
    for neighbor in root.iter('node'):
        # print(neighbor.attrib)
        # print(neighbor.attrib["text"])
        # print(neighbor.attrib.get("text"))
        # 由于某些页面按钮名称存储在content-desc 中 所以添加attrib['content-desc']
        # backup：if neighbor.attrib["text"]==TargetApp:
        if neighbor.attrib["text"]==TargetApp or neighbor.attrib["content-desc"]==TargetApp:
            dict=neighbor.attrib
            bounds=dict['bounds']   #获得的bounds的属性为str

            # 得到一个内含元组的列表
            out=re.findall("\[(\d{1,4}),(\d{1,4})\]\[(\d{1,4}),(\d{1,4})\]",bounds,)
            # 将out重定义为内置的元组 points    元组内每一个数字都是str
            points=out[0]
            # 定义待点击的位置坐标
            x = int(points[0]) + (int(points[2]) - int(points[0])) / 2
            y = int(points[1]) + (int(points[3]) - int(points[1])) / 2
            return x,y


def AutoClick(x,y):
    os.system("adb shell input tap {} {}".format(x,y))
    time.sleep(0.5)

# 1.解析页面 2.获取坐标 3.点击坐标
# a 代表解析页面序号    b代表页面内要点击的位置名称
def Operate(a,b,c=0):
    LoadPage(a)
    time.sleep(c)
    try:
        x1,y1=ParsePage(a,b)
    except:
        print("加载过慢！请稍等！")
        time.sleep(2)
        x1,y1=ParsePage(a,b)
    AutoClick(x1,y1)


if __name__ == '__main__':
    Operate(1,"Undefined。")
    Operate(2,"携程订酒店机票火车票汽车票门票")
    time.sleep(11)
    Operate(3,"去抢火车票")          # 设置额外的time.sleep时间 因为小程序加载过慢















"""
# 测试在ParsePage函数中的{}.xml是否能正确有效的打开目标文件

f=open("1.xml",encoding="utf-8")
i=f.read()
print(i)
f.close()
"""

"""
#以”计算器“为例子运行ParsePage 得到的结果：

{'index': '4', 'text': '计算器', 'resource-id': '', 'class': 'android.widget.TextView', 'package': 'com.htc.launcher', 
'content-desc': '', 'checkable': 'false', 'checked': 'false', 'clickable': 'true', 'enabled': 'true',
 'focusable': 'true', 'focused': 'false', 'scrollable': 'false', 'long-clickable': 'true', 
 'password': 'false', 'selected': 'false', 'bounds': '[283,369][436,556]'}

"""
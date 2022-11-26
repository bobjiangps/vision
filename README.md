# vision
UI auto test framework based on YOLO to recognize elements, less code, less maintenance, cross platform, cross project / 基于YOLO的UI层自动化测试框架, 可识别控件类型，减少代码和维护，一定程度上跨平台跨项目

---
Run command to see how to run web test for stackoverflow site, without xpath / id / name, just define what you see:

运行如下命令来查看在amazon网站上执行web自动化的效果，不用写xpath之类的，只描述人眼看到的即可:
>* python main.py -e QA -t test_ai_login -b Chrome

---
the model is trained by yolov5: https://github.com/ultralytics/yolov5
there are some issues when use .onnx file convert from .pt file. So load pt model directly instead of opencv although opencv would be better.

auto test on any UI layer: web, desktop, mobile app.

no need to define xpath, id, name and so on.

no need to update script if your product has redesigned UI.

for example, the login function works on web, the same code also works on mobile app without change. (depend on the training dataset)

not testing the html nodes, but testing like human: I see there is email text field, I input my email. I see there are continue button and back button, I click the continue button to next page, I can see and check how the page displays. 

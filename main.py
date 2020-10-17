import sensor, time, image, pyb
from pyb import Pin

# 相机参数设置
sensor.reset() # 初始化相机
sensor.set_pixformat(sensor.GRAYSCALE) # 设置灰度像素模式，每个像素8bit
sensor.set_framesize(sensor.B128X128) # 设置图像大小，用于帧差异
sensor.set_windowing((92,112)) # 设置窗口ROI
sensor.skip_frames(10) # 跳过一些帧，等待感光元件变稳定

# 降低环境因素的影响
sensor.set_auto_gain(True) # 开启自动增益
sensor.set_auto_whitebal(True) # 开启自动白平衡
sensor.set_auto_exposure(True) # 开启自动曝光


# 定义IO口
# 输入引脚
p_in0 = Pin('P0', Pin.IN, Pin.PULL_UP) # 设置P0为“按键1”输入引脚，并开启上拉电阻
p_in1 = Pin('P1', Pin.IN, Pin.PULL_UP) # 设置P1为“按键2”输入引脚，并开启上拉电阻
p_in2 = Pin('P2', Pin.IN, Pin.PULL_UP) # 设置P2为“按键3”输入引脚，并开启上拉电阻
p_in3 = Pin('P3', Pin.IN, Pin.PULL_UP) # 设置P3为“按键4”输入引脚，并开启上拉电阻
# 输出引脚
RED_LED_PIN = 1 # 红色LED输出引脚
GREEN_LED_PIN = 2 # 绿色LED输出引脚
BLUE_LED_PIN = 3 # 蓝色LED输出引脚
p_out0 = Pin('P4', Pin.OUT_PP) # 设置p_out为输出引脚
p_out1 = Pin('P5', Pin.OUT_PP) # 设置p_out为输出引脚
p_out2 = Pin('P6', Pin.OUT_PP) # 设置p_out为输出引脚
p_out3 = Pin('P7', Pin.OUT_PP) # 设置p_out为输出引脚

# 定义全局变量
face_result = 0 #身份识别结果
mask_result = 0 #口罩判别结果
iden_out_result = 0 #学习后识别结果

# 功能部分
while(True):
    # 读取输入引脚数值
    value0 = p_in0.value() # 读入p_in0引脚的值
    value1 = p_in1.value() # 读入p_in1引脚的值
    value2 = p_in2.value() # 读入p_in2引脚的值
    value3 = p_in3.value() # 读入p_in3引脚的值

    # 定义变量
    face_num0 = 0
    face_num1 = 0
    face_num2 = 0

    mask_num0 = 0
    mask_num1 = 0
    mask_num2 = 0

    iden_in_num0 = 0
    iden_in_num1 = 0
    iden_in_num2 = 0

    iden_out_num0 = 0
    iden_out_num1 = 0
    iden_out_num2 = 0

    # 判断输入引脚数值
    if value2 == 0: # 第3个按键按下时，开启学习模式
        print("开启学习模式")
        p_out0.low() # 0010 第3个灯亮 表示第3个按键被按下
        p_out1.low()
        p_out2.high()
        p_out3.low()

        sensor.skip_frames(time = 500) # 延时0.5s

        p_out0.low() # 将4个输出IO口全部置低电平（不然灯会一直亮着）
        p_out1.low()
        p_out2.low()
        p_out3.low()

        if value0 == 0: # 第1个按键按下时，学习第1个人
            print("正在学习第1个人脸")

            #设置识别数量
            iden_in_num0 = 1 # 设置被拍摄者序号，第一个人的图片保存到i1文件夹，第二个人的图片保存到i2文件夹，以此类推。每次更换拍摄者时，修改num值
            n = 5 # 拍摄照片数量

            while(n):
                pyb.LED(RED_LED_PIN).on() # 红灯亮

                sensor.skip_frames(time = 3000) # 延时3s
                
                pyb.LED(RED_LED_PIN).off() # 红灯灭
                pyb.LED(BLUE_LED_PIN).on() # 蓝灯亮

                # 保存截取到的图片到SD卡
                print(n)
                sensor.snapshot().save("identify/i%s/%s.pgm" % (iden_in_num0, n) ) # 此处会被保存于"identify/i1/"

                n -= 1 

                pyb.LED(BLUE_LED_PIN).off() # 蓝灯灭
            break
        if value1 == 0: # 第2个按键按下时，学习第2个人
            print("正在学习第2个人脸")
            iden_in_num1 = 2 # 设置被拍摄者序号，第一个人的图片保存到i1文件夹，第二个人的图片保存到i2文件夹，以此类推。每次更换拍摄者时，修改num值
            n = 5 # 拍摄照片数量
            while(n):
                pyb.LED(RED_LED_PIN).on() # 红灯亮

                sensor.skip_frames(time = 3000) # 延时3s

                pyb.LED(RED_LED_PIN).off() # 红灯灭
                pyb.LED(BLUE_LED_PIN).on() # 蓝灯亮

                # 保存截取到的图片到SD卡
                print(n)
                sensor.snapshot().save("identify/i%s/%s.pgm" % (iden_in_num1, n) ) # 此处会被保存于"identify/i2/"

                n -= 1

                pyb.LED(BLUE_LED_PIN).off() # 蓝灯灭
            break
        if value3 == 0: # 第4个按键按下时，学习第3个人（因为第3个按键需长按，保持P6在低电平状态，才能执行之后的程序）
            print("正在学习第3个人脸")
            iden_in_num2 = 3 # 设置被拍摄者序号，第一个人的图片保存到i1文件夹，第二个人的图片保存到i2文件夹，以此类推。每次更换拍摄者时，修改num值
            n = 5 # 拍摄照片数量
            while(n):
                pyb.LED(RED_LED_PIN).on()  # 红灯亮

                sensor.skip_frames(time = 3000) # 延时3s

                pyb.LED(RED_LED_PIN).off() # 红灯灭
                pyb.LED(BLUE_LED_PIN).on() # 蓝灯亮

                # 保存截取到的图片到SD卡
                print(n)
                sensor.snapshot().save("identify/i%s/%s.pgm" % (iden_in_num2, n) ) # 此处会被保存于"identify/i3/"
                n -= 1

                pyb.LED(BLUE_LED_PIN).off() # 蓝灯灭
            break

    if value3 == 0: # 第4个按键单独按下时，开启学习后识别模式
        print("正在开启学习后识别模式")
        p_out0.low() # 0001 第4个灯亮 表示第4个按键被按下
        p_out1.low()
        p_out2.low()
        p_out3.high()

        sensor.skip_frames(time = 500) #延时0.5s

        p_out0.low() # 将4个输出IO口全部置低电平
        p_out1.low()
        p_out2.low()
        p_out3.low()

        #设置样本数量
        NUM_SUBJECTS = 3 # 图像库总人数
        NUM_SUBJECTS_IMGS = 5 # 样本图片数量

        for iden in range(3): # 循环拍摄3次样本图片，进行比对，输出出现次数最多的结果
            # 拍摄当前人脸
            sensor.skip_frames(time = 3000) # 等待3s

            img = sensor.snapshot() # 拍照

            d0 = img.find_lbp((11,14,70,84)) # 当前拍摄人脸的lbp特征，将识别ROI区域往内缩小1/8，避免一定程度上背景带来的影响
            img = None
            pmin = 999999 # pmin为最小特征差异度
            iden_out_num=0

            def min(pmin, a, s): # 确保几次循环后pmin还是最小特征差异度，a代表dist/NUM_SUBJECTS_IMGS
                global iden_out_num
                if a<pmin:
                    pmin=a
                    iden_out_num=s
                return pmin

            for s in range(1, NUM_SUBJECTS+1):
                dist = 0
                for i in range(2, NUM_SUBJECTS_IMGS+1):
                    img = image.Image("identify/i%s/%s.pgm"%(s, i))
                    d1 = img.find_lbp((11,14,70,84)) # d1为第s文件夹中的第i张图片的lbp特征，识别ROI区域往内缩小1/8
                    dist += image.match_descriptor(d0, d1) # 计算d0 d1即样本图像与被检测人脸的特征差异度。
                print("第%d个的特征差异度是: %d"%(s, dist/NUM_SUBJECTS_IMGS)) # 输出当前特征差异度，方便在串口终端显示数据
                pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s) # 特征差异度越小，被检测人脸与此样本更相似更匹配。
                print(pmin)

            # 按照循环次数，将每次识别后的结果存入，共3次
            if iden == 0:
                iden_out_num0 = iden_out_num
                print("第%d次:%d"%(iden+1,iden_out_num0))
            if iden == 1:
                iden_out_num1 = iden_out_num
                print("第%d次:%d"%(iden+1,iden_out_num1))
            if iden == 2:
                iden_out_num2 = iden_out_num
                print("第%d次:%d"%(iden+1,iden_out_num2))

            pyb.LED(BLUE_LED_PIN).on() # 蓝灯亮
            sensor.skip_frames(time = 50) # 等待0.05s
            pyb.LED(BLUE_LED_PIN).off() # 蓝灯灭

        # 在此处对3次输出结果进行比较，输出出现次数最多的那个结果。如果三个分别为不同结果，则报错。
        if iden_out_num0 == iden_out_num1 == iden_out_num2:
            print("结果是：",iden_out_num0)
            iden_out_result = iden_out_num0
        else:
            if iden_out_num0 == iden_out_num1:
                print("结果是：",iden_out_num0)
                iden_out_result = iden_out_num0
            if iden_out_num0 == iden_out_num2:
                print("结果是：",iden_out_num0)
                iden_out_result = iden_out_num0
            if iden_out_num1 == iden_out_num2:
                print("结果是：",iden_out_num1)
                iden_out_result = iden_out_num1
            #else: #不知道为什么有时候有相同结果时也会报错，故此处屏蔽该段代码，下同
             #   print("error")
              #  iden_out_result = 15



    if value0 == 0: # 第1个按键单独按下时，开启身份识别模式
        print("正在开启身份识别模式")
        p_out0.high() # 0001 第1个灯亮 表示第1个按键被按下
        p_out1.low()
        p_out2.low()
        p_out3.low()
        
        sensor.skip_frames(time = 500) # 延时0.5s
        
        p_out0.low() # 将4个输出IO口全部置低电平
        p_out1.low()
        p_out2.low()
        p_out3.low()
        
        #设置样本数量
        NUM_SUBJECTS = 3 # 图像库总人数
        NUM_SUBJECTS_IMGS = 5 # 样本图片数量

        for face in range(3):
            # 拍摄当前人脸
            sensor.skip_frames(time = 3000) # 等待3s

            img = sensor.snapshot() # 拍照

            d0 = img.find_lbp((11,14,70,84)) # 当前拍摄人脸的lbp特征，将识别ROI区域往内缩小1/8

            img = None
            pmin = 999999 # pmin为最小特征差异度
            face_num=0

            def min(pmin, a, s): # 确保几次循环后pmin还是最小特征差异度，a代表dist/NUM_SUBJECTS_IMGS
                global face_num
                if a<pmin:
                    pmin=a
                    face_num=s
                return pmin

            for s in range(1, NUM_SUBJECTS+1):
                dist = 0
                for i in range(2, NUM_SUBJECTS_IMGS+1):
                    img = image.Image("face/f%d/%d.pgm"%(s, i))
                    d1 = img.find_lbp((11,14,70,84)) # d1为第s文件夹中的第i张图片的lbp特征，识别ROI区域往内缩小1/8
                    dist += image.match_descriptor(d0, d1) # 计算d0 d1即样本图像与被检测人脸的特征差异度。
                print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS)) # 输出当前特征差异度，方便在串口终端显示数据
                pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s) # 特征差异度越小，被检测人脸与此样本更相似更匹配。
                print(pmin)
           
            # 按照循环次数，将每次识别后的结果存入，共3次               
            if face == 0:
                face_num0 = face_num
                print("第%d次:%d"%(face+1,face_num0))
            if face == 1:
                face_num1 = face_num
                print("第%d次:%d"%(face+1,face_num1))
            if face == 2:
                face_num2 = face_num
                print("第%d次:%d"%(face+1,face_num2))

            pyb.LED(RED_LED_PIN).on() # 红灯亮
            sensor.skip_frames(time = 50) # 等待0.05s
            pyb.LED(RED_LED_PIN).off() # 红灯灭
       
        # 在此处对3次输出结果进行比较，输出出现次数最多的那个结果。如果三个分别为不同结果，则报错。
        if face_num0 == face_num1 == face_num2:
            print("结果是：",face_num0)
            face_result = face_num0
        else:
            if face_num0 == face_num1:
                print("结果是：",face_num0)
                face_result = face_num0
            if face_num0 == face_num2:
                print("结果是：",face_num0)
                face_result = face_num0
            if face_num1 == face_num2:
                print("结果是：",face_num1)
                face_result = face_num1
            #else:
             #   print("error")
              #  face_result = 15

    if value1 == 0: # 第2个按键单独按下时，开启口罩判别模式
        print("正在开启口罩判别模式")
        
        p_out0.low() # 0100 第2个灯亮 表示第2个按键被按下
        p_out1.high()
        p_out2.low()
        p_out3.low()

        sensor.skip_frames(time = 500) # 延时0.5s

        p_out0.low() # 将4个输出IO口全部置低电平
        p_out1.low()
        p_out2.low()
        p_out3.low()

        #设置样本数量
        NUM_SUBJECTS = 3 # 图像库总人数
        NUM_SUBJECTS_IMGS = 5 # 样本图片数量

        for mask in range(3):
            # 拍摄当前人脸。
            sensor.skip_frames(time = 3000) # 等待3s
            img = sensor.snapshot() # 拍照
            d0 = img.find_lbp((11,14,70,84)) # 当前拍摄人脸的lbp特征，将识别ROI区域往内缩小1/8

            img = None
            pmin = 999999 # pmin为最小特征差异度
            mask_num=0

            def min(pmin, a, s): # 确保几次循环后pmin还是最小特征差异度，a代表dist/NUM_SUBJECTS_IMGS
                global mask_num
                if a<pmin:
                    pmin=a
                    mask_num=s
                return pmin

            for s in range(1, NUM_SUBJECTS+1):
                dist = 0
                for i in range(2, NUM_SUBJECTS_IMGS+1):
                    img = image.Image("mask/m%d/%d.pgm"%(s, i))
                    d1 = img.find_lbp((11,14,70,84)) # d1为第s文件夹中的第i张图片的lbp特征，识别ROI区域往内缩小1/8
                    dist += image.match_descriptor(d0, d1) # 计算d0 d1即样本图像与被检测人脸的特征差异度。
                print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS)) # 输出当前特征差异度，方便在串口终端显示数据
                pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s) # 特征差异度越小，被检测人脸与此样本更相似更匹配。
                print(pmin)
            
            # 按照循环次数，将每次识别后的结果存入，共3次            
            if mask == 0:
                mask_num0 = mask_num
                print("第%d次:%d"%(mask+1,mask_num0))
            if mask == 1:
                mask_num1 = mask_num
                print("第%d次:%d"%(mask+1,mask_num1))
            if mask == 2:
                mask_num2 = mask_num
                print("第%d次:%d"%(mask+1,mask_num2))

            pyb.LED(GREEN_LED_PIN).on() # 绿灯亮
            sensor.skip_frames(time = 50) # 等待0.05s
            pyb.LED(GREEN_LED_PIN).off() #绿灯灭

        # 在此处对3次输出结果进行比较，输出出现次数最多的那个结果。如果三个分别为不同结果，则报错。
        if mask_num0 == mask_num1 == mask_num2:
            print("结果是：",mask_num0)
            mask_result = mask_num0
        else:
            if mask_num0 == mask_num1:
                print("结果是：",mask_num0)
                mask_result = mask_num0
            if mask_num0 == mask_num2:
                print("结果是：",mask_num0)
                mask_result = mask_num0
            if mask_num1 == mask_num2:
                print("结果是：",mask_num1)
                mask_result = mask_num1
            #else:
                #print("error")

    # 此处为输出IO口高低电平定义，具体请参照附表
    # 身份识别结果输出
    if face_result == 1:#1000
        print("face_num1",face_result)
        p_out0.high()
        p_out1.low()
        p_out2.low()
        p_out3.low()

    if face_result == 2:#0100
        print("face_num2",face_result)
        p_out0.low()
        p_out1.high()
        p_out2.low()
        p_out3.low()

    if face_result == 3:#0010
        print("face_num3",face_result)
        p_out0.low()
        p_out1.low()
        p_out2.high()
        p_out3.low()

    if face_result == 15:#1111
        print("error",face_result)
        p_out0.high()
        p_out1.high()
        p_out2.high()
        p_out3.high()

    # 口罩判别结果输出
    if mask_result == 1:#0011
        print("mask_num1",mask_result)
        p_out0.low()
        p_out1.low()
        p_out2.high()
        p_out3.high()

    if mask_result == 2:#1100
        print("mask_num2",mask_result)
        p_out0.high()
        p_out1.high()
        p_out2.low()
        p_out3.low()

    if mask_result == 15:#1111
        print("error",mask_result)
        p_out0.high()
        p_out1.high()
        p_out2.high()
        p_out3.high()

    # 学习后识别结果输出
    if iden_out_result == 1:#0100
        print("iden_out_num1",iden_out_result)
        p_out0.low()
        p_out1.high()
        p_out2.low()
        p_out3.low()

    if iden_out_result == 2:#0010
        print("iden_out_num2",iden_out_result)
        p_out0.low()
        p_out1.low()
        p_out2.high()
        p_out3.low()

    if iden_out_result == 3:#0001
        print("iden_out_num3",iden_out_result)
        p_out0.low()
        p_out1.low()
        p_out2.low()
        p_out3.high()

    if iden_out_result == 15:#1111
        print("error",iden_out_result)
        p_out0.high()
        p_out1.high()
        p_out2.high()
        p_out3.high()










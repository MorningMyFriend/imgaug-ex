# original project: https://github.com/aleju/imgaug

# extension: add perspective augment to imgaug

# 使用方法
### 增强脚本: demo/augment_by_xml.py
### 待处理的图像文件结构:
```buildoutcfg
建立软连接到 demo/VOC $(bash): cd demo && ln -s your_path VOC 

demo/VOC
   |
    --- img
         |
          --- test1.jpg
         |
          --- test2.jpg
   |
    --- xml
         |
          --- test1.xml
         |
          --- test2.xml

```

### 生成的图像和标签存在 demo/img 和 demo/pascal

   
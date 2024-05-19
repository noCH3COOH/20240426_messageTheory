# 20240426_messageTheory
***
## 目录
- [20240426\_messageTheory](#20240426_messagetheory)
  - [目录](#目录)
  - [项目简介](#项目简介)
    - [项目介绍](#项目介绍)
    - [项目结构](#项目结构)
  - [功能列表](#功能列表)
  - [依赖](#依赖)
  - [安装过程](#安装过程)
  - [使用方法](#使用方法)
  - [更新日志](#更新日志)

***
## 项目简介

### 项目介绍

### 项目结构
``` shell
----20240426_messageTheory
    |----src
    |----dst
    |----log
    |----rebuild
    |----main.py   (10.188KB)
    |----huffman.py   (9.133KB)
    |----compare.py   (1.768KB)
    |----README.md   (0.000B)
    |----requirements.txt   (0.000B)
    |----.gitignore   (16.000B)
```
包含以下类型的文件：['无后缀', '.py', '.md', '.txt', '.sample', '.idx', '.pack', '.hf', '.hflist', '.bmp', '.pyc']

***
## 功能列表
使用 huffman 编码压缩 bitmap 图片

***
## 依赖

os
math
time
json
filecmp
matplotlib

***
## 安装过程

下载即可

***
## 使用方法

1. 在 `main.py` 同级目录下创建 `src`、`dst`、`rebuild`、`log` 四个文件夹。

2. 在 `src` 文件夹中放入自己想要压缩的 bitmap 图片（`*.bmp`），随后在 `main.py` 同级目录下打开命令行，输入

```shell
python main.py
```

3. 等待其跑完即可

4. （补充）若需要对比重建文件与源文件的异同，只需要在上述打开的命令行中输入：

```shell
python compare.py
```

前提是你已经跑完了 `main.py` 里的程序

***
## 更新日志
无

***

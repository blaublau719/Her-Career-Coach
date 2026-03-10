# 非开发者简易安装指南

本指南将帮助您在电脑上运行求职信生成器，无需安装Python或VS Code。

## 所需工具

1. **Docker Desktop** (免费软件)
2. **您的OpenAI API密钥** (AI工作必需，用兰的)
3. **可选**: Serper API密钥 (用于增强公司研究功能，用兰的)

## 步骤1: 安装Docker Desktop

1. 从以下网址下载Docker Desktop: https://www.docker.com/products/docker-desktop/
2. 按照安装程序说明进行安装
3. 启动Docker Desktop (您会在系统托盘中看到一个鲸鱼图标)

## 步骤2: 设置API密钥 (已经添加了，可以跳过这步)

1. 用文本编辑器(如记事本)打开`.env`文件
2. 将`your_openai_api_key_here`替换为您的真实OpenAI API密钥
3. 如果有Serper API密钥，也可以添加(可选)
4. 保存文件

**获取API密钥:**
- **OpenAI**: 访问 https://platform.openai.com/api-keys 创建新密钥
- **Serper** (可选): 访问 https://serper.dev/ 免费注册

## 步骤3: 运行应用程序

### Windows用户:
1. 双击`run`文件
2. 等待应用程序启动(首次运行需要几分钟，等看到Application startup complete.就可以进行下一步)
3. 打开浏览器，访问: http://localhost:8000 (复制这个链接到浏览器)

### Mac/Linux用户:
1. 打开终端
2. 导航到此文件夹
3. 运行: `./run.sh`
4. 打开浏览器，访问: http://localhost:8000

## 使用应用程序

1. 粘贴工作职位URL
2. 上传您的简历或粘贴文本内容 (支持word, pdf, txt)
3. 填写您对该职位的求职动机
4. 选择"基础"或"完整"模式
5. 点击"生成求职信"
6. 等待AI为您创建个性化求职信

## 停止应用程序

- 关闭终端/命令行窗口，或
- 在终端中按`Ctrl+C`

## 故障排除

**应用程序无法启动:**
- 确保Docker Desktop正在运行
- 检查`.env`文件中的API密钥是否正确

**生成速度慢:**
- 完整模式需要3-5分钟 - 这是正常的
- 基础模式应该需要1-2分钟

**需要帮助?**
- 检查您的OpenAI API密钥是否有余额
- 确保您有网络连接

## 应用程序功能

- 自动分析职位发布
- 创建个性化德语求职信
- 事实核查内容确保真实性
- 研究公司背景(完整模式)
- 为特定工作优化您的简历(完整模式)

生成的文件将保存在`outputs`文件夹中。
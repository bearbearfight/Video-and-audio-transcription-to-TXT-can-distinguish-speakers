#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASR API测试脚本
直接通过POST请求调用API接口，不依赖HTML页面
"""

import requests
import json
import time
import os

def test_api_with_cos_url(simulate=False):
    """通过COS URL测试API接口"""
    
    # API接口地址
    api_url = "http://localhost:8000/api/asr/convert/"#注意这边需要自己去创建接口，然后将自己的接口放到上面
    
    # 请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 请求数据 - 使用您提供的COS URL
    data = {
        "cos_url": "https://存储桶.cos.ap-shanghai.myqcloud.com/视频文件",#这边存储桶需要填上自己的，视频文件需要填存储桶里面的视频文件可以是mp4或者wav后缀
        "simulate": "true"
    }
    
    # 如果启用模拟模式
    if simulate:
        data["simulate"] = "true"
    
    print("=" * 60)
    if simulate:
        print("ASR API测试 - 模拟模式")
    else:
        print("ASR API测试 - COS URL方式")
    print("=" * 60)
    
    print(f"API地址: {api_url}")
    if not simulate:
        print(f"COS URL: {data['cos_url']}")
    print(f"模拟模式: {simulate}")
    print("-" * 60)
    
    try:
        # 发送POST请求
        print("正在发送请求...")
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        print(f"响应状态码: {response.status_code}")
        
        # 解析响应
        if response.status_code == 200:
            result = response.json()
            print("请求成功!")
            
            # 检查是否为模拟模式
            if result.get('simulated', False):
                print("模拟模式结果")
            else:
                print("真实识别结果")
                
            print(f"任务ID: {result.get('task_id', 'N/A')}")
            print(f"文本行数: {result.get('text_count', 'N/A')}")
            print(f"保存文件: {result.get('file_saved', 'N/A')}")
            print(f"结果文件路径: {result.get('result_file', 'N/A')}")
            
            # 优先显示说话人划分后的内容
            speaker_text_lines = result.get('speaker_text_lines', [])
            if speaker_text_lines:
                print("\n说话人划分结果:")
                print("-" * 40)
                for line in speaker_text_lines:
                    print(line)
            
            # 如果没有说话人划分结果，显示原始文本内容
            elif result.get('text_lines', []):
                text_lines = result.get('text_lines', [])
                print("\n识别的文本内容:")
                print("-" * 40)
                for i, line in enumerate(text_lines, 1):
                    print(f"{i}. {line}")
            
        elif response.status_code == 400:
            result = response.json()
            print("请求失败 - 客户端错误")
            print(f"错误信息: {result.get('message', '未知错误')}")
            
        elif response.status_code == 403:
            result = response.json()
            print("请求失败 - 资源包耗尽")
            print(f"错误信息: {result.get('message', '未知错误')}")
            
        elif response.status_code == 500:
            result = response.json()
            print("请求失败 - 服务器错误")
            print(f"错误信息: {result.get('message', '未知错误')}")
            
        else:
            print(f"未知错误状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("连接失败 - 请确保Django服务器正在运行")
        print("运行命令: python manage.py runserver 0.0.0.0:8000")
        
    except requests.exceptions.Timeout:
        print("请求超时 - 请检查网络连接")
        
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

def test_health_check():
    """测试健康检查接口"""
    
    health_url = "http://localhost:8000/api/asr/health/"
    
    print("\n" + "=" * 60)
    print("健康检查测试")
    print("=" * 60)
    
    try:
        response = requests.get(health_url)
        print(f"健康检查状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("服务健康")
            print(f"服务状态: {result.get('status', 'N/A')}")
            print(f"服务名称: {result.get('service', 'N/A')}")
        else:
            print("服务异常")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("无法连接到服务 - 请启动Django服务器")
        return False
        
    except Exception as e:
        print(f"健康检查失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    
    print("ASR API测试脚本")
    print("此脚本直接通过POST请求调用API，不依赖HTML页面")
    print("=" * 60)
    
    # 首先检查服务是否可用
    if not test_health_check():
        print("\n服务不可用，请先启动Django服务器")
        print("启动命令: python manage.py runserver 0.0.0.0:8000")
        return
    
    # 测试模拟模式（避免腾讯云资源包耗尽问题）
    print("\n由于腾讯云ASR资源包已耗尽，优先测试模拟模式")
    test_api_with_cos_url(simulate=True)
    
    print("\n" + "=" * 60)
    print("模拟模式测试完成!")
    print("=" * 60)
    
    # 询问是否测试真实模式
    print("\n提示：由于腾讯云ASR资源包已耗尽，真实模式会失败")
    user_input = input("是否继续测试真实模式？(y/N): ").strip().lower()
    
    if user_input == 'y' or user_input == 'yes':
        print("\n" + "=" * 60)
        print("开始测试真实模式...")
        print("=" * 60)
        test_api_with_cos_url(simulate=False)
    else:
        print("跳过真实模式测试")

if __name__ == "__main__":
    main()

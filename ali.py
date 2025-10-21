import requests
import json
import sys

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get("http://localhost:8001/api/asr/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_api_with_cos_url(simulate=False):
    """测试COS URL方式的API调用"""
    print(f"\n🎯 {'ASR API测试 - 模拟模式' if simulate else 'ASR API测试 - 真实模式'}...")
    
    # 使用带反引号的COS URL
    cos_url = "`https://bestu-bucket-python.oss-cn-shanghai.aliyuncs.com/68e85f700f620c466212e6fc.mp4`"
    

    # ossutil cp oss://bestu-bucket-python/68e85f700f620c466212e6fc.mp4 C:/Users/Administrator/Desktop
    # 准备请求数据
    data = {
        'cos_url': cos_url,
        'auto_split': True,
        'supervise_type': 2  # 2表示使用算法决定人数
    }
    
    # 如果启用模拟模式，添加simulate参数
    if simulate:
        data['simulate'] = 'true'
        print("📋 模拟模式: True")
    else:
        print("📋 模拟模式: False")
    
    print(f"🌐 COS URL: {cos_url}")
    
    try:
        response = requests.post(
            "http://localhost:8001/api/asr/convert/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            
            # 检查是否为模拟模式结果
            if result.get('simulated'):
                print("📋 模拟模式结果:")
                # 显示使用的测试数据文件来源
                source_file = result.get('source_file')
                if source_file:
                    print(f"   📂 数据来源: {source_file}")
                else:
                    note = result.get('note')
                    if note:
                        print(f"   ℹ️  {note}")
            else:
                print("📋 真实识别结果:")
            
            print(f"   📄 任务ID: {result.get('task_id')}")
            print(f"   📊 文本行数: {result.get('text_count')}")
            print(f"   💾 文件保存: {result.get('file_saved')}")
            print(f"   📁 结果文件: {result.get('result_file')}")
            
            # 优先显示说话人划分后的内容
            speaker_text_lines = result.get('speaker_text_lines', [])
            if speaker_text_lines:
                print("\n🎤 说话人划分结果:")
                for line in speaker_text_lines:
                    print(f"   {line}")
            
            # 如果没有说话人划分结果，显示原始文本内容
            elif result.get('text_lines', []):
                text_lines = result.get('text_lines', [])
                print("\n📝 识别结果内容:")
                for i, line in enumerate(text_lines, 1):
                    print(f"   {i}. {line}")
            
            return True
            
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ 请求参数错误: {error_data.get('message')}")
            return False
            
        elif response.status_code == 500:
            error_data = response.json()
            print(f"❌ 服务器内部错误: {error_data.get('message')}")
            return False
            
        else:
            print(f"❌ 未知错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 阿里云ASR API测试脚本")
    print("=" * 50)
    
    # 首先测试健康检查
    if not test_health_check():
        print("\n❌ 健康检查失败，请先启动Django服务器")
        print("启动命令: cd c:\\Users\\Administrator\\Desktop\\new_collage\\ali && python manage.py runserver 0.0.0.0:8001")
        return
    
    # 直接测试真实模式
    print("\n💡 直接测试真实模式...")
    if test_api_with_cos_url(simulate=False):
        print("\n✅ 真实模式测试成功!")
    else:
        print("\n❌ 真实模式测试失败")

if __name__ == "__main__":
    main()

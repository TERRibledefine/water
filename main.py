import time
import requests
import hashlib
import random

# ==================== 颜色常量 ====================
class Colors:
    """ANSI颜色常量"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # 文本颜色
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 背景颜色
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

# ==================== 彩色输出函数 ====================
def color_print(text: str, color: str = Colors.WHITE, bold: bool = False, bg_color: str = "") -> None:
    """彩色打印"""
    if bold:
        text = f"{Colors.BOLD}{text}{Colors.RESET}"
    if bg_color:
        text = f"{bg_color}{text}{Colors.RESET}"
    print(f"{color}{text}{Colors.RESET}")

def success_print(text: str, bold: bool = True, bg: bool = False) -> None:
    """成功消息打印"""
    if bg:
        color_print(f"🎉 {text}", Colors.BG_GREEN, bold, Colors.WHITE)
    else:
        color_print(f"✅ {text}", Colors.GREEN, bold)

def error_print(text: str, bold: bool = True, bg: bool = False) -> None:
    """错误消息打印"""
    if bg:
        color_print(f"💥 {text}", Colors.BG_RED, bold, Colors.WHITE)
    else:
        color_print(f"❌ {text}", Colors.RED, bold)  # 修复：之前错用BLUE，改为RED更直观

def info_print(text: str, bold: bool = False, bg: bool = False) -> None:
    """信息消息打印"""
    if bg:
        color_print(f"ℹ️ {text}", Colors.BG_BLUE, bold, Colors.WHITE)
    else:
        color_print(f"ℹ️ {text}", Colors.BLUE, bold)  # 修复：图标改为ℹ️，区分成功

def warning_print(text: str, bold: bool = False, bg: bool = False) -> None:
    """警告消息打印"""
    if bg:
        color_print(f"⚠️ {text}", Colors.BG_YELLOW, bold, Colors.BLACK)
    else:
        color_print(f"⚠️ {text}", Colors.YELLOW, bold)

def highlight_print(text: str, color: str = Colors.YELLOW, bold: bool = True, bg: bool = False) -> None:
    """高亮消息打印"""
    if bg:
        color_print(text, color, bold, Colors.BG_WHITE)
    else:
        color_print(text, color, bold)

# ==================== 配置常量 ====================
# 填入tokens
TOKENS = [
    "23d10144369a3806f90bb8f17f48565f",
]

# 用户代理
USER_AGENT = "Mozilla/5.0 (Linux; U; Android 14; zh-cn; RMX3706 Build/UKQ1.230924.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.168 Mobile Safari/537.36 HeyTapBrowser/40.10.10.1"

# 跳过的任务代码列表
NOT_FINISH_TASKS = [
    "7328b1db-d001-4e6a-a9e6-6ae8d281ddbf",
    "e8f837b8-4317-4bf5-89ca-99f809bf9041",
    "65a4e35d-c8ae-4732-adb7-30f8788f2ea7",
    "73f9f146-4b9a-4d14-9d81-3a83f1204b74",
    "12e8c1e4-65d9-45f2-8cc1-16763e710036",
    "75dc2d16-dd46-4123-90a2-9e4c7219ae71"
]

# 任务相关常量
ALIPAY_VIDEO_TASK_CODE = "dc18b525-f679-47d8-805a-e331f8f3341d"
ALIPAY_AD_TASK_CODE = "9"
MAX_VIDEO_ATTEMPTS = 10
MAX_AD_ATTEMPTS = 50

# ==================== 工具函数 ====================
def sha256_encrypt(data: str) -> str:
    """SHA256加密"""
    sha256 = hashlib.sha256()
    sha256.update(data.encode("utf-8"))
    return sha256.hexdigest()

def sign_zfb(timestamp: str, url: str, token: str) -> str:
    """支付宝渠道签名"""
    sign_str = f"appSecret=Ew+ZSuppXZoA9YzBHgHmRvzt0Bw1CpwlQQtSl49QNhY=&channel=alipay&timestamp={timestamp}&token={token}&version=1.96.1&{url[25:]}"
    return sha256_encrypt(sign_str)

def sign_android(timestamp: str, url: str, token: str) -> str:
    """Android渠道签名"""
    sign_str = f"appSecret=nFU9pbG8YQoAe1kFh+E7eyrdlSLglwEJeA0wwHB1j5o=&channel=android_app&timestamp={timestamp}&token={token}&version=1.96.1&{url[25:]}"
    return sha256_encrypt(sign_str)

def http_request(url: str, token: str, data: dict, method: str) -> dict:
    """通用HTTP请求函数（模拟真实APP环境）"""
    timestamp = str(int(time.time() * 1000))
    
    # 根据方法选择签名方式
    if "alipay" in url:
        signature = sign_zfb(timestamp, url, token)
        channel = "alipay"
    else:
        signature = sign_android(timestamp, url, token)
        channel = "android_app"
    
    # 核心修改：模拟真实APP的请求头（新增设备指纹字段）
    headers = {
        "Authorization": token,
        "Version": "1.96.1",
        "channel": channel,
        "phoneBrand": "realme",  # 匹配你的设备 RMX3706（真我手机）
        "phoneModel": "RMX3706", # 新增：真实机型
        "systemVersion": "14",   # 新增：系统版本
        "appVersion": "1.96.1",  # 新增：APP版本
        "deviceId": "868888888888888", # 新增：模拟设备ID（可替换为真实的）
        "timestamp": timestamp,
        "sign": signature,
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": USER_AGENT,
        # 新增：隐藏Python请求特征
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://userapi.qiekj.com/",
        "Origin": "https://userapi.qiekj.com/"
    }
    
    try:
        # 核心修改：使用会话保持，模拟真实APP的cookie/登录态
        session = requests.Session()
        # 先访问首页，获取cookie
        session.get("https://userapi.qiekj.com/", headers=headers, timeout=15)
        
        response = session.post(
            url=url,
            headers=headers,
            json=data,
            timeout=15,
            # 新增：禁用代理，模拟真实网络环境
            proxies={"http": None, "https": None},
            # 新增：模拟移动端请求的TCP参数
            stream=False,
            verify=False  # 忽略SSL验证（APP端通常不验证）
        )
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("msg") == "未登录":
                    error_print("未登录，请检查token有效性")
                    exit()
                return result
            except:
                error_print(f"响应不是JSON格式: {response.text[:100]}")
                return None
        else:
            error_print(f"请求出错 - 状态码: {response.status_code}")
            color_print(f"响应内容: {response.text[:200]}", Colors.CYAN)
            return None
            
    except requests.exceptions.Timeout:
        warning_print("请求超时，稍后重试")
        return {"error": "timeout"}
    except Exception as e:
        error_print(f"请求异常: {e}")
        return None

# ==================== 业务函数 ====================
def get_user_info(token: str) -> None:
    """获取用户信息"""
    url = "https://userapi.qiekj.com/user/info"
    data = {"token": token}
    result = http_request(url, token, data, "post")
    
    if result and result.get("code") == 0:
        user_data = result.get("data", {})
        username = user_data.get("userName", "未设置昵称")
        highlight_print(f"========== {username} ==========", Colors.YELLOW)
        
        # 获取并显示初始积分
        balance_result = get_user_balance(token)
        if balance_result:
            initial_integral = balance_result.get("integral", 0)
            highlight_print(f"💰 初始积分: {initial_integral}", Colors.GREEN, True)
        else:
            warning_print("⚠️  积分数据加载中...")
    else:
        error_print("获取用户信息失败")

def get_user_balance(token: str) -> dict:
    """获取用户积分余额"""
    url = "https://userapi.qiekj.com/user/balance"
    data = {"token": token}
    result = http_request(url, token, data, "post")
    return result.get("data", {}) if result else {}

def daily_signin(token: str) -> None:
    """每日签到"""
    url = "https://userapi.qiekj.com/signin/doUserSignIn"
    data = {"activityId": "600001", "token": token}
    result = http_request(url, token, data, "post")
    
    if result:
        if result.get("code") == 0:
            integral = result.get("data", {}).get("totalIntegral", 0)
            success_print(f"签到成功，获得积分: {integral}")
        elif result.get("code") == 33001:
            info_print("今日已签到")
        else:
            error_print(f"签到失败: {result.get('msg', '未知错误')}")
    else:
        error_print("签到请求失败")

def home_page_browse(token: str) -> None:
    """首页浏览任务"""
    url = "https://userapi.qiekj.com/task/queryByType"
    data = {"taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a", "token": token}
    result = http_request(url, token, data, "post")
    
    if result and result.get("code") == 0 and result.get("data"):
        success_print("首页浏览成功，获得1积分")
    else:
        info_print("首页浏览任务已完成/请求失败")  # 修复：从error改为info，更准确

def get_task_list(token: str) -> list:
    """获取任务列表"""
    url = "https://userapi.qiekj.com/task/list"
    data = {"token": token}
    result = http_request(url, token, data, "post")
    
    if result and result.get("code") == 0:
        return result.get("data", {}).get("items", [])
    else:
        error_print("获取任务列表失败")
        return []

def complete_task(token: str, task_code: str, task_title: str = "") -> dict:
    """完成任务"""
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": task_code, "token": token}
    
    # 支付宝任务使用特殊签名
    if "alipay" in task_code or task_code == "dc18b525-f679-47d8-805a-e331f8f3341d":
        return complete_zfb_task(token, task_code)
    
    return http_request(url, token, data, "post")

def complete_zfb_task(token: str, task_code: str) -> dict:
    """完成支付宝任务（修复超时和405）"""
    url = "https://userapi.qiekj.com/task/completed"
    timestamp = str(int(time.time() * 1000))
    
    headers = {
        'Authorization': token,
        'Version': '1.96.1',
        'channel': 'alipay',
        'phoneBrand': 'Redmi',
        'timestamp': timestamp,
        'sign': sign_zfb(timestamp, url, token),
        # 修复：改用JSON格式
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'userapi.qiekj.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': USER_AGENT
    }
    
    data = {"taskCode": task_code, "token": token}
    try:
        # 修复3：超时延长到10秒，改用JSON传参
        response = requests.post(
            url=url,
            headers=headers,
            json=data,  # 关键修复
            timeout=10
        )
        try:
            return response.json()
        except:
            error_print(f"支付宝任务响应解析失败: {response.text[:100]}")
            return {"code": -1, "msg": "响应格式错误"}
    except Exception as e:
        error_print(f"支付宝任务请求失败: {e}")
        return {"code": -1, "msg": "请求失败"}

def run_zfb_repetitive_task(token: str, task_code: str, task_name: str, emoji: str, max_attempts: int) -> int:
    """运行支付宝重复任务（游戏/广告）- 增加容错"""
    highlight_print(f"{emoji} 开始执行支付宝{task_name}任务...", Colors.CYAN)
    completed_count = 0
    
    for i in range(max_attempts):
        result = complete_zfb_task(token, task_code)
        
        # 修复4：增加JSON解析失败的容错
        if not isinstance(result, dict):
            warning_print(f"    {task_name}任务响应异常，跳过本次")
            time.sleep(random.uniform(5, 8))
            continue
        
        if result.get("code") == 0 and result.get("data"):
            completed_count += 1
            
            # 显示进度条
            progress = int((completed_count / max_attempts) * 20)
            progress_bar = "🟩" * progress + "⬜" * (20 - progress)
            color_print(f"  {emoji} {task_name} {completed_count}/{max_attempts} 完成 [{progress_bar}] {progress*5}%", Colors.GREEN)
            
            if completed_count < max_attempts:
                wait_time = random.uniform(15, 18)
                color_print(f"    ⏳ 等待 {wait_time:.1f} 秒继续...", Colors.GREEN)
                time.sleep(wait_time)
        else:
            warning_print(f"    🔴 {task_name}任务结束 (原因: {result.get('msg', '未知')})")
            break
    
    # 根据任务类型显示正确的积分奖励
    if task_name == "游戏" and completed_count >= 10:
        success_print(f"{emoji} 支付宝{task_name}任务完成，共完成 {completed_count} 次，获得 30 积分")
    elif task_name == "广告" and completed_count >= 50:
        success_print(f"{emoji} 支付宝{task_name}任务完成，共完成 {completed_count} 次，获得 150 积分")
    else:
        success_print(f"{emoji} 支付宝{task_name}任务完成，共完成 {completed_count} 次")
    return completed_count

def run_zfb_video_task(token: str) -> int:
    """运行玩游戏得积分任务"""
    return run_zfb_repetitive_task(token, ALIPAY_VIDEO_TASK_CODE, "游戏", "🎮", MAX_VIDEO_ATTEMPTS)

def run_zfb_ad_task(token: str) -> int:
    """运行支付宝广告任务"""
    return run_zfb_repetitive_task(token, ALIPAY_AD_TASK_CODE, "广告", "📊", MAX_AD_ATTEMPTS)

# ==================== 主程序 ====================
def print_separator(message: str = "") -> None:
    """打印分隔线"""
    color_print("\n" + "="*60, Colors.YELLOW)
    if message:
        highlight_print(f"  {message}", Colors.YELLOW, True)
        color_print("="*60, Colors.YELLOW)
  
def main() -> None:
    """主函数"""
    highlight_print("🚀 胖乖自动任务脚本 v2.2 (修复版)", Colors.MAGENTA, True)
    color_print("="*60, Colors.YELLOW)
    
    total_start_time = time.time()
    
    for idx, token in enumerate(TOKENS, 1):
        account_start_time = time.time()
        highlight_print(f"\n📱 正在处理第 {idx}/{len(TOKENS)} 个账号", Colors.CYAN)
        print_separator("账号开始")
        
        # 获取用户信息
        get_user_info(token)
        time.sleep(1)
        
        # 获取初始积分
        initial_balance = get_user_balance(token)
        initial_integral = initial_balance.get("integral", 0)
        
        # 签到
        daily_signin(token)
        time.sleep(1)
        
        # 首页浏览
        home_page_browse(token)
        time.sleep(1)
        
        # 获取并执行任务列表
        print_separator("普通任务")
        tasks = get_task_list(token)
        
        if not tasks:
            info_print("暂无任务可执行")
        else:
            for task in tasks:
                task_code = task.get("taskCode", "")
                task_title = task.get("title", "未知任务")
                completed_status = task.get("completedStatus", 1)
                
                # 跳过已完成和特定任务
                if completed_status == 0 and task_code not in NOT_FINISH_TASKS and task_code != "2":
                    task_start_time = time.time()
                    color_print(f"\n📋 开始执行: {task_title}", Colors.GREEN)
                    
                    limit = task.get("dailyTaskLimit", 1)
                    success = True
                    
                    for attempt in range(limit):
                        result = complete_task(token, task_code, task_title)
                        
                        if result and result.get("code") == 0 and result.get("data"):
                            info_print(f"  📈 进度: {attempt+1}/{limit}")
                            time.sleep(random.uniform(8, 12))
                        else:
                            error_print(f"  任务失败: {result.get('msg', '未知错误') if result else '请求无响应'}", False)
                            success = False
                            break
                    
                    task_time = time.time() - task_start_time
                    if success:
                        success_print(f"🎯 {task_title} 共完成{limit}次 (耗时: {task_time:.1f}秒)，获得{limit}积分")
                    time.sleep(random.uniform(1, 2))
        
        # 玩游戏得积分任务
        print_separator("玩游戏得积分任务")
        video_start_time = time.time()
        video_count = run_zfb_video_task(token)
        video_time = time.time() - video_start_time
        if video_count > 0:
            info_print(f"  📊 游戏积分任务总耗时: {video_time:.1f}秒 (平均每个游戏: {video_time/video_count:.1f}秒)")
        
        # 支付宝广告任务
        print_separator("支付宝广告任务")
        ad_start_time = time.time()
        ad_count = run_zfb_ad_task(token)
        ad_time = time.time() - ad_start_time
        if ad_count > 0:
            info_print(f"  📊 广告任务总耗时: {ad_time:.1f}秒 (平均每个广告: {ad_time/ad_count:.1f}秒)")
        
        # 统计积分
        print_separator("任务统计")
        final_balance = get_user_balance(token)
        final_integral = final_balance.get("integral", 0)
        today_earned = final_integral - initial_integral
        
        color_print(f"📊 积分统计:", Colors.YELLOW, True)
        color_print(f"  💰 初始积分: {initial_integral}", Colors.BLUE)
        color_print(f"  🏦 当前积分: {final_integral}", Colors.BLUE)
        if today_earned > 0:
            color_print(f"  📈 今日获得: {today_earned} ✨", Colors.GREEN, True)
        elif today_earned < 0:
            color_print(f"  📉 今日获得: {today_earned}", Colors.RED, True)
        else:
            color_print(f"  📊 今日获得: {today_earned}", Colors.YELLOW)
        
        # 账号总耗时
        account_time = time.time() - account_start_time
        color_print(f"⏱️  账号处理总耗时: {account_time:.1f}秒", Colors.CYAN, True)
        
        print_separator(f"账号 {idx} 完成")
        highlight_print("\n" + "🎉"*30 + "\n", Colors.MAGENTA)
        
        # 账号间间隔
        if idx < len(TOKENS):
            info_print("等待3秒开始下一个账号...")
            time.sleep(3)
    
    # 总耗时统计
    total_time = time.time() - total_start_time
    highlight_print(f"\n⏱️  所有账号处理总耗时: {total_time:.1f}秒", Colors.MAGENTA, True)

if __name__ == "__main__":
    try:
        main()
        highlight_print("🎊 所有账号任务已完成！", Colors.MAGENTA, True)
    except KeyboardInterrupt:
        color_print("\n\n⏹️ 用户中断程序", Colors.CYAN)
    except Exception as e:
        error_print(f"\n程序异常: {e}")
        # 打印异常详情，方便排查
        import traceback
        color_print(f"异常详情: {traceback.format_exc()}", Colors.RED)

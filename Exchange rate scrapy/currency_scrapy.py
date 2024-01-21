import sys
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
currency_codes = {
    'GBP': '英镑',
    'HKD': '港币',
    'USD': '美元',
    'CHF': '瑞士法郎',
    'DEM': '德国马克',
    'FRF': '法国法郎',
    'SGD': '新加坡元',
    'SEK': '瑞典克朗',
    'DKK': '丹麦克朗',
    'NOK': '挪威克朗',
    'JPY': '日元',
    'CAD': '加拿大元',
    'AUD': '澳大利亚元',
    'EUR': '欧元',
    'MOP': '澳门元',
    'PHP': '菲律宾比索',
    'THB': '泰国铢',
    'NZD': '新西兰元',
    'KRW': '韩元',
    'RUB': '卢布',
    'MYR': '林吉特',
    'TWD': '新台币',
    'ESP': '西班牙比塞塔',
    'ITL': '意大利里拉',
    'NLG': '荷兰盾',
    'BEF': '比利时法郎',
    'FIM': '芬兰马克',
    'INR': '印度卢比',
    'IDR': '印尼卢比',
    'BRL': '巴西里亚尔',
    'AED': '阿联酋迪拉姆',
    'ZAR': '南非兰特',
    'SAR': '沙特里亚尔',
    'TRY': '土耳其里拉'
}


def get_currency_name(currency_code):
    # 获取货币名称
    return currency_codes.get(currency_code, None)


def get_exchange_rate(date, currency_name):

    # 创建一个Chrome浏览器实例
    driver = webdriver.Chrome()

    try:
        # 打开中国银行外汇牌价网站
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 等待页面加载完成
        time.sleep(2)

        # 输入日期
        date_input = driver.find_element("name", "erectDate")
        date_input.clear()
        date_input.send_keys(date)
        date_input = driver.find_element("name", "nothing")
        date_input.clear()
        date_input.send_keys(date)
        # 选择货币
        currency_select = driver.find_element("name", "pjname")
        currency_dropdown = Select(currency_select)
        currency_dropdown.select_by_visible_text(currency_name)

        # 点击查询按钮
        # 找到所有class为"search_btn"的元素
        search_buttons = driver.find_elements(By.CLASS_NAME, "search_btn")

        # 检查是否至少有两个元素
        if len(search_buttons) >= 2:
            # 选择第二个元素并点击
            second_search_button = search_buttons[1]
            second_search_button.click()
        else:
            print("没有足够的元素可供选择")
        # 等待查询结果加载完成
        time.sleep(2)

        # 找到包含该元素的父元素
        parent_element = driver.find_element(By.CSS_SELECTOR, "tr.odd")

        # 使用CSS选择器找到父元素下的第四个子元素
        fourth_child_element = parent_element.find_element(By.CSS_SELECTOR, "td:nth-child(4)")

        # 获取第四个子元素的文本内容即获取现汇卖出价
        exchange_rate = fourth_child_element.text

        return exchange_rate

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭浏览器
        driver.quit()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 currency_scrapy.py <date> <currency_code>")
        return

    date_input = sys.argv[1]
    currency_code_input = sys.argv[2]
    currency_name_input = get_currency_name(currency_code_input)

    if currency_name_input is None:
        print(f"无效的货币代码: {currency_code_input}")
    else:
        exchange_rate = get_exchange_rate(date_input, currency_name_input)
        if exchange_rate is not None:
            print(exchange_rate)
        else:
            print(f"无法找到 {currency_name_input} 在指定日期 {date_input} 的汇率信息。")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os

import fontforge

# 字体目录变量
font_dir = "."  # 可根据需要修改为实际字体所在目录

# 名称构造变量
mainFontPrefix = "JetBrainsMonoNerdFontMono-"
auxFontPrefix = "LXGWWenKaiMono-"
outputFontPrefix = "LXWenKaiJetBrMonoNF-"
postscriptNamePrefix = "LXWenKaiJetBrMonoNF-"
enName1 = "LXWenKai"
enName2 = "JetBr Nerd Mono"
chsName1 = "霞鹜文楷"
chsName2 = "JetBrains 等宽"


def merge_fonts(variant):
    # 构造文件名和参数
    mainFontFile = os.path.join(font_dir, mainFontPrefix + variant + ".ttf")
    auxFontFile = os.path.join(font_dir, auxFontPrefix + variant + ".ttf")

    outputFontFile = os.path.join(font_dir, outputFontPrefix + variant + ".ttf")
    postscriptName = postscriptNamePrefix + variant

    # 打开主字体
    font = fontforge.open(mainFontFile)

    # 清空现有的SFNT名称记录
    font.sfnt_names = ()

    # 使用FontForge的原生mergeFonts API合并字体
    font.mergeFonts(auxFontFile)

    # 设置字体属性
    family_en = f"{enName1} {enName2}"
    family_zh = f"{chsName1} {chsName2}"
    fullname_en = f"{enName1} {enName2}"
    fullname_zh = f"{chsName1} {chsName2}"

    # 设置字体信息
    font.familyname = family_en
    font.fullname = fullname_en
    font.fontname = postscriptName

    # 设置OS/2表信息
    font.os2_family_class = 0  # Default
    font.os2_weight = get_os2_weight(variant)
    font.os2_width = 5  # Medium (normal)

    if variant == "Regular":
        # ========== Regular 变体的设置 ==========
        # 英文
        font.appendSFNTName("English (US)", "Family", family_en)
        font.appendSFNTName("English (US)", "SubFamily", "Regular")
        font.appendSFNTName("English (US)", "Fullname", family_en)
        font.appendSFNTName("English (US)", "PostScriptName", postscriptName)
        # 注意：不设置 Preferred Family 和 Preferred Subfamily！

        # 中文
        font.appendSFNTName("Chinese (PRC)", "Family", family_zh)
        font.appendSFNTName("Chinese (PRC)", "SubFamily", "Regular")
        font.appendSFNTName("Chinese (PRC)", "Fullname", family_zh)

    else:
        # ========== 非Regular变体（Light/Medium等） ==========
        weighted_family_en = f"{family_en} {variant}"
        weighted_family_zh = f"{family_zh} {variant}"

        # 英文
        font.appendSFNTName("English (US)", "Family", weighted_family_en)
        font.appendSFNTName("English (US)", "SubFamily", variant)
        font.appendSFNTName("English (US)", "Fullname", weighted_family_en)
        font.appendSFNTName("English (US)", "PostScriptName", postscriptName)

        # 关键：设置 Preferred Family 和 Preferred Subfamily
        font.appendSFNTName("English (US)", "Preferred Family", family_en)
        # font.appendSFNTName("English (US)", "Preferred Subfamily", variant)

        # 中文
        font.appendSFNTName("Chinese (PRC)", "Family", weighted_family_zh)
        font.appendSFNTName("Chinese (PRC)", "SubFamily", variant)
        font.appendSFNTName("Chinese (PRC)", "Fullname", weighted_family_zh)
        font.appendSFNTName("Chinese (PRC)", "Preferred Family", family_zh)
        # font.appendSFNTName("Chinese (PRC)", "Preferred Subfamily", variant)

    # 厂商信息
    font.appendSFNTName("English (US)", "Manufacturer", "LXGW + Nerd Fonts")
    font.appendSFNTName("Chinese (PRC)", "Manufacturer", "LXGW + Nerd Fonts")

    # 4. 设置OS/2版本和唯一标识
    font.os2_vendor = "LXGW"

    # 设置其他属性
    font.comment = f"Merged font: {mainFontFile} + {auxFontFile}"
    font.version = "1.0"
    font.copyright = "Merged font"

    # 根据变体设置权重值
    set_custom_weight(font, variant)

    # 保存字体
    font.generate(outputFontFile)
    font.close()
    print(f"Generated: {outputFontFile}")


def get_os2_weight(variant):
    """返回对应变体的OS/2权重值"""
    weights = {
        "Thin": 250,
        "ExtraLight": 275,
        "Light": 300,
        "Normal": 400,
        "Regular": 400,
        "Medium": 500,
        "SemiBold": 600,
        "Bold": 700,
        "ExtraBold": 800,
        "Black": 900,
    }
    return weights.get(variant, 400)


def set_custom_weight(font, variant):
    """设置自定义权重值用于fc-query输出"""
    if variant == "Light":
        weight_value = 50
    elif variant == "Medium":
        weight_value = 100
    elif variant == "Regular":
        weight_value = 80
    else:
        weight_value = 80  # 默认值

    # 为fc-query设置正确的内部权重表示
    # 这里我们设置OS/2 Weight，但为了匹配要求的输出，我们保持一致
    if variant == "Light":
        font.weight = "Light"
        font.os2_weight = 300  # OS/2标准Light权重
    elif variant == "Medium":
        font.weight = "Medium"
        font.os2_weight = 500  # OS/2标准Medium权重
    elif variant == "Regular":
        font.weight = "Regular"
        font.os2_weight = 400  # OS/2标准Regular权重


# 处理所有变体
for variant in ["Light", "Medium", "Regular"]:
    merge_fonts(variant)

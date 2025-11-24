from openai import OpenAI
import time
import json

class RN_Translator_Node():
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_baseurl": ("STRING", {"default": "https://api.openai.com/v1"}),
                "api_key": ("STRING", {"default": ""}),
                "model": ("STRING", {"default": "gpt-3.5-turbo"}),
                "source_text": ("STRING", {"multiline": True, "default": "请输入要翻译的文本"}),
                "source_language": ("STRING", {"default": "自动检测"}),
                "target_language": ("STRING", {"default": "中文"}),
                "translation_style": (["标准", "正式", "口语化", "学术", "商务"], {"default": "标准"}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 2.0, "step": 0.1}),
            },
            "optional": {}
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("翻译结果", "原始文本")
    FUNCTION = "translate_text"
    CATEGORY = "RN翻译"

    def translate_text(self, api_baseurl, api_key, model, source_text, source_language, target_language, translation_style, temperature, system_prompt=None):
        if not api_key:
            return ("错误：请提供API密钥", source_text)
        
        if not source_text.strip():
            return ("错误：请输入要翻译的文本", source_text)

        try:
            client = OpenAI(api_key=api_key, base_url=api_baseurl)
            
            # 构建翻译提示词
            if system_prompt is None:
                system_prompt = "你是一个专业的翻译助手，能够准确地将文本从一种语言翻译成另一种语言。"
            
            # 根据翻译风格调整提示词
            style_prompts = {
                "标准": "请提供标准的翻译",
                "正式": "请使用正式、专业的语言进行翻译",
                "口语化": "请使用口语化、通俗易懂的语言进行翻译",
                "学术": "请使用学术性的语言进行翻译，保持专业性",
                "商务": "请使用商务场合适用的语言进行翻译"
            }
            
            translation_instruction = style_prompts.get(translation_style, "请提供标准的翻译")
            
            # 构建语言说明
            lang_instruction = f""
            if source_language != "自动检测":
                lang_instruction += f"从{source_language}"
            else:
                lang_instruction += "从源语言"
            
            lang_instruction += f"翻译成{target_language}"
            
            user_prompt = f"""
{translation_instruction}。
{lang_instruction}。

要翻译的文本：
{source_text}

请只返回翻译结果，不要添加任何解释或注释。"""

            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt.strip()}
            ]

            completion = client.chat.completions.create(
                model=model, 
                messages=messages, 
                temperature=temperature,
                max_tokens=4096
            )
            
            if completion is not None and hasattr(completion, 'choices') and len(completion.choices) > 0:
                translated_text = completion.choices[0].message.content.strip()
                return (translated_text, source_text)
            else:
                return ("错误：API返回空结果", source_text)
                
        except Exception as e:
            error_msg = f"翻译错误：{str(e)}"
            return (error_msg, source_text)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float(time.time())

# llm_advice.py
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from config import OPENAI_API_KEY, XAI_API_KEY

class LLMClient:
    def get_advice(self, portfolio, stock_prices, news):
        raise NotImplementedError("Subclasses must implement get_advice.")

class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def get_advice(self, portfolio, stock_prices, news):
        prompt = self._build_prompt(portfolio, stock_prices, news)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def _build_prompt(self, portfolio, stock_prices, news):
        return f"""
        You are a financial advisor. Based on the following data, provide investment advice for today.
        Portfolio: Cash: ${portfolio['cash']}, Stocks: {portfolio['stocks']}
        Risk Level: {portfolio['risk_level']}
        Today's Stock Prices: {stock_prices}
        Today's News: {news}
        Provide specific advice (e.g., buy/sell/hold, how much) and a brief rationale.
        """

class Grok3Client(LLMClient):
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1"  # xAI API endpoint
        )

    def get_advice(self, portfolio, stock_prices, news):
        prompt = self._build_prompt(portfolio, stock_prices, news)
        response = self.client.chat.completions.create(
            model="grok-3",  # Updated to Grok 3
            messages=[
                {"role": "system", "content": "You are a financial expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def _build_prompt(self, portfolio, stock_prices, news):
        return f"""
        You are a financial advisor. Based on the following data, provide investment advice for today.
        Portfolio: Cash: ${portfolio['cash']}, Stocks: {portfolio['stocks']}
        Risk Level: {portfolio['risk_level']}
        Today's Stock Prices: {stock_prices}
        Today's News: {news}
        Provide specific advice (e.g., buy/sell/hold, how much) and a brief rationale.
        """

class FinGPTClient(LLMClient):
    def __init__(self):
        self.model_name = "FinGPT/fingpt-llama-7b"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def get_advice(self, portfolio, stock_prices, news):
        prompt = self._build_prompt(portfolio, stock_prices, news)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    def _build_prompt(self, portfolio, stock_prices, news):
        return f"""
        You are a financial advisor. Based on the following data, provide investment advice for today.
        Portfolio: Cash: ${portfolio['cash']}, Stocks: {portfolio['stocks']}
        Risk Level: {portfolio['risk_level']}
        Today's Stock Prices: {stock_prices}
        Today's News: {news}
        Provide specific advice (e.g., buy/sell/hold, how much) and a brief rationale.
        """

def get_llm_client(llm_name):
    llm_name = llm_name.lower()
    if llm_name == "openai":
        return OpenAIClient()
    elif llm_name == "grok3":
        return Grok3Client()
    elif llm_name == "fingpt":
        return FinGPTClient()
    else:
        raise ValueError(f"Unsupported LLM: {llm_name}. Choose 'openai', 'grok3', or 'fingpt'.")

def get_investment_advice(llm_name, portfolio, stock_prices, news):
    client = get_llm_client(llm_name)
    return client.get_advice(portfolio, stock_prices, news)

if __name__ == "__main__":
    sample_portfolio = {"cash": 5000, "stocks": {"AAPL": 10, "TSLA": 5}, "risk_level": "Moderate"}
    sample_prices = {"AAPL": 182.34, "TSLA": 298.12}
    sample_news = "Fed hints at rate hike, TSLA announces new factory."
    for llm in ["openai", "grok3", "fingpt"]:
        try:
            advice = get_investment_advice(llm, sample_portfolio, sample_prices, sample_news)
            print(f"{llm.capitalize()} Advice: {advice}\n")
        except Exception as e:
            print(f"Error with {llm}: {e}\n")
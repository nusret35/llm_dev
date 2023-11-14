
import replicate

prompt = '''
- Abstract: This paper seeks to investigate and detail the scientific consensus surrounding climate change, focusing on its trends, impacts, and the effectiveness of various mitigation strategies. Data were gathered from multiple sources including satellite observations, ground-based measurements, and climate model simulations. Findings suggest that climate change consequences are already substantial and expected to worsen. However, targeted and aggressive mitigation strategies can significantly reduce future impacts.

- Introduction: Climate change, driven by human activities like burning fossil fuels and deforestation, has led to an increase in Earth's average temperature, causing shifts in weather patterns and rising sea levels. These impacts affect lives and ecosystems globally, with extreme weather events like hurricanes and droughts posing challenges to human societies and natural ecosystems. Despite progress in understanding climate change, gaps remain in quantifying its impacts and evaluating mitigation approaches. The complexity of the issue calls for continued research and attention.

- Conclusion: This text discusses the challenges of climate change and emphasizes the need for an integrative approach involving proactive mitigation, adaptive strategies, and global cooperation. It highlights the importance of science in guiding our understanding, public discourse, and policy decisions, while offering an overview of the current scientific understanding and potential strategies for mitigation and adaptation.

- Methodology: The text describes a thorough literature review on the subject of climate change, utilizing multiple databases and keywords, and also mentions analyzing publicly available data from meteorological stations, satellites, and climate models to gain insights into climate trends and patterns.

- Outcomes: The analysis of data has shown that human-induced climate change is causing significant effects on global ecosystems and human societies, and mitigation strategies need to be implemented more widely and aggressively to prevent the worst impacts. There is an urgent call for a comprehensive and coordinated global response that combines both mitigation and adaptation strategies.
'''

enrich_sys_prompt = 'You are a tool that enriches the abstract by giving insights from the sections of introduction, conclusion, methodoly, and outcomes. As an output, you give an enriched abstract of the article.'

insights_sys_prompt = 'You are a tool that extracts key insights from an article. You will be provided with article sections. As an output, you should provide concise insights about the given article in bulletpoints.'


rp_client = replicate.Client(api_token='r8_2tA69DBhLIRzC81EbCjYOfBKZ4vCPxB1e2Ymo')

output = rp_client.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    input={
    "debug": False,
    "top_k": 50,
    "top_p": 1,
    "prompt": prompt,
    "temperature": 0.75,
    "system_prompt": insights_sys_prompt,
    "max_new_tokens": 1000,
    "min_new_tokens": -1
  }
)

# The meta/llama-2-70b-chat model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
    print(item, end="")
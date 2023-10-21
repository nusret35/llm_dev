from summarizer import Summarizer

sections = {

    'Introduction':"Climate change, driven by human activities like burning fossil fuels and deforestation, has led to an increase in Earth's average temperature, causing shifts in weather patterns and rising sea levels. These impacts affect lives and ecosystems globally, with extreme weather events like hurricanes and droughts posing challenges to human societies and natural ecosystems. Despite progress in understanding climate change, gaps remain in quantifying its impacts and evaluating mitigation approaches. The complexity of the issue calls for continued research and attention.",

    'Conclusion' :'This text discusses the challenges of climate change and emphasizes the need for an integrative approach involving proactive mitigation, adaptive strategies, and global cooperation. It highlights the importance of science in guiding our understanding, public discourse, and policy decisions, while offering an overview of the current scientific understanding and potential strategies for mitigation and adaptation.',

    'Methodology' : 'The text describes a thorough literature review on the subject of climate change, utilizing multiple databases and keywords, and also mentions analyzing publicly available data from meteorological stations, satellites, and climate models to gain insights into climate trends and patterns.',

    'Outcomes' : 'The analysis of data has shown that human-induced climate change is causing significant effects on global ecosystems and human societies, and mitigation strategies need to be implemented more widely and aggressively to prevent the worst impacts. There is an urgent call for a comprehensive and coordinated global response that combines both mitigation and adaptation strategies.'
}


if __name__ == "__main__":
    llama_exec_path = '/Users/nusretkizilaslan/Desktop/AIProject/llama2/llama.cpp/main'
    summarizer = Summarizer(exec_path=llama_exec_path)
    abstract = "This paper seeks to investigate and detail the scientific consensus surrounding climate change, focusing on its trends, impacts, and the effectiveness of various mitigation strategies. Data were gathered from multiple sources including satellite observations, ground-based measurements, and climate model simulations. Findings suggest that climate change consequences are already substantial and expected to worsen. However, targeted and aggressive mitigation strategies can significantly reduce future impacts."
    print()
    print('ENRICH ABSTRACT 1')
    result = summarizer.enrich_abstract_1(abstract,sections)
    print()
    print(result)
    print('-----------------------------------------------------------------')
    print()
    print('ENRICH ABSTRACT 2')
    result = summarizer.enrich_abstract_2(abstract,sections)
    print()
    print(result)
    print('-----------------------------------------------------------------')
    
    

    
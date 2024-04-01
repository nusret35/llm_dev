import re
import subprocess

def shorten_text(long_string):
    # Split the long string into sentences based on periods
    sentences = long_string.split('.')

    # Exclude the last sentence if there are more than one sentence
    if len(sentences) > 1:
        shortened = '.'.join(sentences[:-2])
    else:
        shortened = long_string

    return shortened


def is_section(section_key) :
    counter = 0
    for character in section_key :
        if character == '.' :
            counter += 1
        elif counter == 1 and character.isnumeric() :
            return False
        """
        elif counter == 1 and character.isalpha() :
            model_response = is_section_model_response(section_key)
            return model_response
        """     
    return True


# Processes a dictionary of sections and groups subsections under their respective main sections.
def group_subsections(sections_dict):
    new_dict = {}
    sub_dict = {}
    prev_section = ''
    for index in range(len(sections_dict)):
        key = list(sections_dict.keys())[index]
        if is_section(key):
            if sub_dict != {} and prev_section != '':
                new_dict[prev_section] = sub_dict # Insert the sub_dict as the value to the new_dict
                sub_dict = {}
            key = re.sub(r'[0-9.:]', '', key).strip()  # Remove integers and punctuation from key
            prev_section = key
            if prev_section not in list(new_dict.keys()):
                new_dict[prev_section] = list(sections_dict.values())[index]
        else:
            key = re.sub(r'[0-9.:]', '', key).strip()  # Remove integers and punctuation from key
            sub_dict[key] = list(sections_dict.values())[index]
    if sub_dict != {} and prev_section != '': # Insert the last sub_dict as the value of the last section name
        new_dict[prev_section] = sub_dict 
    return new_dict


def is_correct_title(title):
    for c in title:
        if ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z'):
            return True
    return False
        

def divide_article_into_sections(article):
    sections = {}
    section_titles = re.findall(r'\d+\..+?\n', article)  # Find all lines that start with "number.title"
    
    # Remove the falsely selected section titles
    section_titles = [title for title in section_titles if '%' not in title] # EX: '2.5% ...' is not a section title
    
    # Check the correctness of the chosen section titles by checking the non-decreasing order of the section numbers
    correct_titles = []
    previous_number = 0  # Start with a sentinel value
    for title in section_titles:
        pos = article.find(title)
        prev_pos = pos-1
        # Extract the number at the start of the title
        match = re.match(r'(\d+)(\.\d+)?', title)
        if match:
            number = float(match.group(1))
            # Check if the main number (before the dot) is non-decreasing
            if number == previous_number or number == (previous_number + 1):
                # Check if there is a new line char before the title number
                if article[prev_pos] == '\n':
                    if is_correct_title(title):
                        correct_titles.append(title)
                        previous_number = number
                    
    section_titles = correct_titles
    
    # Use zip to pair section titles with their corresponding text
    for title, next_title in zip(section_titles, section_titles[1:] + ['']):
        # Get the start and end positions of each section
        start_pos = article.find(title)
        end_pos = article.find(next_title)
        
        # Extract the section text and remove the section title
        section_text = article[start_pos + len(title):end_pos].strip()
        
        # Store the section in the dictionary with the title as the key
        sections[title.strip()] = section_text
    
    abstract_types = ["abstract", "Abstract", "a b s t r a c t", "A B S T R A C T"]
    for type in abstract_types:
        if type in article:
            start_pos = article.find(type)
            end_pos = article.find(list(sections.keys())[0])
            section_text = article[start_pos + len(type):end_pos]
            new_sections_dic = {'abstract':section_text}
            new_sections_dic.update(sections)
            sections = new_sections_dic
            break

    # Cleaned sections dictionary
    cleaned_sections_dict = {}

    # Regular expression to match integers and punctuation
    regex = re.compile('[0-9\.\,\!\?\:\;\-\—\(\)]')

    for key, value in sections.items():
        # Remove integers and punctuation from the key
        cleaned_key = regex.sub('', key)
        # Convert key to lowercase
        cleaned_key = cleaned_key.lower()
        # Remove any extra whitespace
        cleaned_key = cleaned_key.strip()
        # Add to the cleaned dictionary
        cleaned_sections_dict[cleaned_key] = value

    return cleaned_sections_dict


if __name__ == "__main__":
    text = "Provide a summary of the text which is a section of an article. This is the section text:We tested the proposed model with the same sample of B2B firms inthe Chilean market, but in a new setting of economic expansion (T2),surveying the same informant of T1. The supplier’s managers agreed toparticipate in the research again, as part of an industrial developmentprogram in the host country. The subjects evaluated their industrialcontext for 2018 (regarding being in an economic recovery) on an 11-point scale with 0 = not at all and 10 = completely; the average resultwas 8.04. We replicated the Study 1 methodological approach, usingMLR and MIIV-2SLS estimations. The MLR and MIIV-2SLS results aresimilar in both direction and significance (see Web Appendix D). TheSEMs yielded satisfactory model fit considering PR, CTS, and EC as DVs(CFI = 0.958, 0.935, 0.963; SRMR = 0.082, 0.083, 0.085, respectively).These fit measures are in line with the established thresholds (Hu &Bentler, 1999). All item loadings were > 0.50, all AVEs were > 0.50, andall construct reliabilities were > 0.70. We found convergent anddiscriminant validity for all factors, checked with the Gerbing-Anderson(1988) and Fornell-Larcker (1981) criteria, respectively.Based on the MIIV-2SLS model results (see Sargan’s tests in WebAppendix E), interesting differences in the significance and direction ofcoefficients are identified in comparison with Study 1 findings. For allthree models, the path coefficient for the buyer–seller communicationopenness and customer value anticipation association (β = 0.615, p =0.000) is significant at the α = 0.05 level. Conversely, the path coeffi-cient for the buyer–seller technical involvement and customer valueanticipation association (β = 0.148, p = 0.163) is not significant at the α= 0.05 level. Hence, during times of economic recovery, firms shouldgenerate knowledge to adapt the relationship only via communication(consistent with times of economic crisis). In the model with PR as DV,the path coefficients linked to buyer–seller technical involvement andtop management compatibility effect on PR (β = 0.464; β = 0.436,respectively) are significant at the α = 0.05 level, while the path coef-ficient associated to customer value anticipation influence on PR ismarginally significant (β = 0.221, p = 0.092). To provide further detail(using MLR estimation), we tested the difference between INV → PRcoefficient and CVA → PR and TMC → PR coefficients, finding positivelysignificant differences at the α = 0.10 level (i.e., βINV > βCVA and βINV >βTMC). In the model with CTS as DV, only the influence of technicalinvolvement on CTS is significant (β = -0.451, p < 0.05), whereas thecoefficients for customer value anticipation and top managementcompatibility effect on CTS.(β = -0.183; β = -0.114, respectively) are not significant at the α =0.05 level.In the model with EC as DV, all the path coefficients linked totechnical involvement, customer value anticipation, and top manage-ment compatibility are significant (β = 0.599, p = 0.000; β = 0.390, p =2 The variable INV1 is used as measure (see Appendix).R. Mora Cortez et al.Journal of Business Research 165 (2023) 1140630.001; β = 0.890, p = 0.000, respectively). To provide further detail(using MLR estimation), we tested the difference between INV → ECcoefficient and CVA → EC and TMC → EC coefficients, finding non-significant differences at the α = 0.10 level. To validate that the find-ings from Studies 1 and 2 are comparable and to what extent, we ran ameasurement invariance test. This approach assesses a major potentialconfound in the data: measures could behave differently in differentgroups (i.e., T2 vs. T1). Our data support metric invariance (using MLRestimation), which allows a meaningful comparison of slope differencesacross groups (see Table 5). The fit of the model assuming metricinvariance is acceptable and not significantly different from the lessconstrained configural model (Δχ2PR = 1.950; Δχ2CTS = 3.503; Δχ2EC =2.935; ps < 0.05).We formally tested the slope coefficient differences between thegroups (T2 vs. T1) in R software, using MLR estimation. For all threemodels, there are no significant differences in the COM → INV and COM→ CVA coefficients at the α = 0.05 level. Thus, a change in the economictrajectory does not affect the relevance of the communication inbuyer–seller relationships as the coefficients remain similar (positiveand significant). Conversely, the INV → CVA coefficient significantlydiffers between the groups in all the models at the α = 0.10 level, withthe recovery/expansion scenario showing higher influence of technicalinvolvement on customer value anticipation (Δβs range from 0.310 to0.322; see Table 6).In the model with PR as DV, both the INV → PR and TMC → PRcoefficients are significantly lower in the crisis scenario (Δβ = 1.138, p< 0.05 and Δβ = 0.221, p < 0.10). The association between CVA and PRremains statistically similar in both times of crisis and times of recovery/expansion (Δβ = -0.301, p > 0.10). In the model with CTS as DV, whilethe CVA → CTS coefficient is significantly higher in times of recovery/expansion (Δβ = 0.381, p < 0.05), the INV → CTS coefficient is signif-icantly higher in times of crisis (Δβ = -0.756, p < 0.05). In addition, theTMC → CTS association (Δβ = 0.073, p = 0.563) does not differ betweenthe groups at the α = 0.05 level. In the model with EC as DV, both INV →EC and CVA → EC coefficients significantly differ between the groups,with the recovery scenario showing higher influence for INV and CVA onEC (Δβ = 0.815, p = 0.000 and Δβ = 0.309, p = 0.028, respectively) atthe α = 0.05 level. Also, the association between TMC and EC does notsignificantly differ between the groups (Δβ = -0.052, p > 0.10).Overall, times of economic crisis/contraction provide less RM pro-cess opportunities for suppliers to increase customer-level profitabilityand expectation of relationship continuity. Regarding the nine links tothe DVs in each scenario (T2 vs. T1), in the crisis setting only three effectsare significantly higher than zero, while in the expansion setting, sixeffects are significantly higher than zero (see Table 7). Buyer-sellertechnical involvement is the most controversial RM mechanism interms of volatility through a BC. During times of crisis, technicalinvolvement has a negative influence on both price and expectation ofcontinuity and a positive influence on reducing the cost-to-serve cus-tomers. Probably, both supplier and customer are fully aware of thecrisis risks and concentrate their efforts on reducing dyadic costs thatTable 5Measurement Invariance.Invarianced.f.CFIBICΔ BICΔ χ2p-valueDV: PRConfigural620.9387745Metric670.9407720−251.9500.856Scalar720.9427694−262.0120.847DV: CTSConfigural620.9307978Metric670.9317954−243.5030.623Scalar720.9337928−261.8940.863DV: ECConfigural620.9507550Metric670.9517525−252.9350.710Scalar720.9537499−262.0420.843Table 6Results – Multi-group Analysis (from MLR estimation).Path(T2 vs T1)βΔ (βT2- βT1)unstandardizedSEt-valuep-valueConclusionDV: PRCOM →INV−0.1710.120−1.4270.153Non-significantCOM →CVA−0.2390.175−1.3640.173Non-significantINV →CVA0.3180.1891.6830.092Significant†INV →PR1.1380.1627.0410.000Significant*CVA →PR−0.3010.196−1.5390.124Non-significantTMC →PR0.2210.1131.9550.051Significant†DV: CTSCOM →INV−0.1360.122−1.1120.266Non-significantCOM →CVA−0.2420.1661.4590.145Non-significantINV →CVA0.3220.1831.7650.078Significant†INV →CTS−0.7560.197−3.8340.000Significant*CVA →CTS0.3810.1692.2560.024Significant*TMC →CTS0.0730.1270.5790.563Non-significantDV: ECCOM →INV−0.1710.124−1.3810.167Non-significantCOM →CVA−0.2240.170−1.3180.187Non-significantINV →CVA0.3100.1861.6670.096Significant†INV →EC0.8150.1385.9070.000Significant*CVA →EC0.3090.1402.2030.028Significant*TMC →EC−0.0520.098−0.5280.597Non-significant† At the α = 0.10 (two-tailed) *At the α = 0.05 (two-tailed).Table 7Mechanisms for Successful Relationship Management of a Business Cycle (BC).VariableEffecton PREffecton CTSEffecton ECOverall Higher Order Effect onSupplier and RelationshipCrisis/contractionINV–+–Profitability can be > 0, positiveimpact on CTS should be higherthan negative impact on PR. Risk ofrelationship dissolution is increasedCVA+–0Profitability can be > 0, positiveimpact on PR should be higher thannegative impact on CTSTMC00+Risk of relationship dissolution isdecreasedRecovery/expansionINV+–+Profitability can be > 0, positiveimpact on PR should be higher thannegative impact on CTS. Risk ofrelationship dissolution isdecreasedCVA+0+Profitability is likely to be > 0, andrisk of relationship dissolution isdecreasedTMC+0+Profitability is likely to be > 0, andrisk of relationship dissolution isdecreasedR. Mora Cortez et al.Journal of Business Research 165 (2023) 114063could serve as an argument for the supplier to reduce its price. Duringtimes of recovery, technical involvement has a positive effect on bothprice and expectation of continuity and a negative influence on cost-to-serve. A possible explanation is both supplier and customer being able toperceive the growing opportunities, investing in new procedures ordevelopments that can increase the supplier’s cost-to-serve, but simul-taneously driving a higher, acceptable selling price. The influences ofboth CVA and TMC effect on the DVs are more stable through a BC, butnot entirely rigid. The CVA influence changes in the CTS model from anegative effect to a zero effect, and in the EC model from a zero effect toa positive effect. The TMC influence changes only in the PR model from azero effect to a positive effect (see Table 7).Provide a summary of the text which is a section of an article. This is the section text:We tested the proposed model with the same sample of B2B firms inthe Chilean market, but in a new setting of economic expansion (T2),surveying the same informant of T1. The supplier’s managers agreed toparticipate in the research again, as part of an industrial developmentprogram in the host country. The subjects evaluated their industrialcontext for 2018 (regarding being in an economic recovery) on an 11-point scale with 0 = not at all and 10 = completely; the average resultwas 8.04. We replicated the Study 1 methodological approach, usingMLR and MIIV-2SLS estimations. The MLR and MIIV-2SLS results aresimilar in both direction and significance (see Web Appendix D). TheSEMs yielded satisfactory model fit considering PR, CTS, and EC as DVs(CFI = 0.958, 0.935, 0.963; SRMR = 0.082, 0.083, 0.085, respectively).These fit measures are in line with the established thresholds (Hu &Bentler, 1999). All item loadings were > 0.50, all AVEs were > 0.50, andall construct reliabilities were > 0.70. We found convergent anddiscriminant validity for all factors, checked with the Gerbing-Anderson(1988) and Fornell-Larcker (1981) criteria, respectively.Based on the MIIV-2SLS model results (see Sargan’s tests in WebAppendix E), interesting differences in the significance and direction ofcoefficients are identified in comparison with Study 1 findings. For allthree models, the path coefficient for the buyer–seller communicationopenness and customer value anticipation association (β = 0.615, p =0.000) is significant at the α = 0.05 level. Conversely, the path coeffi-cient for the buyer–seller technical involvement and customer valueanticipation association (β = 0.148, p = 0.163) is not significant at the α= 0.05 level. Hence, during times of economic recovery, firms shouldgenerate knowledge to adapt the relationship only via communication(consistent with times of economic crisis). In the model with PR as DV,the path coefficients linked to buyer–seller technical involvement andtop management compatibility effect on PR (β = 0.464; β = 0.436,respectively) are significant at the α = 0.05 level, while the path coef-ficient associated to customer value anticipation influence on PR ismarginally significant (β = 0.221, p = 0.092). To provide further detail(using MLR estimation), we tested the difference between INV → PRcoefficient and CVA → PR and TMC → PR coefficients, finding positivelysignificant differences at the α = 0.10 level (i.e., βINV > βCVA and βINV >βTMC). In the model with CTS as DV, only the influence of technicalinvolvement on CTS is significant (β = -0.451, p < 0.05), whereas thecoefficients for customer value anticipation and top managementcompatibility effect on CTS.(β = -0.183; β = -0.114, respectively) are not significant at the α =0.05 level.In the model with EC as DV, all the path coefficients linked totechnical involvement, customer value anticipation, and top manage-ment compatibility are significant (β = 0.599, p = 0.000; β = 0.390, p =2 The variable INV1 is used as measure (see Appendix).R. Mora Cortez et al.Journal of Business Research 165 (2023) 1140630.001; β = 0.890, p = 0.000, respectively). To provide further detail(using MLR estimation), we tested the difference between INV → ECcoefficient and CVA → EC and TMC → EC coefficients, finding non-significant differences at the α = 0.10 level. To validate that the find-ings from Studies 1 and 2 are comparable and to what extent, we ran ameasurement invariance test. This approach assesses a major potentialconfound in the data: measures could behave differently in differentgroups (i.e., T2 vs. T1). Our data support metric invariance (using MLRestimation), which allows a meaningful comparison of slope differencesacross groups (see Table 5). The fit of the model assuming metricinvariance is acceptable and not significantly different from the lessconstrained configural model (Δχ2PR = 1.950; Δχ2CTS = 3.503; Δχ2EC =2.935; ps < 0.05).We formally tested the slope coefficient differences between thegroups (T2 vs. T1) in R software, using MLR estimation. For all threemodels, there are no significant differences in the COM → INV and COM→ CVA coefficients at the α = 0.05 level. Thus, a change in the economictrajectory does not affect the relevance of the communication inbuyer–seller relationships as the coefficients remain similar (positiveand significant). Conversely, the INV → CVA coefficient significantlydiffers between the groups in all the models at the α = 0.10 level, withthe recovery/expansion scenario showing higher influence of technicalinvolvement on customer value anticipation (Δβs range from 0.310 to0.322; see Table 6).In the model with PR as DV, both the INV → PR and TMC → PRcoefficients are significantly lower in the crisis scenario (Δβ = 1.138, p< 0.05 and Δβ = 0.221, p < 0.10). The association between CVA and PRremains statistically similar in both times of crisis and times of recovery/expansion (Δβ = -0.301, p > 0.10). In the model with CTS as DV, whilethe CVA → CTS coefficient is significantly higher in times of recovery/expansion (Δβ = 0.381, p < 0.05), the INV → CTS coefficient is signif-icantly higher in times of crisis (Δβ = -0.756, p < 0.05). In addition, theTMC → CTS association (Δβ = 0.073, p = 0.563) does not differ betweenthe groups at the α = 0.05 level. In the model with EC as DV, both INV →EC and CVA → EC coefficients significantly differ between the groups,with the recovery scenario showing higher influence for INV and CVA onEC (Δβ = 0.815, p = 0.000 and Δβ = 0.309, p = 0.028, respectively) atthe α = 0.05 level. Also, the association between TMC and EC does notsignificantly differ between the groups (Δβ = -0.052, p > 0.10).Overall, times of economic crisis/contraction provide less RM pro-cess opportunities for suppliers to increase customer-level profitabilityand expectation of relationship continuity. Regarding the nine links tothe DVs in each scenario (T2 vs. T1), in the crisis setting only three effectsare significantly higher than zero, while in the expansion setting, sixeffects are significantly higher than zero (see Table 7). Buyer-sellertechnical involvement is the most controversial RM mechanism interms of volatility through a BC. During times of crisis, technicalinvolvement has a negative influence on both price and expectation ofcontinuity and a positive influence on reducing the cost-to-serve cus-tomers. Probably, both supplier and customer are fully aware of thecrisis risks and concentrate their efforts on reducing dyadic costs thatTable 5Measurement Invariance.Invarianced.f.CFIBICΔ BICΔ χ2p-valueDV: PRConfigural620.9387745Metric670.9407720−251.9500.856Scalar720.9427694−262.0120.847DV: CTSConfigural620.9307978Metric670.9317954−243.5030.623Scalar720.9337928−261.8940.863DV: ECConfigural620.9507550Metric670.9517525−252.9350.710Scalar720.9537499−262.0420.843Table 6Results – Multi-group Analysis (from MLR estimation).Path(T2 vs T1)βΔ (βT2- βT1)unstandardizedSEt-valuep-valueConclusionDV: PRCOM →INV−0.1710.120−1.4270.153Non-significantCOM →CVA−0.2390.175−1.3640.173Non-significantINV →CVA0.3180.1891.6830.092Significant†INV →PR1.1380.1627.0410.000Significant*CVA →PR−0.3010.196−1.5390.124Non-significantTMC →PR0.2210.1131.9550.051Significant†DV: CTSCOM →INV−0.1360.122−1.1120.266Non-significantCOM →CVA−0.2420.1661.4590.145Non-significantINV →CVA0.3220.1831.7650.078Significant†INV →CTS−0.7560.197−3.8340.000Significant*CVA →CTS0.3810.1692.2560.024Significant*TMC →CTS0.0730.1270.5790.563Non-significantDV: ECCOM →INV−0.1710.124−1.3810.167Non-significantCOM →CVA−0.2240.170−1.3180.187Non-significantINV →CVA0.3100.1861.6670.096Significant†INV →EC0.8150.1385.9070.000Significant*CVA →EC0.3090.1402.2030.028Significant*TMC →EC−0.0520.098−0.5280.597Non-significant† At the α = 0.10 (two-tailed) *At the α = 0.05 (two-tailed).Table 7Mechanisms for Successful Relationship Management of a Business Cycle (BC).VariableEffecton PREffecton CTSEffecton ECOverall Higher Order Effect onSupplier and RelationshipCrisis/contractionINV–+–Profitability can be > 0, positiveimpact on CTS should be higherthan negative impact on PR. Risk ofrelationship dissolution is increasedCVA+–0Profitability can be > 0, positiveimpact on PR should be higher thannegative impact on CTSTMC00+Risk of relationship dissolution isdecreasedRecovery/expansionINV+–+Profitability can be > 0, positiveimpact on PR should be higher thannegative impact on CTS. Risk ofrelationship dissolution isdecreasedCVA+0+Profitability is likely to be > 0, andrisk of relationship dissolution isdecreasedTMC+0+Profitability is likely to be > 0, andrisk of relationship dissolution isdecreasedR. Mora Cortez et al.Journal of Business Research 165 (2023) 114063could serve as an argument for the supplier to reduce its price. Duringtimes of recovery, technical involvement has a positive effect on bothprice and expectation of continuity and a negative influence on cost-to-serve. A possible explanation is both supplier and customer being able toperceive the growing opportunities, investing in new procedures ordevelopments that can increase the supplier’s cost-to-serve, but simul-taneously driving a higher, acceptable selling price. The influences ofboth CVA and TMC effect on the DVs are more stable through a BC, butnot entirely rigid. The CVA influence changes in the CTS model from anegative effect to a zero effect, and in the EC model from a zero effect toa positive effect. The TMC influence changes only in the PR model from azero effect to a positive effect (see Table 7)."

    while len(text) > 12000:
        text = shorten_text(text)
        print(len(text))
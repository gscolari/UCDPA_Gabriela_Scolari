#!/usr/bin/env python
# coding: utf-8

# # Import libraries for reading data into frame, analysis and visualization 

# In[2]:


import pandas as pd 


# In[3]:


import numpy as np 


# In[4]:


import matplotlib.pyplot as plt 


# In[5]:


import seaborn as sns 


# # Import the CSV files into a Pandas Data Frame 

# In[7]:


violence = pd.read_csv('violence_against_women.csv') 


# In[8]:


contraceptive = pd.read_csv('contraceptive.csv', encoding='iso-8859-1') 


# # Sorting “contraceptive” data by Percentage distribution of women aged 15-49 (per country) - who have the relevant pregnancy intention and contraceptive use - in Descending Order  

# In[10]:


contracept_sorted = contraceptive.sort_values(by='Percentage distribution of women aged 15-49  (per country)', ascending=False) 


# # Sorting “violence” data by Value in Descending Order  - Value in this dataset means % of people surveyed in the relevant group who agree with the question (e.g. the percentage of women aged 15-24 in Afghanistan who agree that a husband is justified in hitting or beating his wife if she burns the food) 

# In[12]:


violence_sorted = violence.sort_values(by='Value', ascending=False)  


# # Checking for missing values 

# In[14]:


contracept_sorted.isnull().values.any() 


# In[15]:


violence_sorted.isnull().values.any() 


# # Replacing missing values 

# In[17]:


violence_sorted.fillna(0)  


# # head.() showing sorted values to start having first impressions 

# In[18]:


violence_sorted.head() 


# In[19]:


contracept_sorted.head() 
 


# # Here my analysis starts

# # Analysing how many women have the intention or not to avoid pregnancy grouped by “continent” and “pregnancy intention” 

# # The groupby function was the one that best suited this part of analysis since I wanted to know the difference amongst continents. 

# In[68]:


grouped = contraceptive.groupby(['Continent', 'Pregnancy intention']).size().unstack() 

grouped.plot(kind='bar', stacked=True) 


# # Analysing how many women want to avoid pregnancy related to having available contraceptive to meet their needs. 

# # Calculating value counts for "Pregnancy intention" and "Contraceptive availability" 

# In[21]:


pregnancy_counts = contraceptive['Pregnancy intention'].value_counts() 


# In[22]:


contraceptive_counts = contraceptive['Contraceptive availability'].value_counts() 


# # Creating a bar plot for visualization 

# In[23]:


plt.figure(figsize=(10, 6)) 


# # Plotting Pregnancy Intention 

# In[24]:


plt.subplot(1, 2, 1) 

pregnancy_counts.plot(kind='bar') 

plt.title('Pregnancy Intention Counts') 

plt.xlabel('Pregnancy Intention') 

plt.ylabel('Count') 

plt.show() 


# # Plotting Contraceptive Availability 

# In[25]:


plt.subplot(1, 2, 2) 

contraceptive_counts.plot(kind='bar') 

plt.title('Contraceptive Availability Counts') 

plt.xlabel('Contraceptive Availability') 

plt.ylabel('Count') 

plt.tight_layout() 

plt.show() 


# # This was my single analysis for “contraceptive” Data Frame. 

# # Now I will start analysing my second Data Frame, “violence” - This data was taken from a survey of men and women in African, Asian, and South American countries, exploring the attitudes and perceived justifications given for committing acts of violence against women. The data also explores different sociodemographic groups that the respondents belong to, including: Education Level, Marital status, Employment, and Age group. 

# # My first analysis is to have an overview of how many people with ages "15-24", "25-34", "35-49" years old participate of this survey. 

# # Filtered the Data Frame based on "Demographics Question" containing "age" 

# In[26]:


age_demographics = violence_sorted[violence_sorted['Demographics Question'].str.contains('age', case=False)] 


# # Counted the occurrences of each response in "Demographics Response" 

# In[27]:


response_counts = age_demographics['Demographics Response'].value_counts() 


# # Created a bar plot for visualization 

# In[28]:


plt.figure(figsize=(10, 6)) 

response_counts.plot(kind='bar') 

plt.title('Demographics Response for Age-related Questions') 

plt.xlabel('Demographics Response') 

plt.ylabel('Count') 

plt.xticks(rotation=45) 

plt.tight_layout() 

plt.show() 


# # Then I analysed the country with highest value (most violent country for women) and the lowest value (least violent country for women): 

# # Finding the country with the highest value 

# In[29]:


highest_value_country = violence_sorted.loc[violence_sorted['Value'].idxmax(), 'Country'] 
 


# # Finding the country with the lowest value 

# In[30]:


lowest_value_country = violence_sorted.loc[violence_sorted['Value'].idxmin(), 'Country'] 


# # printing results from findings 

# In[31]:


print(f"The country with the highest value, which means most violent country for women, is : {highest_value_country}") 


# In[32]:


print(f"The country with the lowest value, which means safest country for women, is: {lowest_value_country}") 


# # Then I analysed what country would be the middle term for women to live in, not the most violent neither the least violent 

# # Calculating the median of the "Value" column 

# In[33]:


median_value = violence_sorted['Value'].median() 


# # Finding the country closest to the median value 

# In[34]:


middle_country = violence_sorted.loc[ 

    violence_sorted['Value'].sub(median_value).abs().idxmin(), 

    'Country' 

] 


# # printing the result from finding 

# In[35]:


print(f"The country closest to the median value is: {middle_country}") 


# # I analysed by country, how many women with higher or no education suffer from violence. I wanted to know if women’s education has or hasn’t a relation with them suffering from violence. 

# # Filtering the Data Frame for "No education" and "Higher" in the column “Demographics Responses” 

# In[36]:


filtered_df = violence_sorted[ 

    (violence_sorted['Demographics Response'] == 'No education') | 

    (violence_sorted['Demographics Response'] == 'Higher') 

] 


# # Removing rows with missing "Value" data 

# In[37]:


filtered_df = filtered_df.dropna(subset=['Value']) 


# # Creating a bar plot using seaborn for visualization 

# In[38]:


plt.figure(figsize=(12, 6)) 

sns.barplot(data=filtered_df, x='Country', y='Value', hue='Demographics Response') 

plt.title('Comparison of Value for "No education" and "Higher" Demographics Responses') 

plt.xlabel('Country') 

plt.ylabel('Value') 

plt.xticks(rotation=45, ha='right') 

plt.tight_layout() 

plt.show() 


# # I analysed if employment status also makes a difference when the subject is violence against women 

# # Filtering the Data Frame for the desired “Demographics Responses” 

# In[39]:


filtered_df = violence_sorted[ 

    (violence_sorted['Demographics Response'] == 'Unemployed') | 

    (violence_sorted['Demographics Response'] == 'Employed for cash') | 

    (violence_sorted['Demographics Response'] == 'Employed for kind') | 

    (violence_sorted['Demographics Response'] == 'No education')  # Add missing value 

] 


# # Defining a custom colour palette 

# In[40]:


custom_palette = { 

    'Unemployed': 'orange', 

    'Employed for cash': 'green', 

    'Employed for kind': 'pink', 

    'No education': 'blue'  # Adjust color and label as needed 

} 


# # Creating a plot for visualization 

# In[41]:


plt.figure(figsize=(12, 6)) 

sns.barplot( 

    data=filtered_df, 

    x='Country', 

    y='Value', 

    hue='Demographics Response', 

    palette=custom_palette 

) 

plt.title('Comparison of Value for Different Employment Status') 

plt.xlabel('Country') 

plt.ylabel('Value') 

plt.xticks(rotation=45, ha='right') 

plt.tight_layout() 

plt.legend(title='Employment Status') 

plt.show() 


# # For my next analysis, I need the full list of countries in the column "Country" 

# # Extracting the list of unique countries from the "Country" column 

# In[42]:


countries_list = violence_sorted['Country'].unique() 


# # Printing the list of countries 

# In[43]:


print(countries_list) 


# 
# # My list has 79 countries, which I divided them by religion. I wanted to separate those countries by the most known religions, to have an overview if there’s relation between religion and violence against women. 

# # Lists of countries by religious groups 

# In[44]:


islam_countries = ['Afghanistan', 'Morocco', 'Mali', 'Eritrea', 'Chad', 'Azerbaijan', 'Gambia', 'Turkmenistan', 'Ethiopia', 'Guinea', 'Sierra Leone', 'Tajikistan', 'Pakistan', 'Egypt', 'Kyrgyz Republic', 'Yemen', 'Gabon', 'Kenya', 'Uganda', 'Senegal', 'Comoros', "Cote d'Ivoire", 'Niger', 'Somalia'] 

christianity_countries = ['Timor-Leste', 'Congo Democratic Republic', 'Congo', 'Tanzania', 'Zambia', 'Burundi', 'Lesotho', 'Nigeria', 'Liberia', 'Burkina Faso', 'Ghana', 'Armenia', 'Rwanda', 'Namibia', 'Sao Tome and Principe', 'Guyana', 'Albania', 'Maldives', 'Honduras', 'Nicaragua', 'Dominican Republic', 'Peru'] 

hinduism_countries = ['Nepal'] 

buddhism_countries = ['Myanmar', 'Cambodia'] 

african_traditional_countries = ['Zimbabwe', 'Cameroon', 'Kenya', 'Uganda', 'South Africa'] 

multiple_religions_countries = ['India', 'Indonesia', 'Togo', 'Bangladesh', 'Mozambique', 'Turkey', 'Madagascar', 'Benin', 'Angola', 'Philippines', 'Colombia', 'Malawi', 'Guatemala', 'Haiti', 'Bolivia', 'Nicaragua', 'Haiti', 'Bolivia', 'South Africa'] 


# # Creating a Data Frame with the categorized countries 

# In[45]:


categories_df = pd.DataFrame({ 

    'Country': islam_countries + christianity_countries + hinduism_countries + 

               buddhism_countries + african_traditional_countries + multiple_religions_countries, 

    'Religion': (['Islam'] * len(islam_countries)) + 

                (['Christianity'] * len(christianity_countries)) + 

                (['Hinduism'] * len(hinduism_countries)) + 

                (['Buddhism'] * len(buddhism_countries)) + 

                (['African Traditional'] * len(african_traditional_countries)) + 

                (['Multiple Religions'] * len(multiple_religions_countries)) 

}) 


#  # Merging the categorized Data Frame with the “violence_sorted” Data Frame to get the "Value" for each category 

# In[46]:


merged_df = pd.merge(categories_df, violence_sorted, on='Country', how='left') 


# # Grouping the merged Data Frame by "Religion" and calculate the sum of "Value" for each group 

# In[47]:


grouped_df = merged_df.groupby('Religion')['Value'].sum().reset_index() 


# # Creating a bar plot using matplotlib for visualization 

# In[48]:


plt.figure(figsize=(10, 6)) 

plt.bar(grouped_df['Religion'], grouped_df['Value']) 

plt.title('Comparison of "Value" by Religion Categories') 

plt.xlabel('Religion') 

plt.ylabel('Total Value') 

plt.tight_layout() 

plt.show() 


# # In this code, we create a new Data Frame called “categories_df” that includes all the categorized countries along with their respective religions. We then merge this Data Frame with the original “violence_sorted” Data Frame to get the "Value" for each category. After merging, we group the Data Frame by "Religion" and calculate the sum of "Value" for each group. Finally, we create a bar plot to compare the total "Value" for each religion category. 
#  

# # I decided to add the countries’ religion as a column – First I created the religion list 

# In[49]:


islam_countries = ['Afghanistan', 'Morocco', 'Mali', 'Eritrea', 'Chad', 'Azerbaijan', 'Gambia', 'Turkmenistan', 'Ethiopia', 'Guinea', 'Sierra Leone', 'Tajikistan', 'Pakistan', 'Egypt', 'Kyrgyz Republic', 'Yemen', 'Gabon', 'Kenya', 'Uganda', 'Senegal', 'Comoros', "Cote d'Ivoire", 'Niger', 'Somalia'] 

christianity_countries = ['Timor-Leste', 'Congo Democratic Republic', 'Congo', 'Tanzania', 'Zambia', 'Burundi', 'Lesotho', 'Nigeria', 'Liberia', 'Burkina Faso', 'Ghana', 'Armenia', 'Rwanda', 'Namibia', 'Sao Tome and Principe', 'Guyana', 'Albania', 'Maldives', 'Honduras', 'Nicaragua', 'Dominican Republic', 'Peru'] 

hinduism_countries = ['Nepal'] 

buddhism_countries = ['Myanmar', 'Cambodia'] 

african_traditional_countries = ['Zimbabwe', 'Cameroon', 'Kenya', 'Uganda', 'South Africa'] 

multiple_religions_countries = ['India', 'Indonesia', 'Togo', 'Bangladesh', 'Mozambique', 'Turkey', 'Madagascar', 'Benin', 'Angola', 'Philippines', 'Colombia', 'Malawi', 'Guatemala', 'Haiti', 'Bolivia', 'Nicaragua', 'Haiti', 'Bolivia', 'South Africa'] 

 


# # Creating a new column 'Religion' and initializing it as None 

# In[50]:


violence_sorted['Religion'] = None 


# # Setting the religion values based on the country lists 

# In[51]:


violence_sorted.loc[violence_sorted['Country'].isin(islam_countries), 'Religion'] = 'Islam' 

violence_sorted.loc[violence_sorted['Country'].isin(christianity_countries), 'Religion'] = 'Christianity' 

violence_sorted.loc[violence_sorted['Country'].isin(hinduism_countries), 'Religion'] = 'Hinduism' 

violence_sorted.loc[violence_sorted['Country'].isin(buddhism_countries), 'Religion'] = 'Buddhism' 

violence_sorted.loc[violence_sorted['Country'].isin(african_traditional_countries), 'Religion'] = 'African Traditional' 

violence_sorted.loc[violence_sorted['Country'].isin(multiple_religions_countries), 'Religion'] = 'Multiple Religions' 


# # Displaying the updated Data Frame head.() 

# In[52]:


print(violence_sorted.head()) 


# # My next analysis is to know if there is relation between violence against women compared to their marital status. 

# # List of desired "Demographics Response" categories 

# In[53]:


desired_categories = ['Never married', 'Widowed, divorced, separated', 'Married or living together'] 

 


# # Filtering the Data Frame for the desired "Demographics Response" categories 

# In[54]:


filtered_df = violence_sorted[violence_sorted['Demographics Response'].isin(desired_categories)] 


# # Creating a bar plot using seaborn for visualization 

# In[55]:


plt.figure(figsize=(12, 6)) 

sns.barplot(data=filtered_df, x='Demographics Response', y='Value') 

plt.title('Comparison of Value for Marital Status')  # Corrected line 

plt.xlabel('Demographics Response') 

plt.ylabel('Value') 

plt.tight_layout() 

plt.show() 


# # In this code, we use the isin() function to filter the original “violence_sorted” Data Frame to include only rows with "Demographics Response" values that match the desired categories. We then create a bar plot using seaborn to compare the "Value" for the specified "Demographics Response" categories.

# # Now my intention is to merge my violence against women Data Frame with my pregnancy and contraceptive Data Frame to analyse them together. I will merge them with how='inner', this means that the merge() function will only keep the rows where there is a matching "Country" value in both the "violence_sorted" and "contracept_sorted" data frames. Any rows with non-matching "Country" values will be dropped from the resulting merged_df data frame. 

# In[56]:


merged_df = violence_sorted.merge(contracept_sorted, on='Country', how='inner') 


# # I wanted to check the columns names of this new Data Frame 

# In[57]:


print(merged_df.columns) 


# # Then I wanted to check how many countries the Data Frame had in total 

# In[58]:


country_count = violence_sorted['Country'].nunique() 


# In[59]:


print("Number of unique countries:", country_count)  


# # Here I will start my merged analysis. I wanted to know, if religion impacts the intention of pregnancy in women.  

# # This code will create a bar plot using seaborn that shows the counts of "Not wanting to avoid pregnancy" and "Wanting to avoid pregnancy" for each religion. The x-axis represents different religions, the y-axis represents the count, and different colors represent the two pregnancy intention categories.  

# # Counting the occurrences of each combination of Pregnancy intention and Religion 

# In[60]:


count_df = merged_df.groupby(["Pregnancy intention", "Religion"]).size().reset_index(name="Count") 

 


# # Filtering for the desired values 

# In[61]:


not_wanting_to_avoid = count_df[(count_df["Pregnancy intention"] == "Not wanting to avoid pregnancy")] 

wanting_to_avoid = count_df[(count_df["Pregnancy intention"] == "Wanting to avoid pregnancy")] 


# # Setting the style of seaborn 

# In[62]:


sns.set(style="whitegrid") 


# # Creating a bar plot using seaborn 

# In[63]:


plt.figure(figsize=(10, 6)) 

sns.barplot(x="Religion", y="Count", hue="Pregnancy intention", data=count_df) 

plt.title("Pregnancy Intention by Religion") 

plt.xlabel("Religion") 

plt.ylabel("Count") 

plt.xticks(rotation=45) 

plt.legend(title="Pregnancy Intention") 

plt.tight_layout() 

plt.show() 


# # To finish my analysis, I wanted to analyse by religion, if the contraceptive needs of women were or weren’t met.  

# # Counting the occurrences of each combination of Contraceptive availability and Religion 

# In[64]:


count_df = merged_df.groupby(["Contraceptive availability", "Religion"]).size().reset_index(name="Count") 


# # Filtering for the desired values 

# In[65]:


met_need = count_df[(count_df["Contraceptive availability"] == "Met need")] 

unmet_need = count_df[(count_df["Contraceptive availability"] == "Unmet need")] 


# # Setting the style of seaborn 

# In[66]:


sns.set(style="whitegrid") 


# # Creating a bar plot using seaborn 

# In[67]:


plt.figure(figsize=(10, 6)) 

sns.barplot(x="Religion", y="Count", hue="Contraceptive availability", data=count_df) 

plt.title("Contraceptive Availability by Religion") 

plt.xlabel("Religion") 

plt.ylabel("Count") 

plt.xticks(rotation=45) 

plt.legend(title="Contraceptive Availability") 

plt.tight_layout() 

plt.show() 


# In[ ]:





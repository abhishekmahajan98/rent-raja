import pandas as pd
from openai import OpenAI
import os

PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')

class PropertyReportGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def create_property_context(self, df_row):
        def format_value(value, is_numeric=False):
            if pd.isna(value):
                return "No information available"
            if is_numeric and isinstance(value, (int, float)):
                return f"{value:,.2f}" if isinstance(value, float) else str(int(value))
            return str(value)
        
        return f"""
        Property Details:
        - Address: {format_value(df_row['street'])}
        - Price: ${format_value(df_row['price'], True)}
        - Location: {format_value(df_row['neighborhood'])}, {format_value(df_row['borough'])}
        - Beds/Baths: {format_value(df_row['beds'], True)}/{format_value(df_row['baths'], True)}
        - Built: {format_value(df_row['builtIn'], True)}
        - Description: {format_value(df_row['description'])}
        
        Neighborhood Statistics:
        - Demographics: {format_value(df_row['Black or African American Alone_ratio']*100 if not pd.isna(df_row['Black or African American Alone_ratio']) else None, True)}% Black, 
          {format_value(df_row['Hispanic or Latino_ratio']*100 if not pd.isna(df_row['Hispanic or Latino_ratio']) else None, True)}% Hispanic,
          {format_value(df_row['White Alone_ratio']*100 if not pd.isna(df_row['White Alone_ratio']) else None, True)}% White,
          {format_value(df_row['Asian Alone_ratio']*100 if not pd.isna(df_row['Asian Alone_ratio']) else None, True)}% Asian
        - Income: ${format_value(df_row['Median Household Income'], True)} median household
        - Safety Rank: {format_value(df_row['precinct_safety_rank'])}/74
        - Transit: {format_value(df_row['nearby_subway_stations'])} nearby subway stations
        """

    def generate_report(self, df_row):
        context = self.create_property_context(df_row)
        messages = [{
            "role": "system",
            "content": "You are a real estate analyst. Generate detailed property reports in markdown format."
        }, {
            "role": "user",
            "content": f"""
            Generate a detailed markdown property report based on this data:
            {context}
            
            The report should:
            1. Analyze the property's value proposition
            2. Evaluate the neighborhood
            3. Compare rental proposed price to market metrics
            4. Assess transportation and safety
            5. Include demographic insights
            6. Make renting recommendation
            
            Format in markdown with clear sections and bullet points where appropriate.
            """
        }]
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-small-128k-online",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None
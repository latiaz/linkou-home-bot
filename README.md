# Linkou Real Estate Information System

## Project Description

The Linkou Real Estate Information System is an open-source project dedicated to providing comprehensive and accessible real estate data for the Linkou District in New Taipei City, Taiwan. This project leverages web scraping techniques and government APIs to gather and integrate data, which is then automatically organized and analyzed to deliver valuable insights.

The project also features a LINE bot that allows users across Taiwan to easily access real-time updates and detailed information about the real estate market in the Linkou District. All features are provided for free to ensure that everyone can make informed decisions about real estate.

## Project Goals

- **Data Aggregation**: Collect real estate data from various sources including web scraping and government APIs.
- **Data Analysis**: Automatically organize and analyze the collected data to provide meaningful insights.
- **Public Accessibility**: Develop a LINE bot to disseminate real-time real estate information to the public.
- **Free and Open Source**: Ensure that all features and data are freely accessible to the public, promoting transparency in the real estate market.

## Features

- **Web Scraping**: Gather data from real estate websites.
- **API Integration**: Fetch data from government APIs.
- **Data Processing**: Clean and organize the collected data for analysis.
- **Analysis and Insights**: Provide insights into real estate trends and market conditions.
- **LINE Bot Integration**: Offer a user-friendly interface through a LINE bot for easy access to information.

## Installation

### Prerequisites

- Python 3.8+
- LINE Messaging API account

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/linkou-real-estate.git
    cd linkou-real-estate
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables for the LINE Messaging API and any other API keys required:
    ```bash
    export LINE_CHANNEL_SECRET=your_line_channel_secret
    export LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    export GOVERNMENT_API_KEY=your_government_api_key
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Deployment

For deployment, you can use services like Heroku, AWS, or any other cloud service provider. Ensure that your environment variables are properly set in your deployment configuration.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

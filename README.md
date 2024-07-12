![RSSfeed](https://github.com/dmitryporotnikov/unofficial_azure_updates/actions/workflows/generate_feed/badge.svg)

# Unofficial RSS feed for Azure Updates page

If you visit https://azure.microsoft.com/en-us/updates/, you will see the following message: 

***'Azure Updates website is undergoing maintenance. During this time, you may notice limited functionality affecting RSS feeds and search features. We apologize for any inconvenience this may cause. Thank you for your patience and understanding.'***

It seems the RSS feed is not available at the moment for Azure Updates. For my own convenience, I created a Python script that parses the webpage and a GitHub workflow that creates an RSS feed from this parse. The workflow runs every day at 00:00.

## RSS Feed Link

https://raw.githubusercontent.com/dmitryporotnikov/unofficial_azure_updates/main/latest_feed.xml

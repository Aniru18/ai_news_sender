from mcp_servers.news_server.services.extractor_service import extract_article_text

url = "https://news.google.com/rss/articles/CBMickFVX3lxTE52d29UR1pzUmtpS3RCS29ZOG1oLXp6bEdlS1p0ZWtjaDhzTDVWUGpEaGxmX09Jc3hRa2d4NTh1MkJaUmdZWllIR1FOeVcxTFpyeG5TZmRIUHR5Z3h4UVRpRXRjOFVoc3Vwa3hsVXNNU3ZCQQ?oc=5"

text = extract_article_text(url)

print("Length:", len(text))
print(text[:500])

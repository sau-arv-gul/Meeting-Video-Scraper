
# save the direct links in a json file
with open("direct_urls.json", "w") as f:
    json.dump(direct_url_list, f, indent=4)
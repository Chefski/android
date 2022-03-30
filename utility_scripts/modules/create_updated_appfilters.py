from bs4 import BeautifulSoup as bs


def main(appfilter_file, new_appfilters):
    with open(appfilter_file, encoding='utf-8') as file:
        content = bs(file.read(), 'xml')
        root = content.find("resources")

        for appfilter in new_appfilters:
            tag = bs.new_tag("item")
            tag.attrs['drawable'] = appfilter["drawable"]
            tag.attrs['componentInfo'] = "ComponentInfo\{%s\}" % appfilter["activity"]
            root.append(tag)

        file.write(str(content))
        file.close()

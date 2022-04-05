from bs4 import BeautifulSoup as bs


def main(appfilter_file, new_appfilters):
    with open(appfilter_file, 'r+', encoding='utf-8') as file:
        content = bs(file.read(), 'xml')

        for appfilter in new_appfilters:
            tag = content.new_tag("item", attrs={
                "drawable": appfilter["drawable"],
                "component": "ComponentInfo{%s}" % appfilter["activity"]
            })
            content.resources.append(tag)

        file.seek(0)
        file.write(str(content.prettify()))
        file.truncate()
        file.close()
